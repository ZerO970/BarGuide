# Alligator Guide — Project Brief

Staff bar reference app for **House of Louie / The Alligator Bar** (London).
PWA, offline-first, single HTML file. Live at: **https://zero970.github.io/AlligatorGuide**

---

## Stack & deployment

- **Single file**: `D:\Claude\whisky-guide\index.html` (~7100 lines) — **работай здесь**
- **Assets**: `images/bottles/`, `images/bottles_cards/`, `images/Cocktails/`, `alligator.svg`, `icons/`
- **PWA**: `manifest.json` + `sw.js` (service worker, cache-first for assets, network-first for HTML)
- **Deployed**: GitHub Pages → `https://github.com/ZerO970/AlligatorGuide`
- **SW cache key**: timestamped (`alligator-guide-YYYYMMDD-HHMM`) — bump on every push so clients update:
  ```bash
  VERSION=$(date +"%Y%m%d-%H%M") && sed -i "s|const CACHE = 'alligator-guide-[^']*'|const CACHE = 'alligator-guide-${VERSION}'|" sw.js
  ```

---

## File structure inside `index.html` (~7300 lines)

| Lines (approx) | Content |
|---|---|
| 1–16 | `<head>`, fonts, no-flash script |
| 17–1200 | `<style>` — all CSS |
| 1200–1450 | `<body>` HTML |
| 1450–3450 | `<script>` data: `WHISKIES[]` (74), `RUMS[]` (21), `COGNACS[]` (5), `ARMAGNACS[]`, `VODKAS[]` (8), `GINS[]` (8), `TEQUILAS[]` (15), `MEZCALS[]` (3), `ABSINTHES[]` |
| 3450–3730 | `COCKTAILS[]` — 67 коктейлей (whisky×20, gin×13, tequila×10, rum×10, vodka×8, cognac×6) |
| 3730–4000 | `CATEGORIES{}`, `SPIRIT_TYPES[]`, `MAIN_MENU[]`, `COCKTAIL_IMG{}`, `TRIVIA[]` |
| 4000–4250 | JS — state, lang, theme, nav |
| 4250–4750 | JS — `renderAllSpiritsGrid()`, `renderGenericSpiritGrid()`, `openSpiritModal()`, `renderBar()` |
| 4750–5550 | JS — `findSpirit()`, `renderCocktails()`, `openWhiskyModal()` |
| 5550–5800 | JS — `openCocktailModal()` |
| 5800–end | JS — trivia, quiz, match, favourites, compare, onboarding |

---

## Screens & navigation

```
SCREEN_ORDER = ['event', 'bar', 'cocktails', 'on-the-menu', 'quiz', 'match']
DOM IDs:      #screen-event  #screen-bar  #screen-cocktails  #screen-on-the-menu  #screen-quiz  #screen-match
```

All 6 screens live side-by-side in `#screensTrack` (flex row, 600vw wide).
Navigation via `slideTrackTo(idx)` + `translateX`. Swipe handled by `initSwipe()`.
`navSetScreen(screen, keepContext)` — main function to switch screens. `keepContext=true` on swipe-back (preserves spirit view state).

### Nav pill buttons (order in DOM)
| Button | Behaviour |
|---|---|
| **Main** (`id="navMainBtn"`) | `goMainHome()` → shows 4-card main home |
| **Event** (`data-screen="event"`) | only visible when event is active; amber dot animation |
| **Alcohol** (`data-screen="bar"`) | `navSetScreen('bar')` → shows spirit type selector |
| Cocktails / On the Menu / Quiz / Match | `navSetScreen(screen)` as usual |

### Bar screen internal views (all inside `#screen-bar`)
Navigation between views is DOM-based (hidden/shown), not screen-slide based.

```
mainHome (#mainHome)          ← goMainHome() lands here
  └─ click Alcohol card
spiritHome (#spiritHome)      ← navSetScreen('bar') via Alcohol nav lands here
  └─ click a spirit type
  [whisky]  → catHome (#catHome) → catDetail (#catDetail) → whiskeyGrid
  [others]  → whiskeyGrid directly + spiritBackWrap (← Spirits button)
```

