const CACHE_NAME = 'fein-cache-' + new Date().getTime();

// 変更点 1: /index.html の事前キャッシュを削除
// これにより、HTMLの更新をService Workerのバージョン管理に依存せず、ネットワーク優先の戦略で最新を取得する
const urlsToCache = [

];

self.addEventListener('install', event => {
 event.waitUntil(
  caches.open(CACHE_NAME)
   .then(cache => {
    // 事前キャッシュするファイルがなければ、空のまま続行
    return cache.addAll(urlsToCache);
   })
 );
 self.skipWaiting();
});

self.addEventListener('activate', event => {
 event.waitUntil(
  caches.keys().then(cacheNames => {
   return Promise.all(
    cacheNames.filter(function (cacheName) {

     return cacheName.startsWith('fein-cache-') && cacheName !== CACHE_NAME;
    }).map(function (cacheName) {
     return caches.delete(cacheName);
    })
   );
  })
 );
 self.clients.claim();
});

self.addEventListener('fetch', event => {
 // ナビゲーションリクエスト (HTMLページ) の処理
 if (event.request.mode === 'navigate') {

  event.respondWith(
   fetch(event.request) // ネットワーク優先 (CDNを経由)
    .then(response => {
     const clone = response.clone();
     // 取得した最新のHTMLをService Workerのキャッシュに保存 (オフライン用)
     caches.open(CACHE_NAME).then(cache => {
      cache.put(event.request, clone);
     });
     return response;
    })
    .catch(() => {
     // ネットワーク失敗時は Service Worker のキャッシュから返す (オフライン対応)
     return caches.match(event.request);
    })
  );
 } else {
  // 変更点 2: 静的ファイル (画像, CSS, JS) の処理
  // Service Workerのキャッシュ確認をせず、常にネットワーク (CDN) へリクエストを渡す
  // これにより、App EngineのCache-Controlヘッダーが尊重される
  event.respondWith(
   fetch(event.request)
  );
 }
});
