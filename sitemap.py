import os
from flask import Blueprint, Response, render_template
import datetime

sitemap_bp = Blueprint('sitemap', __name__)

def get_static_pages():
    static_dir = 'www'
    static_pages = []
    for root, dirs, files in os.walk(static_dir):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file).replace('\\', '/')
                url = path.replace(static_dir, '').lstrip('/')
                static_pages.append({
                    'loc': f'https://feinatelier.org/{url}',
                    'lastmod': datetime.datetime.now().strftime('%Y-%m-%d'),
                })
    return static_pages

def get_dynamic_pages(app):
    dynamic_pages = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static' and '<' not in rule.rule and rule.rule != '/<page_name>' and rule.rule != '/<path:filename>':
            url = f'https://feinatelier.org{rule.rule}'
            dynamic_pages.append({
                'loc': url,
                'lastmod': datetime.datetime.now().strftime('%Y-%m-%d'),
            })
    return dynamic_pages

@sitemap_bp.route('/sitemap.xml')
def sitemap():
    from main import app

    static_pages = get_static_pages()
    print(f"Static Pages: {static_pages}")

    dynamic_pages = get_dynamic_pages(app)
    print(f"Dynamic Pages: {dynamic_pages}")

    pages = static_pages + dynamic_pages
    print(f"All Pages: {pages}")

    sitemap_xml = render_template('sitemap.xml', pages=pages,
                                  generated_date=datetime.datetime.now().strftime('%Y-%m-%d'))
    return Response(sitemap_xml, mimetype='application/xml')
