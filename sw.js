const CACHE = 'bar-guide-v6';
const ASSETS = [
  '/BarGuide/',
  '/BarGuide/index.html',
  '/BarGuide/manifest.json',
  '/BarGuide/alligator.svg',
  '/BarGuide/icons/icon-192.png',
  '/BarGuide/icons/icon-512.png',
  '/BarGuide/images/bottles/ardbeg-uigeadail.jpg',
  '/BarGuide/images/bottles/ardbeg-wee-beastie.avif',
  '/BarGuide/images/bottles/balvenie-portwood-21.webp',
  '/BarGuide/images/bottles/bernheim.jpg',
  '/BarGuide/images/bottles/blantons-gold.webp',
  '/BarGuide/images/bottles/bower-hill-rye.jpg',
  '/BarGuide/images/bottles/bowmore-12.webp',
  '/BarGuide/images/bottles/buffalo-trace.webp',
  '/BarGuide/images/bottles/bulleit-bourbon.png',
  '/BarGuide/images/bottles/bulleit-bourbon-10.jpg',
  '/BarGuide/images/bottles/bulleit-rye.jpg',
  '/BarGuide/images/bottles/clynelish-14.webp',
  '/BarGuide/images/bottles/dalmore-king-alexander.webp',
  '/BarGuide/images/bottles/elijah-craig.webp',
  '/BarGuide/images/bottles/evan-williams.jpg',
  '/BarGuide/images/bottles/gentleman-jack.webp',
  '/BarGuide/images/bottles/glenfiddich-18.webp',
  '/BarGuide/images/bottles/glenfiddich-21.jpg',
  '/BarGuide/images/bottles/glenfiddich-grand-cru.avif',
  '/BarGuide/images/bottles/glenfiddich-grande-couronne.jpg',
  '/BarGuide/images/bottles/highland-park-dark-origins.jpg',
  '/BarGuide/images/bottles/hudson-rye.webp',
  '/BarGuide/images/bottles/jameson-black-barrel.webp',
  '/BarGuide/images/bottles/jd-single-barrel-rye.webp',
  '/BarGuide/images/bottles/jim-beam-rye.webp',
  '/BarGuide/images/bottles/johnny-drum.webp',
  '/BarGuide/images/bottles/jw-black-label.webp',
  '/BarGuide/images/bottles/jw-blue-label.webp',
  '/BarGuide/images/bottles/knob-creek-bourbon.jpg',
  '/BarGuide/images/bottles/knob-creek-rye.webp',
  '/BarGuide/images/bottles/lagavulin-16.jpg',
  '/BarGuide/images/bottles/laphroaig-quarter-cask.jpg',
  '/BarGuide/images/bottles/michters-10yr-bourbon.jpg',
  '/BarGuide/images/bottles/michters-10yr-rye.webp',
  '/BarGuide/images/bottles/michters-bourbon.jpg',
  '/BarGuide/images/bottles/michters-rye.webp',
  '/BarGuide/images/bottles/michters-sour-mash.jpg',
  '/BarGuide/images/bottles/nikka-from-the-barrel.webp',
  '/BarGuide/images/bottles/noahs-mill.jpg',
  '/BarGuide/images/bottles/oban-14.webp',
  '/BarGuide/images/bottles/old-crow.webp',
  '/BarGuide/images/bottles/old-rip-van-winkle.jpg',
  '/BarGuide/images/bottles/rabbit-hole-bourbon.jpg',
  '/BarGuide/images/bottles/rabbit-hole-rye.png',
  '/BarGuide/images/bottles/rittenhouse-rye.jpg',
  '/BarGuide/images/bottles/roe-and-co.jpg',
  '/BarGuide/images/bottles/rowans-creek.webp',
  '/BarGuide/images/bottles/sazerac-rye.jpg',
  '/BarGuide/images/bottles/singleton-12.jpg',
  '/BarGuide/images/bottles/talisker-10.jpg',
  '/BarGuide/images/bottles/taoscan.webp',
  '/BarGuide/images/bottles/van-winkle-12.webp',
  '/BarGuide/images/bottles/wathens.jpg',
  '/BarGuide/images/bottles/westland-sherry-wood.webp',
  '/BarGuide/images/bottles/whistlepig-10.jpg',
  '/BarGuide/images/bottles/whistlepig-12.jpg',
  '/BarGuide/images/bottles/whistlepig-15.jpg',
  '/BarGuide/images/bottles/whistlepig-farmstock.jpg',
  '/BarGuide/images/bottles/willett-pot-still.png',
  '/BarGuide/images/bottles/william-larue-weller.jpg',
  '/BarGuide/images/bottles/woodford-reserve.jpg',
  '/BarGuide/images/bottles/woodford-reserve-rye.jpg',
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
  const { pathname } = new URL(e.request.url);

  // Network-first for the HTML shell — always fetch fresh when online,
  // fall back to cache only when offline.
  if (pathname === '/BarGuide/' || pathname === '/BarGuide/index.html') {
    e.respondWith(
      fetch(e.request)
        .then(res => {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
          return res;
        })
        .catch(() => caches.match(e.request))
    );
    return;
  }

  // Cache-first for all static assets (images, icons, manifest).
  e.respondWith(
    caches.match(e.request)
      .then(cached => cached || fetch(e.request))
      .catch(() => caches.match('/BarGuide/index.html'))
  );
});
