const CACHE = 'spread-pwa-v1';
const ASSETS = ['/app/', '/static/portal/css/app.css'];
self.addEventListener('install', e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS))));
self.addEventListener('fetch', e => e.respondWith(fetch(e.request).catch(() => caches.match(e.request))));
