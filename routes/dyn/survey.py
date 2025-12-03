from flask import Blueprint, request, jsonify
import requests
import os

bp = Blueprint("survey", __name__)

API_KEY = os.getenv("PAGESPEED_API_KEY")

@bp.route("/", methods=["GET"])
def survey_home():
    # クエリパラメータからURLを取得。指定がなければexample.com
    test_url = request.args.get("url", "https://example.com")

    api_url = (
        f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        f"?url={test_url}&key={API_KEY}"
    )

    try:
        resp = requests.get(api_url)
        data = resp.json()

        score = data.get("lighthouseResult", {}).get("categories", {}).get("performance", {}).get("score", None)

        return jsonify({
            "tested_url": test_url,
            "performance_score": score
        })
    except Exception as e:
        return jsonify({"error": str(e)})
