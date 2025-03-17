import os
from flask import Blueprint, render_template
from bs4 import BeautifulSoup

pagelist_bp = Blueprint('pagelist', __name__)

def get_category_pages_with_titles(category_name):
    static_dir = 'www'
    category_pages = []
    excluded_paths = [
        '/index.html',
        '/externalization/commongdl.html',
        '/menu/menu.html',
        '/another-eden/anaden_sitemap.html',
        '/contents/site_create.html',
        '/fish/fish_sitemap.html',
        '/contents/rss.html',
        '/sitemap.xml',
        '/contents/x_exoduslink.html',
        '/menu/symbol.html',
        '/pages/pagelist',
        '/'
    ]

    for root, dirs, files in os.walk(static_dir):
        if category_name in root:
            for file in files:
                if file.endswith('.html'):
                    path = os.path.join(root, file).replace('\\', '/')
                    url = path.replace(static_dir, '').lstrip('/')
                    if f'/{url}' not in excluded_paths:
                        title = get_page_title(path)
                        category_pages.append({'url': f'/{url}', 'title': title})
    return category_pages

def get_page_title(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            return soup.title.string if soup.title else 'No Title'
    except Exception as e:
        return 'Error Reading Title'

def get_another_eden_pages():
    return get_category_pages_with_titles('another-eden')

def get_contents_pages():
    return get_category_pages_with_titles('contents')

def get_fish_pages():
    return get_category_pages_with_titles('fish')

def get_rss_pages():
    return get_category_pages_with_titles('rss')

def get_dynamic_pages(app):
    dynamic_pages = []
    excluded_paths = [
        '/index.html',
        '/externalization/commongdl.html',
        '/menu/menu.html',
        '/another-eden/anaden_sitemap.html',
        '/contents/site_create.html',
        '/fish/fish_sitemap.html',
        '/contents/rss.html',
        '/sitemap.xml',
        '/contents/x_exoduslink.html',
        '/menu/symbol.html',
        '/pages/pagelist',
        '/'
    ]

    url_to_title = {
        '/': None,
        '/sitemap.xml': 'サイトマップのXML表示',
        '/pages/pagelist': None,
        '/redirect': '独自ドメイン設定後にリダイレクト機能を追加する',
        '/top': '個人サイトへPythonのFlaskを導入する'
    }

    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static' and '<' not in rule.rule and rule.rule not in excluded_paths:
            title = url_to_title.get(rule.rule, 'Dynamic Page')
            if title:
                dynamic_pages.append({'url': rule.rule, 'title': title})

    return dynamic_pages

@pagelist_bp.route('/pagelist')
def pagelist():
    from main import app

    pages_by_category = {
        'Another Eden': get_another_eden_pages(),
        'Contents': get_contents_pages(),
        'Fish': get_fish_pages(),
        'RSS': get_rss_pages(),
        'Dynamic': get_dynamic_pages(app)
    }

    return render_template('pagelist.html', pages_by_category=pages_by_category)
