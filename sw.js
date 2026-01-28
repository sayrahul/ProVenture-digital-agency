const CACHE_Name = 'proventure-v1';
const ASSETS = [
    '/',
    '/index.html',
    '/custom/css/main.css',
    '/custom/css/proventure-custom.css',
    '/custom/js/proventure-custom.js',
    '/custom/js/bg-animation.js',
    '/site.webmanifest',
    '/favicon.ico'
];

self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open(CACHE_Name).then((cache) => {
            return cache.addAll(ASSETS);
        })
    );
});

self.addEventListener('fetch', (e) => {
    e.respondWith(
        caches.match(e.request).then((response) => {
            return response || fetch(e.request);
        })
    );
});
