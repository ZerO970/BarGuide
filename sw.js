const CACHE = 'alligator-guide-20260624-0439';
const ASSETS = [
  '/AlligatorGuide/',
  '/AlligatorGuide/index.html',
  '/AlligatorGuide/manifest.json',
  '/AlligatorGuide/alligator.svg',
  '/AlligatorGuide/icons/icon-192.png',
  '/AlligatorGuide/icons/icon-512.png',
  '/AlligatorGuide/images/bottles/ardbeg-uigeadail.jpg',
  '/AlligatorGuide/images/bottles/ardbeg-wee-beastie.avif',
  '/AlligatorGuide/images/bottles/balvenie-portwood-21.webp',
  '/AlligatorGuide/images/bottles/bernheim.jpg',
  '/AlligatorGuide/images/bottles/blantons-gold.webp',
  '/AlligatorGuide/images/bottles/bower-hill-rye.jpg',
  '/AlligatorGuide/images/bottles/bowmore-12.webp',
  '/AlligatorGuide/images/bottles/buffalo-trace.webp',
  '/AlligatorGuide/images/bottles/bulleit-bourbon.png',
  '/AlligatorGuide/images/bottles/bulleit-bourbon-10.jpg',
  '/AlligatorGuide/images/bottles/bulleit-rye.jpg',
  '/AlligatorGuide/images/bottles/clynelish-14.webp',
  '/AlligatorGuide/images/bottles/dalmore-king-alexander.webp',
  '/AlligatorGuide/images/bottles/elijah-craig.webp',
  '/AlligatorGuide/images/bottles/evan-williams.jpg',
  '/AlligatorGuide/images/bottles/gentleman-jack.webp',
  '/AlligatorGuide/images/bottles/glenfiddich-18.webp',
  '/AlligatorGuide/images/bottles/glenfiddich-21.jpg',
  '/AlligatorGuide/images/bottles/glenfiddich-grand-cru.avif',
  '/AlligatorGuide/images/bottles/glenfiddich-grande-couronne.jpg',
  '/AlligatorGuide/images/bottles/highland-park-dark-origins.jpg',
  '/AlligatorGuide/images/bottles/hudson-rye.webp',
  '/AlligatorGuide/images/bottles/jameson-black-barrel.webp',
  '/AlligatorGuide/images/bottles/jd-single-barrel-rye.webp',
  '/AlligatorGuide/images/bottles/jim-beam-rye.webp',
  '/AlligatorGuide/images/bottles/johnny-drum.webp',
  '/AlligatorGuide/images/bottles/jw-black-label.webp',
  '/AlligatorGuide/images/bottles/jw-blue-label.webp',
  '/AlligatorGuide/images/bottles/knob-creek-bourbon.jpg',
  '/AlligatorGuide/images/bottles/knob-creek-rye.webp',
  '/AlligatorGuide/images/bottles/lagavulin-16.jpg',
  '/AlligatorGuide/images/bottles/laphroaig-quarter-cask.jpg',
  '/AlligatorGuide/images/bottles/michters-10yr-bourbon.jpg',
  '/AlligatorGuide/images/bottles/michters-10yr-rye.webp',
  '/AlligatorGuide/images/bottles/michters-bourbon.jpg',
  '/AlligatorGuide/images/bottles/michters-rye.webp',
  '/AlligatorGuide/images/bottles/michters-sour-mash.jpg',
  '/AlligatorGuide/images/bottles/nikka-from-the-barrel.webp',
  '/AlligatorGuide/images/bottles/noahs-mill.jpg',
  '/AlligatorGuide/images/bottles/oban-14.webp',
  '/AlligatorGuide/images/bottles/old-crow.webp',
  '/AlligatorGuide/images/bottles/old-rip-van-winkle.jpg',
  '/AlligatorGuide/images/bottles/rabbit-hole-bourbon.jpg',
  '/AlligatorGuide/images/bottles/rabbit-hole-rye.png',
  '/AlligatorGuide/images/bottles/rittenhouse-rye.jpg',
  '/AlligatorGuide/images/bottles/roe-and-co.jpg',
  '/AlligatorGuide/images/bottles/rowans-creek.webp',
  '/AlligatorGuide/images/bottles/sazerac-rye.jpg',
  '/AlligatorGuide/images/bottles/singleton-12.jpg',
  '/AlligatorGuide/images/bottles/talisker-10.jpg',
  '/AlligatorGuide/images/bottles/taoscan.webp',
  '/AlligatorGuide/images/bottles/van-winkle-12.webp',
  '/AlligatorGuide/images/bottles/wathens.jpg',
  '/AlligatorGuide/images/bottles/westland-sherry-wood.webp',
  '/AlligatorGuide/images/bottles/whistlepig-10.jpg',
  '/AlligatorGuide/images/bottles/whistlepig-12.jpg',
  '/AlligatorGuide/images/bottles/whistlepig-15.jpg',
  '/AlligatorGuide/images/bottles/whistlepig-farmstock.jpg',
  '/AlligatorGuide/images/bottles/willett-pot-still.png',
  '/AlligatorGuide/images/bottles/william-larue-weller.jpg',
  '/AlligatorGuide/images/bottles/woodford-reserve.jpg',
  '/AlligatorGuide/images/bottles/woodford-reserve-rye.jpg',
  '/AlligatorGuide/images/bottles_cards/ardbeg-uigeadail.jpg',
  '/AlligatorGuide/images/bottles_cards/ardbeg-wee-beastie.avif',
  '/AlligatorGuide/images/bottles_cards/balvenie-portwood-21.webp',
  '/AlligatorGuide/images/bottles_cards/bernheim.jpg',
  '/AlligatorGuide/images/bottles_cards/blantons-gold.webp',
  '/AlligatorGuide/images/bottles_cards/bower-hill-rye.jpg',
  '/AlligatorGuide/images/bottles_cards/bowmore-12.webp',
  '/AlligatorGuide/images/bottles_cards/buffalo-trace.webp',
  '/AlligatorGuide/images/bottles_cards/bulleit-bourbon.png',
  '/AlligatorGuide/images/bottles_cards/bulleit-bourbon-10.jpg',
  '/AlligatorGuide/images/bottles_cards/bulleit-rye.jpg',
  '/AlligatorGuide/images/bottles_cards/clynelish-14.webp',
  '/AlligatorGuide/images/bottles_cards/dalmore-king-alexander.webp',
  '/AlligatorGuide/images/bottles_cards/elijah-craig.webp',
  '/AlligatorGuide/images/bottles_cards/evan-williams.jpg',
  '/AlligatorGuide/images/bottles_cards/gentleman-jack.webp',
  '/AlligatorGuide/images/bottles_cards/glenfiddich-18.webp',
  '/AlligatorGuide/images/bottles_cards/glenfiddich-21.jpg',
  '/AlligatorGuide/images/bottles_cards/glenfiddich-grand-cru.avif',
  '/AlligatorGuide/images/bottles_cards/glenfiddich-grande-couronne.jpg',
  '/AlligatorGuide/images/bottles_cards/highland-park-dark-origins.jpg',
  '/AlligatorGuide/images/bottles_cards/hudson-rye.webp',
  '/AlligatorGuide/images/bottles_cards/jameson-black-barrel.webp',
  '/AlligatorGuide/images/bottles_cards/jd-single-barrel-rye.webp',
  '/AlligatorGuide/images/bottles_cards/jim-beam-rye.webp',
  '/AlligatorGuide/images/bottles_cards/johnny-drum.webp',
  '/AlligatorGuide/images/bottles_cards/jw-black-label.webp',
  '/AlligatorGuide/images/bottles_cards/jw-blue-label.webp',
  '/AlligatorGuide/images/bottles_cards/knob-creek-bourbon.jpg',
  '/AlligatorGuide/images/bottles_cards/knob-creek-rye.webp',
  '/AlligatorGuide/images/bottles_cards/lagavulin-16.jpg',
  '/AlligatorGuide/images/bottles_cards/laphroaig-quarter-cask.jpg',
  '/AlligatorGuide/images/bottles_cards/michters-10yr-bourbon.jpg',
  '/AlligatorGuide/images/bottles_cards/michters-10yr-rye.webp',
  '/AlligatorGuide/images/bottles_cards/michters-bourbon.jpg',
  '/AlligatorGuide/images/bottles_cards/michters-rye.webp',
  '/AlligatorGuide/images/bottles_cards/michters-sour-mash.jpg',
  '/AlligatorGuide/images/bottles_cards/nikka-from-the-barrel.webp',
  '/AlligatorGuide/images/bottles_cards/noahs-mill.jpg',
  '/AlligatorGuide/images/bottles_cards/oban-14.webp',
  '/AlligatorGuide/images/bottles_cards/old-crow.webp',
  '/AlligatorGuide/images/bottles_cards/old-rip-van-winkle.jpg',
  '/AlligatorGuide/images/bottles_cards/rabbit-hole-bourbon.jpg',
  '/AlligatorGuide/images/bottles_cards/rabbit-hole-rye.png',
  '/AlligatorGuide/images/bottles_cards/rittenhouse-rye.jpg',
  '/AlligatorGuide/images/bottles_cards/roe-and-co.jpg',
  '/AlligatorGuide/images/bottles_cards/rowans-creek.webp',
  '/AlligatorGuide/images/bottles_cards/sazerac-rye.jpg',
  '/AlligatorGuide/images/bottles_cards/singleton-12.jpg',
  '/AlligatorGuide/images/bottles_cards/talisker-10.jpg',
  '/AlligatorGuide/images/bottles_cards/taoscan.webp',
  '/AlligatorGuide/images/bottles_cards/thomas-h-handy.webp',
  '/AlligatorGuide/images/bottles_cards/van-winkle-12.webp',
  '/AlligatorGuide/images/bottles_cards/wathens.jpg',
  '/AlligatorGuide/images/bottles_cards/westland-sherry-wood.webp',
  '/AlligatorGuide/images/bottles_cards/whistlepig-10.jpg',
  '/AlligatorGuide/images/bottles_cards/whistlepig-12.jpg',
  '/AlligatorGuide/images/bottles_cards/whistlepig-15.jpg',
  '/AlligatorGuide/images/bottles_cards/whistlepig-farmstock.jpg',
  '/AlligatorGuide/images/bottles_cards/willett-pot-still.png',
  '/AlligatorGuide/images/bottles_cards/william-larue-weller.jpg',
  '/AlligatorGuide/images/bottles_cards/woodford-reserve.jpg',
  '/AlligatorGuide/images/bottles_cards/woodford-reserve-rye.jpg',
  '/AlligatorGuide/images/Cocktails/Old_fashioned.jpg',
  '/AlligatorGuide/images/Cocktails/Manhattan.jpg',
  '/AlligatorGuide/images/Cocktails/Whisky Sour.jpg',
  '/AlligatorGuide/images/Cocktails/Highball.jpg',
  '/AlligatorGuide/images/Cocktails/Penicillin.webp',
  '/AlligatorGuide/images/Cocktails/Boulevardier.webp',
  '/AlligatorGuide/images/Cocktails/Hot Toddy.jpg',
  '/AlligatorGuide/images/Cocktails/Rob Roy.jpg',
  '/AlligatorGuide/images/Cocktails/Paper Plane.jpg',
  '/AlligatorGuide/images/Cocktails/Gold Rush.jpg',
  '/AlligatorGuide/images/Cocktails/Mint Julep.jpg',
  '/AlligatorGuide/images/Cocktails/Vieux Carré.jpg',
  '/AlligatorGuide/images/Cocktails/Sazerac.avif',
  '/AlligatorGuide/images/Cocktails/Whisky Mule.webp',
  '/AlligatorGuide/images/Cocktails/Jameson, Ginger & Lime.avif',
  '/AlligatorGuide/images/ui/card-alcohol.webp',
  '/AlligatorGuide/images/ui/card-cocktails.webp',
  '/AlligatorGuide/images/ui/card-menu.jpg',
  '/AlligatorGuide/images/ui/card-menu-dark.svg',
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
  if (pathname === '/AlligatorGuide/' || pathname === '/AlligatorGuide/index.html') {
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
      .catch(() => caches.match('/AlligatorGuide/index.html'))
  );
});
