# Alligator Guide — Project Brief

Staff bar reference app for **House of Louie / The Alligator Bar** (London).
PWA, offline-first, single HTML file. Live at: **https://zero970.github.io/AlligatorGuide**

---

## Stack & deployment

- **Single file**: `D:\Claude\whisky-guide\index.html` (~5100 lines, no bundler, no framework)
- **Assets**: `images/bottles/`, `images/bottles_cards/`, `images/Cocktails/`, `alligator.svg`, `icons/`
- **PWA**: `manifest.json` + `sw.js` (service worker, cache-first for assets, network-first for HTML)
- **Deployed**: GitHub Pages → `https://github.com/ZerO970/AlligatorGuide`
- **SW cache key**: timestamped (`alligator-guide-YYYYMMDD-HHMM`) — bump on every push so clients update:
  ```bash
  VERSION=$(date +"%Y%m%d-%H%M") && sed -i "s|const CACHE = 'alligator-guide-[^']*'|const CACHE = 'alligator-guide-${VERSION}'|" sw.js
  ```

---

## File structure inside `index.html`

| Lines (approx) | Content |
|---|---|
| 1–16 | `<head>`, fonts, no-flash script |
| 17–1190 | `<style>` — all CSS (tokens, components, themes, responsive) |
| 1191–1420 | `<body>` HTML — header, onboarding overlay, screens track, modal, compare bar |
| 1421–3185 | `<script>` — data: `WHISKIES[]`, `CATEGORIES{}`, `COCKTAILS[]`, `TRIVIA[]`, `CARLOS_COCKTAIL` |
| 3186–3600 | JS — state, lang, theme, nav, search, filters, category/bar render |
| 3600–3870 | JS — `openWhiskyModal()`, `openCocktailModal()`, `openModal()` / `closeModal()` |
| 3870–4040 | JS — trivia: `triviaState`, `triviaStart()`, `renderTriviaQ()`, `triviaAnswer()` |
| 4040–4215 | JS — quiz: `quizState`, `quizNext()`, `quizAnswer()` |
| 4215–4340 | JS — favourites (`favIds`, localStorage), `renderBar` patch |
| 4340–4430 | JS — `initSwipe()` — carousel drag, drum pill animation |
| 4430–4565 | JS — compare: `compareIds`, `syncCompareBar()`, `openCompareModal()` |
| 4565–5070 | JS — match (guest sommelier): `matchState`, `buildLadder()`, `renderMatchStep()` |
| 5070–5230 | JS — easter egg (`openCaimanModal()`), init (`renderCategories()`, `slideTrackTo()`) |
| 5230–5340 | JS — `initOnboarding()`, service worker registration |

---

## Screens & navigation

```
SCREEN_ORDER = ['bar', 'cocktails', 'quiz', 'match']
DOM IDs:      #screen-bar  #screen-cocktails  #screen-quiz  #screen-match
```

All 4 screens live side-by-side in `#screensTrack` (flex row, 400vw wide).
Navigation via `slideTrackTo(idx)` + `translateX`. Swipe handled by `initSwipe()`.
`navSetScreen(screen)` — main function to switch screens (resets scroll to top).

---

## Themes

4 themes cycle on theme button click:
`louie` (dark green) → `louie-light` (sage) → `dark` (charcoal) → `light` (cream)

Default: `data-theme="louie"` on `<html>`.

Alligator branding (logo, gator watermark) activates in `louie` and `louie-light` themes.
Fixed background gator: `.louie-gator-bg` div, `position:fixed`, `z-index:0`.

Color system: **OKLCH** throughout. Token variables defined per theme in CSS.

---

## Key data structures

### Whisky entry (in `WHISKIES[]`)
```js
{
  id: 'bulleit-rye',
  name: 'Bulleit Rye', brand: 'Bulleit',
  type: 'rye',                          // bourbon | rye | irish | scotch | japanese | ...
  typeLabel: { en: '...', ru: '...' },
  region: { en: '...', ru: '...' },
  abv: '45%', priceGbp: '£12.5', price: '££',
  balance: 'bold',                      // bold | approachable
  balanceLabel: { en: '...', ru: '...' },
  nose: { tags: { en: [...], ru: [...] } },
  palate: { spice: 4, malt: 2, fruit: 3, caramel: 2, oak: 3 }, // 1–5
  palateNotes: { en: '...', ru: '...' },
  finish: { notes: { en: [...], ru: [...] } },
  texture: { en: '...', ru: '...' },
  whenToRecommend: { en: '...', ru: '...' },
  cocktails: [{ name: '...', icon: '🍸', desc: { en: '...', ru: '...' } }],
  history: { en: '...', ru: '...' },
  img: 'images/bottles/bulleit-rye.jpg',   // card thumbnail
  imgVariant: 'a',                          // 'a' = portrait, 'b' = landscape
  imgPos: 'center top',                     // optional object-position override
  // imgCard auto-derived: replaces 'images/bottles/' → 'images/bottles_cards/'
}
```

