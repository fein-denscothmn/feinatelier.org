from flask import Blueprint, request, jsonify
import requests
import os
import json
# 認証と安定した外部通信に必要なライブラリをインポート
from google.auth.transport.requests import AuthorizedSession
from google.auth import default
from google.auth.exceptions import DefaultCredentialsError

# Datastore モデルのインポート
from routes.dyn.datastore_models import PagespeedResult

# Blueprint に url_prefix を指定（/dyn/worker/pagespeed が目標）
bp = Blueprint("worker", __name__, url_prefix="/dyn/worker")

# Pagespeed APIキーは環境変数から取得
API_KEY = os.getenv("PAGESPEED_API_KEY")

# 認証セッションの初期化
# GAEサービスアカウントの認証情報を使用して、APIへのアクセスを安定させる
try:
    credentials, _ = default()
    # 認証セッションを作成
    AUTH_SESSION = AuthorizedSession(credentials)
except DefaultCredentialsError as e:
    # 認証情報が見つからない場合のフォールバック（主にローカル環境でのデバッグ用）
    print(f"[WORKER INIT ERROR] Default credentials not found. Using unauthenticated session: {e}")
    AUTH_SESSION = requests.Session()


def run_pagespeed_api(url: str, strategy: str):
    """Pagespeed APIを同期的に叩き、結果を辞書で返す"""

    if not API_KEY:
        error_message = "PAGESPEED_API_KEY is not set in the environment."
        print(f"[WORKER ERROR] {error_message}")
        return {"error": error_message}

    api_url = (
        f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        f"?url={url}&strategy={strategy}&key={API_KEY}"
    )

    try:
        # requests.getの代わりに、認証セッションを使用してAPIを呼び出す
        resp = AUTH_SESSION.get(api_url, timeout=30)
        print(f"[WORKER DEBUG] URL={url}, Strategy={strategy}, Status={resp.status_code}")

        resp.raise_for_status() # HTTPエラー（4xx, 5xx）なら例外を投げる
        data = resp.json()

    except requests.exceptions.RequestException as e:
        # HTTP通信そのものが失敗
        error_message = f"HTTP request failed: {type(e).__name__} - {e}"
        print(f"[WORKER API ERROR] {error_message}")
        return {"error": error_message}
    except ValueError as e:
        # JSON解析が失敗（不正なレスポンスが返ってきた）
        error_message = f"JSON parse error: {e}"
        print(f"[WORKER API ERROR] {error_message}")
        return {"error": error_message}

    if "error" in data:
        # Pagespeed API自体がエラーメッセージを返してきた場合
        api_error_message = data["error"].get("message", "Unknown API error")
        error_message = f"Pagespeed API returned error: {api_error_message}"
        print(f"[WORKER API ERROR] {error_message}")
        # APIのエラーメッセージを Datastore に保存するために辞書として返す
        return {"error": error_message}

    # Pagespeed Insightsのデータを抽出
    lighthouse = data.get("lighthouseResult", {})
    categories = lighthouse.get("categories", {})
    audits = lighthouse.get("audits", {})

    # 結果をDatastore保存用に整形して返す
    return {
        "score": categories.get("performance", {}).get("score", None),
        "fcp": audits.get("first-contentful-paint", {}).get("displayValue"),
        "lcp": audits.get("largest-contentful-paint", {}).get("displayValue"),
        "cls": audits.get("cumulative-layout-shift", {}).get("displayValue"),
        "tbt": audits.get("total-blocking-time", {}).get("displayValue"),
        "speed_index": audits.get("speed-index", {}).get("displayValue"),
        "tti": audits.get("interactive", {}).get("displayValue"),
        "error": None # 成功時はエラーを None に設定
    }


@bp.route("/pagespeed", methods=["POST"])
def pagespeed_worker():
    """Cloud Tasksから呼び出され、計測を実行し、Datastoreに保存するエンドポイント"""
    payload = None # エラーハンドリングのために先に定義
    url = "unknown_url"
    strategy = "unknown_strategy"

    try:
        # Cloud Tasksから送られてくる JSON ペイロードを解析
        payload = request.get_json(silent=True)
        if not payload or 'url' not in payload or 'strategy' not in payload:
            # ログを記録してから失敗
            print(f"[WORKER FATAL ERROR] Invalid task payload received: {payload}")
            return jsonify({"status": "error", "message": "Invalid task payload"}), 400

        url = payload['url']
        strategy = payload['strategy']

        print(f"[WORKER] Starting Pagespeed measurement for {url} ({strategy})")

        # 1. API呼び出しの実行 (成功/失敗にかかわらず結果を result_data に格納)
        result_data = run_pagespeed_api(url, strategy)

        # 2. Datastoreへの保存 (成功しても失敗しても、result_dataの内容を保存する)
        PagespeedResult.save_result(url, strategy, result_data)

        # result_dataにエラーが含まれていれば、ワーカー処理は成功だが、API呼び出しは失敗
        if "error" in result_data and result_data["error"] is not None:
            # API呼び出しエラーを記録したため、Cloud Tasksに対しては成功ステータス（200 OK）を返す
            # これでリトライが止まり、エラーがレポートに表示される
            print(f"[WORKER] Pagespeed API failed but error saved to Datastore. Stopping retry.")
            return jsonify({"status": "error_logged", "url": url, "strategy": strategy, "error": result_data["error"]}), 200

        # 成功ステータス（200 OK）を返す
        return jsonify({"status": "success", "url": url, "strategy": strategy}), 200

    except Exception as e:
        # ワーカー処理自体の致命的なエラー（ex: Datastore接続失敗、不正なJSON）
        # このエラーをDatastoreに記録し、リトライを停止させる
        fatal_error_message = f"Unhandled exception in worker process: {str(e)}"
        print(f"[WORKER FATAL ERROR] {fatal_error_message}")

        # 致命的なエラーもDatastoreに記録して、レポートに表示させる
        PagespeedResult.save_result(url, strategy, {"error": fatal_error_message})

        # エラーを記録したので、Cloud Tasksに対しては成功として扱い、リトライを停止
        return jsonify({"status": "fatal_error_logged", "message": fatal_error_message}), 200