Key functions:
- `goMainHome()` — go to 4-card home, highlights Main in nav
- `enterSpiritType()` — show spiritHome (spirit type list)
- `exitSpiritType()` — back to mainHome, highlights Main in nav
- `enterSpirit(id)` — drill into a specific spirit category
- `exitSpirit()` — back to spiritHome, highlights Alcohol in nav
- `spiritBackWrap` (`<div id="spiritBackWrap">`) — block wrapper for the dynamic "← Spirits" back button (fixes left-drift on desktop)

---

## Events screen (`#screen-event`)

Appears in nav only when `isEventActiveToday()` returns true (checks `EVENT_DATA.dateStart`/`dateEnd` against today).

### EVENT_DATA structure
```js
window.EVENT_DATA = {
  active: true,
  title: 'London Essence',          // shown as <em> in hero
  dateStart: '2026-06-12',
  dateEnd: '2026-09-30',
  items: [/* cocktail objects, same shape as COCKTAILS[] */]
};
```
Rendered by `initEventScreen()` on page load. Nav button pulses with amber dot animation (`.nav-event-btn.event-active::before`).

### Sponsor logos
Below the event cocktail grid, `.event-sponsors` section shows partner brands:
- **London Essence Co.** — inline SVG monogram (LE mark, `fill="currentColor"`)
- **Palmarae** — inline SVG wordmark sourced from palmarae.com (`fill="currentColor"`)

Both logos adapt to all 4 themes via `color: var(--text-secondary)`.

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
  baseSpirit: 'whisky',                        // 'whisky'|'gin'|'tequila'|'rum'|'vodka'|'cognac'
  tagline: { en: '...', ru: '...' },
  topWhiskies: ['knob-creek-bourbon', ...],    // up to 3 spirit IDs (any category, not just whisky)
  topReasons: { 'knob-creek-bourbon': { en: '...', ru: '...' } },
  history: { en: '...', ru: '...' },
  story: { en: '...', ru: '...' },             // optional bartender story
  spec: {
    en: { glass: '...', ingredients: [...], method: '...', garnish: '...' },
    ru: { ... }
  }
}
```

**67 cocktails total**: whisky×20, gin×13, tequila×10, rum×10, vodka×8, cognac×6.

Cocktail image map: `COCKTAIL_IMG` object (id → filename in `images/Cocktails/`).
Cocktails without image fall back to `c.icon` (emoji) automatically.

### activeSpirit & filtering
```
let activeSpirit = null;  // set when user enters a spirit section
```
- `renderCocktails()` filters `COCKTAILS` by `c.baseSpirit === activeSpirit` when set
- Set in the spirit section entry function; reset to `null` on back-to-home
- `findSpirit(id)` — searches ALL spirit arrays (WHISKIES, GINS, TEQUILAS, RUMS, VODKAS, COGNACS, MEZCALS, ARMAGNACS) — use instead of `WHISKIES.find` anywhere spirits from multiple categories may appear

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

### Add a new whisky / spirit
1. Add entry to the correct array: `WHISKIES[]`, `GINS[]`, `TEQUILAS[]`, `RUMS[]`, `VODKAS[]`, `COGNACS[]`, `MEZCALS[]`
2. Add card image to `images/bottles/` + hero to `images/bottles_cards/`
3. Add both paths to `sw.js` ASSETS array
4. Bump SW cache version before pushing

### Add a new cocktail
1. Add entry to `COCKTAILS[]` — include `baseSpirit` field
2. `topWhiskies` = up to 3 IDs from ANY spirit array matching the cocktail's category
3. Add photo to `images/Cocktails/` + mapping to `COCKTAIL_IMG` (no image = emoji fallback, that's fine)
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


---

## Owner

Bar: **House of Louie / The Alligator Bar**, London.
GitHub: `https://github.com/ZerO970/AlligatorGuide`
User email: wwwetal97@gmail.com
