const CACHE_NAME = 'fein-cache-' + new Date().getTime();

const urlsToCache = [
 '/index.html'
];

self.addEventListener('install', event => {
 event.waitUntil(
  caches.open(CACHE_NAME)
   .then(cache => {
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
 if (event.request.mode === 'navigate') {

  event.respondWith(
   fetch(event.request)
    .then(response => {
     const clone = response.clone();
     caches.open(CACHE_NAME).then(cache => {
      cache.put(event.request, clone);
     });
     return response;
    })
    .catch(() => {
     return caches.match(event.request);
    })
  );
 } else {

  event.respondWith(
   caches.match(event.request)
    .then(response => {
     return response || fetch(event.request);
    })
  );
 }
});
