import os
from flask import Flask, render_template, send_from_directory, abort
from sitemap import sitemap_bp  # Blueprintのインポート

app = Flask(__name__)

# Blueprintの登録
app.register_blueprint(sitemap_bp)

# ルート `/` で `index.html` をレンダリング
@app.route('/')
def serve_static_index():
    return send_from_directory('www', 'index.html')

# 明示的な動的ルート：/redirect
@app.route('/redirect')
def serve_redirect():
    # 動的に templates/server/redirect.html をレンダリングする
    return render_template('server/redirect.html')

# Flask の動的コンテンツ：/top
@app.route('/top')
def serve_flask_content():
    return render_template('top.html')

# 意図的な動的ルート：templates/server 以下の HTML を対応（例：/about, /contact など）
@app.route('/<page_name>')
def serve_dynamic_content(page_name):
    try:
        return render_template(f'server/{page_name}.html')
    except:
        abort(404)

# キャッチオール：静的ファイルを提供
@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('www', filename)

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False') == 'True'
    app.run(debug=debug_mode)
