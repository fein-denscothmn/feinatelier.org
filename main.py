import os
from flask import Flask, render_template, send_from_directory, abort
from sitemap import sitemap_bp
from pagelist import pagelist_bp

app = Flask(__name__)

app.register_blueprint(sitemap_bp)
app.register_blueprint(pagelist_bp, url_prefix='/pages')

@app.route('/')
def serve_static_index():
    return send_from_directory('www', 'index.html')

@app.route('/redirect')
def serve_redirect():
    return render_template('server/redirect.html')

@app.route('/top')
def serve_flask_content():
    return render_template('top.html')

@app.route('/<page_name>')
def serve_dynamic_content(page_name):
    try:
        return render_template(f'server/{page_name}.html')
    except:
        abort(404)

@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('www', filename)

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False') == 'True'
    app.run(debug=debug_mode)
