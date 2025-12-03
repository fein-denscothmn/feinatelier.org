import os
import json
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, render_template
from google.cloud import tasks_v2
# Datastoreからのインポート名を修正（get_latest_resultメソッドがPagespeedResultクラスにあると仮定）
from routes.dyn.datastore_models import PagespeedResult


# --- 設定 ---

# GAEプロジェクトの設定
PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT')
GAE_LOCATION = os.environ.get('GAE_LOCATION', 'europe-west3') # 環境変数から取得、なければ 'europe-west3'
QUEUE_NAME = 'pagespeed-queue' # Cloud Tasks キュー名

# データ鮮度設定（例: 7日より古い場合は再計測）
RECHECK_INTERVAL = timedelta(days=7)

# 計測対象 URL リスト
TARGET_URLS = [
    "https://feinatelier.org/another-eden/atelier_studio.html",
]

# --- Cloud Tasks 初期化 ---

# Cloud Tasks クライアントの初期化
try:
    tasks_client = tasks_v2.CloudTasksClient()
    queue_path = tasks_client.queue_path(PROJECT_ID, GAE_LOCATION, QUEUE_NAME)
except Exception as e:
    # ローカル実行などでプロジェクトIDがない場合のエラーをキャッチ
    print(f"[ERROR] Cloud Tasks Client initialization failed: {e}")
    tasks_client = None
    queue_path = None


# --- ユーティリティ関数 ---

def create_pagespeed_task(url: str, strategy: str):
    """Pagespeed API呼び出しタスクをCloud Tasksにキューイングする"""

    if not tasks_client:
        print("[ERROR] Cloud Tasks client not initialized. Skipping task creation.")
        return False

    # タスクペイロード（ワーカーエンドポイントに渡すデータ）
    payload = {
        "url": url,
        "strategy": strategy,
    }

    relative_uri = '/dyn/worker/pagespeed'

    task = {
        'app_engine_http_request': {
            'http_method': 'POST',
            'relative_uri': relative_uri,
            'body': json.dumps(payload).encode('utf-8'),
            'headers': {'Content-Type': 'application/json'},
        }
    }

    # タスクが重複しないように、URLとStrategyに基づいた名前を設定
    # Cloud Tasksは同じ名前のタスクをキュー内に保持しないため、重複実行防止に役立つ
    task_name = f'pagespeed-{url.replace("/", "_").replace(":", "_")}-{strategy}'
    task['name'] = tasks_client.task_path(PROJECT_ID, GAE_LOCATION, QUEUE_NAME, task_name)

    # タスクをキューに追加（即時実行）
    try:
        tasks_client.create_task(parent=queue_path, task=task)
        print(f"[INFO] Task created for {url} ({strategy})")
        return True
    except Exception as e:
        # タスクが既にキューに存在する場合（Cloud Tasksの仕様）はエラーではない
        if 'ALREADY_EXISTS' in str(e):
            print(f"[INFO] Task already exists for {url} ({strategy}). Skipping.")
            return True
        print(f"[ERROR] Failed to create task: {e}")
        return False


def get_and_queue_results():
    """
    Datastoreから最新の結果を取得し、
    結果がない、または古い場合はタスクをキューイングする。
    """
    pages = []
    now = datetime.utcnow()

    for url in TARGET_URLS:
        page_data = {"url": url, "mobile": None, "desktop": None}

        # --- モバイル結果の処理 ---
        mobile_result = PagespeedResult.get_latest_result(url, "mobile")

        # 鮮度チェック: 結果がない or 古い場合、タスクをキューイング
        if mobile_result is None or (now - mobile_result.timestamp) > RECHECK_INTERVAL:
            page_data["mobile"] = {"error": "Processing..."}
            create_pagespeed_task(url, "mobile")
            # Datastoreに古いデータがある場合は、Processing中でも古いデータを表示するために残す
            if mobile_result:
                page_data["mobile"]["old_data"] = PagespeedResult.to_dict(mobile_result) # to_dictの呼び出し方を修正
        else:
            # 最新の結果がある場合
            page_data["mobile"] = PagespeedResult.to_dict(mobile_result) # to_dictの呼び出し方を修正

        # --- デスクトップ結果の処理 ---
        desktop_result = PagespeedResult.get_latest_result(url, "desktop")

        # 鮮度チェック: 結果がない or 古い場合、タスクをキューイング
        if desktop_result is None or (now - desktop_result.timestamp) > RECHECK_INTERVAL:
            page_data["desktop"] = {"error": "Processing..."}
            create_pagespeed_task(url, "desktop")
            # Datastoreに古いデータがある場合は、Processing中でも古いデータを表示するために残す
            if desktop_result:
                page_data["desktop"]["old_data"] = PagespeedResult.to_dict(desktop_result) # to_dictの呼び出し方を修正
        else:
            # 最新の結果がある場合
            page_data["desktop"] = PagespeedResult.to_dict(desktop_result) # to_dictの呼び出し方を修正

        pages.append(page_data)

    return pages


# --- Flask ルート定義 ---

# Blueprintの定義をここで行う（重複は禁止）
bp = Blueprint("survey", __name__, url_prefix="/dyn/survey")

@bp.route("/json", methods=["GET"])
def survey_json():
    """JSON形式でPagespeedの結果を返す（最新結果があれば表示、なければキューイング）"""
    results = get_and_queue_results()

    # to_dict() で Datastore Entity から辞書に変換済みのため、そのまま jsonify
    return jsonify({"results": results})

@bp.route("/", methods=["GET"])
def survey_home():
    """HTMLテンプレートでPagespeedの結果を返す（最新結果があれば表示、なければキューイング）"""
    pages = get_and_queue_results()

    # pages は Datastore Entity ではなく、整形された辞書リストであることに注意
    return render_template("survey_report.html", pages=pages)
