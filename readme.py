import os
import markdown
from flask import Blueprint, render_template_string

bp = Blueprint("readme", __name__)

BASE_DIR = os.path.dirname(__file__)
README_PATH = os.path.join(BASE_DIR, "README.md")

@bp.route("/readme")
def readme():
    with open(README_PATH, encoding="utf-8") as f:
        content = f.read()
    html = markdown.markdown(content, extensions=["extra", "nl2br"])
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="utf-8">
        <title>README_GitHub</title>


 <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/pstyle.css') }}">
 <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/style.css') }}">
 <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/header.css') }}">
 <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/footer.css') }}">
 <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/flower.css') }}">
 <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/menu.css') }}">
 <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/collapsible.css') }}">
 <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/feinpan.css') }}">
 <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/feinheadline1.css') }}">

 <link rel="preconnect" href="https://fonts.googleapis.com">
 <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
 <link
  href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@100..900&family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap"
  rel="stylesheet">
 <link rel="apple-touch-icon" sizes="180x180" href="{{ url_for('static', filename='icons/appleicon.png') }}">
 <link rel="icon" sizes="32x32" href="{{ url_for('static', filename='icons/favicon.ico') }}" type="image/x-icon">

 <script src="{{ url_for('static', filename='js/underline.js') }}"></script>
 <script src="{{ url_for('static', filename='js/feinfade.js') }}"></script>
 <script src="{{ url_for('static', filename='js/feinScroll.js') }}"></script>
 <script src="{{ url_for('static', filename='js/album.js') }}"></script>
 <script src="{{ url_for('static', filename='js/collapsible.js') }}"></script>

    </head>
    <body>

 <nav class="den_nav">
  <ul>
<li>
    <a href="/" class="animated-link feinhome-link">
     <img src="/menu/mspass.webp" alt="このサイトのシンボルマーク" class="feinhome">
     <span>fein's home</span>
    </a>
   </li>
   <li><a href="/another-eden/anaden_sitemap.html" class="animated-link">Another Eden</a></li>
   <li><a href="/fish/fish_sitemap.html" class="animated-link">Outdoor Activities</a></li>
   <li><a href="/contents/site_create.html" class="animated-link">Personal Website Creation</a></li>
   <li><a href="/contents/protect.html" class="animated-link">AI Block</a></li>
   <li><a href="/contents/rss.html" class="animated-link">Updates</a></li>
  </ul>
 </nav>

 <!--レスポンシブデザイン-->
 <div class="feincontainer">


  <!--パンくずリスト-->
  <div>
   <ol class="breadcrumb">
    <li class="breadcrumb-item"><a href="/">Home（グラスタの場所一覧表〜入手範囲別〜）</a></li>
    <li class="breadcrumb-item"><a href="/contents/site_create.html">個人サイト制作：サイトマップ</a></li>
    <li class="breadcrumb-item active" aria-current="page">README_GitHub</li>
   </ol>
  </div>

  <!-- ハンバーガーメニュー -->
  <div class="fden-hamburger-menu">
   <button class="fden-hamburger-button" id="fden-hamburger-button" onclick="toggleMenu()">☰ メニューを開く
    ▼</button>
   <div class="fden-menu" id="fden-menu">
    <!-- メニュー内容は外部ファイルから読み込む -->
    <div id="fden-menu-content"></div>
   </div>
  </div>
  <script src="{{ url_for('static', filename='js/menu.js') }}"></script>
  <!-- ハンバーガーメニューここまで -->

  <!--サイトタイトル-->
  <div class="header-frame">
   <div class="header-container">
    <img src="{{ url_for('static', filename='images/readme.png') }}" alt="Fein Atelier - org"
     class="header-image">
    <div class="header-text">
     <a href="https://feinatelier.org/">Fein Atelier - org</a>
    </div>
   </div>
  </div>

  <div class="spacer"></div>

  <button id="generate-headings" data-open-text="README_GitHubの目次を開く ▼"
   data-close-text="README_GitHubの目次を閉じる ▲">README_GitHubの目次を開く ▼</button><!--目次の自動生成-->
  <div class="spacer"></div>

  <p><a href="/contents/site_create.html">個人サイト制作：サイトマップへ戻る</a></p>

  <!-- ●ヘッダーここまで。直下でコンテンツ開始● -->

  <h1 class="background-waveimage-heading"><span>README_GitHub</span></h1>
