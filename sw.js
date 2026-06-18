const CACHE = 'bar-guide-v1';
const ASSETS = [
  '/BarGuide/',
  '/BarGuide/index.html',
  '/BarGuide/manifest.json',
  '/BarGuide/alligator.svg',
  '/BarGuide/icons/icon-192.png',
  '/BarGuide/icons/icon-512.png',
  '/BarGuide/images/bottles/bulleit-rye.jpg',
  '/BarGuide/images/bottles/whistlepig-10.jpg',
  '/BarGuide/images/bottles/whistlepig-15.jpg',
  '/BarGuide/images/bottles/knob-creek-rye.webp',
  '/BarGuide/images/bottles/jim-beam-rye.webp',
  '/BarGuide/images/bottles/michters-rye.webp',
  '/BarGuide/images/bottles/rabbit-hole-rye.png',
  '/BarGuide/images/bottles/rittenhouse-rye.jpg',
  '/BarGuide/images/bottles/sazerac-rye.jpg',
  '/BarGuide/images/bottles/bower-hill-rye.jpg',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request).catch(() => caches.match('/BarGuide/index.html')))
  );
});
