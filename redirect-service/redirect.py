import os
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def redirect_all(path):
    # クエリ文字列も含めた完全な URL を作成
    new_url = request.url.replace(request.host, 'feinatelier.org', 1)
    return redirect(new_url, code=301)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'  # デバッグモードを環境変数で制御
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