<p>GitHub には README.md を置くことができ、アプリケーションの仕様が Markdown記法で書かれています。<br>
     これを Python Flask で HTML化して表示させて頂きました。<br>
     こちらのほうが読みやすいでしょう。</p>
<ul>
<li><a href="https://github.com/fein-denscothmn">feinのGitHubはこちらです</a></li>
<li>関連ページ：<a href="/contents/py_readme.html">GitHubのREADMEをPythonを使ってWebページにする</a></li>
</ul>

        {{ html|safe }}

<p>念のため、<a href="https://github.com/fein-denscothmn/fein-sites-dev1/blob/main/README.md">GitHubにあるREADME</a>へのリンクも付けておきますね。</p>
  <!-- ●ここから人間用のフッター● -->
  <hr id="feinhr">
  <div class="spacer"></div>

  <section class="sitemap">
   <h2 class="sitemap_heading">サイトマップ</h2>
   <p><a href="/pages/pagelist">全ページをリスト化したサイトマップ</a>も用意していますが、けっこうなページ数があります。<br>
    下記の「カテゴリー分けサイトマップ」のほうが使いやすいでしょう。</p>
   <p><a href="/another-eden/anaden_sitemap.html">
アナザーエデン関連ページ・サイトマップ</a><br>
アナザーエデンの強敵戦やストーリーコンテンツのリスト、お勧めバッジなどを掲載したコーナーです。<br>
期間限定のない普通のRPGですので、初心者でも安心して続けていけるゲームとなっています。<br>
もっとも重要なグラスタについては、場所別に網羅した表があります。</p>


   <p><a href="/contents/site_create.html">
     個人サイトのホスティングとコンテンツ作成</a><br>
個人でウェブサイトを作るなら時間をかけて。<br>
    HTML・CSS・JavaScriptの書き方はもちろん、無料かつ広告なしでホームページを作る方法を掲載したコーナーです。<br>
    Webデザインやレイアウトについても書いてあります。</p>
   <p><a href="/fish/fish_sitemap.html">魚釣りなどアウトドアのエリア</a><br>
ゲームとパソコンだけじゃなく、アウトドアも趣味なんです。<br>
    このコーナーでは魚釣りの記録とか、魚料理のレシピ、はたまたサイクリングなどなど。<br>
    アウトドアに関連するコンテンツが詰め込まれています。</p>

  </section>

  <!-- ページ上部へ戻るボタン -->
  <button id="scrollToTopBtn" onclick="scrollToTop()">ページ上部へ戻る</button>
  <script src="{{ url_for('static', filename='js/feinScroll.js') }}"></script>

  <div class="spacer"></div>

  <footer>
   <!--common google digital leader-->

   <div id="commongdl"></div>
   <script src="{{ url_for('static', filename='externalization/common.js') }}"></script>

   <div class="spacer"></div>


   <div class="spacer"></div>
   <p class="portal" id="updated-date">この <a href="https://feinatelier.org/">fein's personal
     site</a> は、2023/7/4に開設された <a href="https://portal.feinatelier.org/">fein's portal</a>
    を母体として、yyyy/mm/ddに至るまで更新し続けられています。</p>
   <script>
    document.addEventListener('DOMContentLoaded', function () {
     const today = new Date();
     const year = today.getFullYear();
     const month = String(today.getMonth() + 1).padStart(2, '0');
     const day = String(today.getDate()).padStart(2, '0');
     const dateElement = document.getElementById('updated-date');
     dateElement.innerHTML = `この <a href="https://feinatelier.org/">Fein Atelier - org</a> は、2023/7/4に開設された <a href="https://portal.feinatelier.org/">fein's portal</a> を母体として、${year}/${month}/${day}に至るまで更新し続けられています。`;
    });
   </script>

  </footer>

 </div><!--レスポンシブデザイン-->

 <script src="{{ url_for('static', filename='js/feinheadline1.js') }}"></script><!--見出しの自動生成-->

 <!-- ●ここまで人間用のフッター。直下でbodyを閉める● -->
    </body>
    </html>
    """, html=html)