### Cocktail entry (in `COCKTAILS[]`)
```js
{
  id: 'old-fashioned',
  name: 'Old Fashioned', icon: '🍊',
  tagline: { en: '...', ru: '...' },
  topWhiskies: ['knob-creek-bourbon', ...],   // up to 3 whisky IDs
  topReasons: { 'knob-creek-bourbon': { en: '...', ru: '...' } },
  history: { en: '...', ru: '...' },
  story: { en: '...', ru: '...' },            // optional bartender story
  spec: {
    en: { glass: '...', ingredients: [...], method: '...', garnish: '...' },
    ru: { ... }
  }
}
```

Cocktail image map: `COCKTAIL_IMG` object (id → filename in `images/Cocktails/`).

### Trivia question
```js
{ d: 1,           // difficulty: 1=easy, 2=medium, 3=hard
  q: '...',       // question EN
  qr: '...',      // question RU
  o: [...],       // options EN (4 strings)
  or: [...],      // options RU
  a: 2,           // correct answer INDEX in original o[] array
  e: '...',       // explanation EN
  er: '...' }     // explanation RU
```
Answers are shuffled on render via Fisher-Yates; `triviaState.correctIdx` tracks where correct landed.

---

## Modal system

Single modal: `#modalOverlay` > `#modalPanel` > `#modalBody`.
`openModal()` / `closeModal()` manage visibility + body scroll lock.
Content injected via `innerHTML` in `openWhiskyModal(w)`, `openCocktailModal(c)`, `openCompareModal()`.

**Whisky modal hero**: `images/bottles_cards/` + `object-fit: cover` via `.modal-hero-cocktail` class.
**Cocktail modal hero**: `images/Cocktails/` + `object-fit: cover`.
Both use `.modal-hero` structure: blurred bg div + img + gradient overlays + close/nav buttons.

Whisky modal has prev/next arrows + hero swipe to navigate within `lastRenderedList`.

---

## Onboarding

- **Splash** (`.onb-load`): plays **every launch** (~1.9s returning, ~3.2s first-time)
- **Coach tour** (`.onb-steps`, 3 tappable steps): **first launch only**
- Flag: `localStorage.getItem('ag_onboarded_v1')`
- To replay for testing: `window.replayOnboarding()` in console, or open in incognito

---

## Languages

Toggle EN ↔ RU via `setLang(l)`. Russian adds `lang-ru` class to `body`.
CSS: `[data-ru] { display: none }` / `body.lang-ru [data-en] { display: none }`.
All user-facing strings use `{ en: '...', ru: '...' }` objects, accessed via `t(obj)` helper.

---

## Common tasks

### Add a new whisky
1. Add entry to `WHISKIES[]` array (copy existing entry as template)
2. Add card image to `images/bottles/` (thumbnail shown on grid)
3. Add hero image to `images/bottles_cards/` (same filename — shown in modal)
4. Add both paths to `sw.js` ASSETS array
5. Bump SW cache version before pushing

### Add a new cocktail
1. Add entry to `COCKTAILS[]` array
2. Add photo to `images/Cocktails/`
3. Add mapping to `COCKTAIL_IMG` object (id → filename)
4. Add path to `sw.js` ASSETS array
5. Bump SW cache version

### Add trivia questions
Add objects to `TRIVIA[]` array. Keep `d:` honest (1/2/3). There are currently:
- d:1 → 42 questions, d:2 → 56, d:3 → 38 (all ≥10, safe to use any difficulty)

### Change default theme
Edit `data-theme="..."` on the `<html>` tag (line 2).
Cycle order defined in theme button JS: `louie → louie-light → dark → light`.

### Bump SW cache (required after every push)
```bash
VERSION=$(date +"%Y%m%d-%H%M") && sed -i "s|const CACHE = 'alligator-guide-[^']*'|const CACHE = 'alligator-guide-${VERSION}'|" sw.js
```

---

## Known issues / deferred

- **Favourites & Compare** — UI code exists but buttons aren't rendered on normal grid cards. Deferred by owner. Code is in `renderBar` patch (~line 4380) and `syncCompareBar()` (~line 4567).
- **Swipe doesn't init Quiz/Match** — `quizNext()` triggers on pill click only; if user swipes to quiz screen it's blank until they tap. Low priority, quick fix: call `quizNext()` inside `navSetScreen`.
- **Search is EN-only** — `renderBar()` searches `w.nose.tags.en` regardless of active language. Fix: also search `w.nose.tags[lang]`.
- **`alligator.svg` = 1.9MB** — large for an SVG (embedded raster inside). Safe to optimize.

---

## Owner

Bar: **House of Louie / The Alligator Bar**, London.
GitHub: `https://github.com/ZerO970/AlligatorGuide`
User email: wwwetal97@gmail.com
