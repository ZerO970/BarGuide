# Alligator Guide — Project Brief

Staff bar reference app for **House of Louie / The Alligator Bar** (London).
PWA, offline-first, single HTML file. Live at: **https://zero970.github.io/AlligatorGuide**

---

## Stack & deployment

- **Single file**: `D:\Claude\whisky-guide\index.html` (~9300 lines) — **работай здесь**
- **Assets**: `images/bottles/`, `images/bottles_cards/`, `images/Cocktails/`, `alligator.svg`, `icons/`
- **PWA**: `manifest.json` + `sw.js` (service worker, cache-first for assets, network-first for HTML)
- **Deployed**: GitHub Pages → `https://github.com/ZerO970/AlligatorGuide`
- **SW cache key**: timestamped (`alligator-guide-YYYYMMDD-HHMM`) — bump on every push so clients update:
  ```bash
  VERSION=$(date +"%Y%m%d-%H%M") && sed -i "s|const CACHE = 'alligator-guide-[^']*'|const CACHE = 'alligator-guide-${VERSION}'|" sw.js
  ```

---

## File structure inside `index.html` (~9300 lines)

| Lines (approx) | Content |
|---|---|
| 1–16 | `<head>`, fonts, no-flash script |
| 17–1940 | `<style>` — all CSS |
| 1940–2374 | `<body>` HTML — 8 screens + overlays (manager updates, flavor wheel) |
| 2375–4188 | `<script>` data: `WHISKIES[]` (74), `RUMS[]` (21), `COGNACS[]` (5), `ARMAGNACS[]`, `VODKAS[]` (8), `GINS[]` (8), `TEQUILAS[]` (15), `MEZCALS[]` (3), `ABSINTHES[]` |
| 4189–5290 | `COCKTAILS[]` — 67 коктейлей (whisky×20, gin×13, tequila×10, rum×10, vodka×8, cognac×6) |
| 5291–5556 | `COCKTAIL_FLAVOR_PROFILES{}`, `DAILY_SPECIALS[]`, `WEEKLY_TASKS{}`, `CHECKLISTS{}`, `MANAGER_UPDATES[]` |
| 5557–5900 | `CATEGORIES{}`, `SPIRIT_TYPES[]`, `MAIN_MENU[]`, `COCKTAIL_IMG{}`, `TRIVIA[]`, `EVENT_DATA` |
| 5900–6550 | JS — state, lang, theme, nav, `renderFood()` dispatch |
| 6550–7080 | JS — `renderAllSpiritsGrid()`, `renderGenericSpiritGrid()`, `openSpiritModal()`, `renderBar()` |
| 7080–7215 | JS — Flavor Wheel: `buildFlavorWheel()`, `openFlavorWheel()`, `fwToggle()`, `applyFlavorFilter()` |
| 7215–8015 | JS — `findSpirit()`, `renderCocktails()`, `openWhiskyModal()` |
| 8015–8210 | JS — swipe navigation `initSwipe()` |
| 8210–9115 | JS — compare, trivia, quiz, match, favourites, onboarding |
| 9115–end | JS — checklist: `renderChecklist()`, `resetChecklist()`, `openFoodModal()`, `renderFood()` |

---

## Screens & navigation

```
SCREEN_ORDER = ['event', 'bar', 'cocktails', 'on-the-menu', 'quiz', 'match', 'food', 'checklist']
DOM IDs:      #screen-event  #screen-bar  #screen-cocktails  #screen-on-the-menu  #screen-quiz  #screen-match  #screen-food  #screen-checklist
```

All 8 screens live side-by-side in `#screensTrack` (flex row, **800vw** wide).
Navigation via `slideTrackTo(idx)` + `translateX`. Swipe handled by `initSwipe()`.
`navSetScreen(screen, keepContext)` — main function to switch screens. `keepContext=true` on swipe-back (preserves spirit view state).

**Event screen is NOT in the swipe chain** — `minIdx()` always returns `1` (bar). Event is accessible only via its nav button.

### Nav pill buttons (order in DOM)
| Button | Behaviour |
|---|---|
| **Main** (`id="navMainBtn"`) | `goMainHome()` → shows 4-card main home |
| **Event** (`data-screen="event"`) | only visible when event is active; amber dot animation; nav-button-only (not swipeable) |
| **Alcohol** (`data-screen="bar"`) | `navSetScreen('bar')` → shows spirit type selector |
| Cocktails / On the Menu / Quiz / Match | `navSetScreen(screen)` as usual |
| **Food** (`data-screen="food"`) | `navSetScreen('food')` → food menu screen |
| **Checklist** (`data-screen="checklist"`) | `navSetScreen('checklist')` → shift checklist screen |

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
  title: 'London Essence',
  dateStart: '2026-06-12',
  dateEnd: '2026-08-31',
  items: [/* cocktail objects — same shape as COCKTAILS[], plus img: 'images/events/...' */]
};
```
Each item can have `img` field pointing to `images/events/` → shown as hero in modal and as `.ccard` image.

Rendered by `initEventScreen()`. Event grid uses `.ccard` components (not simple `.cocktail-card`).
Nav button: amber dot `::before` animation instead of opacity flash.

### Riviera modal
When opening an event cocktail, `#modalPanel` gets class `.modal-riviera` → `repeating-conic-gradient` radial sunburst pattern in teal (8% opacity). Removed on `closeModal()`.

### Sponsor logos
`.event-sponsors` section below the grid — "In partnership with":
- **London Essence Co.** — inline SVG LE monogram (`fill="currentColor"`)
- **Palmarae** — inline SVG wordmark from palmarae.com (`fill="currentColor"`)

---

## Flavor Wheel (`#fwOverlay`)

Circular SVG filter on the cocktails screen. Opens from the `🎨 Flavor` button in the filter row.

```js
FLAVOR_DIMS = [
  { key:'sweet', emoji:'🍬', en:'Sweet',   ru:'Сладкий',   color:'#f59e0b' },
  { key:'fruity', ... }, { key:'spicy', ... }, { key:'smoky', ... },
  { key:'bitter', ... }, { key:'sour',  ... }, { key:'floral', ... }, { key:'creamy', ... },
]

COCKTAIL_FLAVOR_PROFILES = {
  'old-fashioned': { sweet:4, sour:0, bitter:3, smoky:1, spicy:2, fruity:2, floral:0, creamy:0 },
  // … 67 cocktails total, scores 0–5
}
```

Filter threshold: score **≥ 3** to match. `flavorFilter[]` is the active state; applied in `renderCocktails()`.

Key functions: `openFlavorWheel()`, `closeFlavorWheel()`, `fwToggle(key)`, `applyFlavorFilter()`, `clearFlavorFilter()`, `fwRemoveOne(key)`, `fwUpdateBtn()`.
Active chips shown in `#fwActiveRow` / `#fwActiveChips` (below filter row). `#flavorWheelBtn` gets `.fw-active` class when filter is on.

---

## Daily Special card (main home)

`DAILY_SPECIALS[]` — 7 entries, one per day of week (`dayOfWeek: 0=Sun…6=Sat`). Can also use `date: 'YYYY-MM-DD'` for one-offs.

```js
{ dayOfWeek: 1, type: 'cocktail', refId: 'boulevardier',
  title: { en: 'Boulevardier Monday', ru: 'Понедельничный Boulevardier' },
  desc:  { en: '...', ru: '...' } }
```

`type` is always `'cocktail'` for now; `refId` must match an ID in `COCKTAILS[]` (or `FOOD[]` if `type:'food'`).
Rendered as a card on the main home screen; click opens the relevant cocktail/food modal.

---

## Food Menu screen (`#screen-food`)

Real House of Louie menu (Summer 26 Food Bible). **32 dishes.**

```js
FOOD = [
  { id: 'cote-de-boeuf', name: 'Côte de Boeuf (1kg)', emoji: '🍖', category: 'main', price: '£125',
    description: { en: '...', ru: '...' },
    foh: { en: '...', ru: '...' },            // FOH talking point — staff selling line, shown in modal
    allergens: ['milk', 'sulphites'],         // string array
    tags: { en: ['meat','sharing'], ru: ['мясо','на стол'] },
    pairings: ['old-fashioned', 'boulevardier'],  // cocktail IDs from COCKTAILS[]
    wine: { en: 'Cissac or Domaine La Solitude', ru: '...' }  // sommelier note from venue wine list
  },
  // …
]
```

Categories: `'snack'` | `'starter'` | `'main'` | `'side'` | `'dessert'`.
Food has no images — uses `emoji` field (`f.img` optional, falls back to emoji).
Filter tabs are a fixed list in `renderFood()` (all/snack/starter/main/side/dessert), not derived from data.
`openFoodModal(f)` uses the main `#modalOverlay`; renders Description, Allergens, **💬 Talking Point** (`foh`), **🍷 Wine Pairing** (`wine`), **🍸 Cocktail Pairing** (`pairings`). Empty `foh`/`wine`/`pairings` sections are omitted; empty `price` is omitted.

Wine list available at venue (for `wine` field): White — Saline, Sancerre, Riesling, Saint Véran. Red — Domaine La Solitude, Cissac, Saboteur, Etna Judeka. Rosé — Rock Angel. Champagne — Ruinart Brut, Ruinart Blanc de Blancs, Veuve Clicquot Rosé. Sparkling/NA — Saicho jasmine tea, French Bloom.

Some dishes have no listed price in the source PDF (melon-soup, tomato-burrata, fennel-quinoa, miso-aubergine, sea-bass-provencal) — `price: ''`, render guards it.

### Add a food dish
1. Add entry to `FOOD[]` — `id`, `name`, `emoji`, `category`, `price`, `description` required; `foh`/`tags`/`pairings`/`wine` optional
2. `pairings` must be valid IDs from `COCKTAILS[]`; `wine` is free text from the venue wine list
3. If adding a new `category`, also add a tab to the `categories` array in `renderFood()`
4. No images needed (emoji fallback)

---

## Shift Checklist screen (`#screen-checklist`)

```js
CHECKLISTS = {
  manager:   { opening: [{id, task:{en,ru}}, ...], during: [...], closing: [...] },
  bartender: { opening: [...], during: [...], closing: [...] },
  waiter:    { opening: [...], during: [...], closing: [...] },
}

WEEKLY_TASKS = { 0: {en,ru}, 1: {en,ru}, … 6: {en,ru} }  // keyed by dayOfWeek (0=Sun)
```

State persisted in `localStorage`:
- `ag_checklist_v1` — `{ date: 'YYYY-MM-DD', checked: { itemId: true } }` — resets when date changes
- `ag_checklist_role` — last selected role (`'manager'|'bartender'|'waiter'`)
- `ag_checklist_shift` — last selected shift (`'opening'|'during'|'closing'`)

Key functions: `renderChecklist()`, `resetChecklist()`.
Progress bar updates on every item toggle.

---

## Manager Updates overlay (`#updatesOverlay`)

```js
MANAGER_UPDATES = [
  { id: 'upd-1', date: '2026-06-26', tag: 'urgent',
    title: { en: '...', ru: '...' },
    body:  { en: '...', ru: '...' } },
  // …
]
```

Tags: `'urgent'` | `'menu'` | `'info'`.
`#navUpdatesBadge` pill shows count of unread. Seen IDs stored in `localStorage ag_updates_v1`.
Key functions: `openUpdates()`, `renderUpdates()`.

### Update manager messages
Edit `MANAGER_UPDATES[]` directly. Add new entries at the top (they render in order). Remove old ones when stale. Badge auto-resets for returning users who haven't seen the new IDs.

---

## NEW badge system

Spirits with `addedAt: "YYYY-MM-DD"` field show NEW badges for 14 days after that date.

```js
isNew(item)          // true if addedAt within 14 days
isSeen(id)           // checks localStorage ag_seen_v1 (Set of IDs)
markSeen(id)         // called in openWhiskyModal + openSpiritModal
updateNewBadges()    // updates nav Alcohol badge count + rerenders spiritHome
```

- **Nav**: `#navAlcoholBadge` shows unseen new count (red pill)
- **Spirit type list**: per-category `NEW N` badge replaces the `›` arrow
- **Spirit cards**: gold border + `NEW` badge replaces balance label
- **localStorage key**: `ag_seen_v1` (JSON array of seen IDs)

---

## Themes

2 themes cycle on theme button click (the generic `dark`/`light` themes were removed):
`louie` (dark green) → `louie-light` (sage)

Default: `data-theme="louie"` on `<html>`.
**Persisted**: saved to `localStorage` as `ag_theme`. No-flash inline `<script>` in `<head>` restores it before CSS renders, and **migrates legacy values** (`dark`→`louie`, `light`→`louie-light`) so returning users aren't stranded on a removed theme.

**Theme crossfade ("light switch"):** main-home cards stack two `<img>` (`.card-photo--dark` + `.card-photo--light`); on theme change the photos crossfade via opacity (2880ms) while bg/header/nav transition via the `theme-transitioning` class (1800ms). `.main-card` uses `isolation:isolate` + `translateZ(0)` to keep gradient/badges glued during the fade (iOS Safari compositing fix). `prefers-reduced-motion` disables both.

Alligator branding (logo, gator watermark) activates in `louie` and `louie-light` themes.
Fixed background gator: `.louie-gator-bg` div, `position:fixed`, `z-index:0`.

Color system: **OKLCH** throughout. Token variables defined per theme in CSS.

### Splash screen (onboarding)
Light themes (`louie-light`, `light`) get a separate CSS variant: sage-to-cream gradient, alligator in dark forest green (`mix-blend-mode: multiply`). Selectors: `[data-theme="louie-light"] .onb`, `[data-theme="light"] .onb`.

### Theme-switching card images (`MAIN_MENU`)
Cards support `photo` as either a string (all themes) or an object keyed by theme name:
```js
photo: {
  louie: 'images/ui/card-alcohol.webp',      // dark night version
  dark:  'images/ui/card-alcohol.webp',
  'louie-light': 'images/ui/card-alcohol-light.jpg',  // bright day version
  light: 'images/ui/card-alcohol-light.jpg'
}
```
Current day/night pairs in `images/ui/`:
| Card | Dark | Light |
|---|---|---|
| Alcohol | `card-alcohol.webp` | `card-alcohol-light.jpg` |
| Cocktails | `card-cocktails.webp` | `card-cocktails-light.jpg` |
| On the Menu | `card-menu-dark.svg` (louie+dark) | `card-menu.jpg` (louie-light+light) |
| Events | `card-events.jpg` | `card-events-light.jpg` |

Cards also support `imgPos` (string, e.g. `'center 20%'`) → applied as inline `style="object-position:..."`.
`data-id="${item.id}"` on each `.main-card` div enables CSS targeting per card.
Mobile overrides in `@media (max-width: 640px)`: `[data-theme="louie"] [data-id="on-the-menu"]`, etc.

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
5. Add an entry to `COCKTAIL_FLAVOR_PROFILES` with 8 dimensions (sweet/sour/bitter/smoky/spicy/fruity/floral/creamy), scores 0–5
6. Bump SW cache version

### Add trivia questions
Add objects to `TRIVIA[]` array. Keep `d:` honest (1/2/3). There are currently:
- d:1 → 42 questions, d:2 → 56, d:3 → 38 (all ≥10, safe to use any difficulty)

### Change default theme
Edit `data-theme="..."` on the `<html>` tag (line 2).
Cycle order defined in theme button JS: `louie → louie-light` (2 active themes; `dark`/`light` removed but migration remains for legacy users).

### Bump SW cache (required after every push)
```bash
VERSION=$(date +"%Y%m%d-%H%M") && sed -i "s|const CACHE = 'alligator-guide-[^']*'|const CACHE = 'alligator-guide-${VERSION}'|" sw.js
```

---

## localStorage keys

| Key | Content |
|---|---|
| `ag_theme` | current theme (`louie` or `louie-light`) |
| `ag_seen_v1` | JSON array of spirit IDs seen by user (NEW badge system) |
| `ag_onboarded_v1` | `'1'` after first launch (coach tour) |
| `ag_checklist_v1` | `{ date: 'YYYY-MM-DD', checked: { itemId: true } }` |
| `ag_checklist_role` | last selected checklist role |
| `ag_checklist_shift` | last selected checklist shift |
| `ag_updates_v1` | JSON array of manager update IDs marked as read |
| `ag_favs_v1` | JSON array of favourited spirit IDs |
| `ag_compare_v1` | JSON array of spirit IDs in compare tray |

---

## Known issues / deferred

- **Favourites & Compare** — UI code exists but buttons aren't rendered on normal grid cards. Deferred by owner. `syncCompareBar()`/`openCompareModal()` still use `WHISKIES.find` (whisky-only) — switch to `findSpirit()` if the feature ever ships for multiple categories.
- ~~Food menu — placeholder content~~ — **done**: replaced with the real House of Louie Summer 26 menu (32 dishes, with `foh` talking points + `wine`/cocktail pairings). Photos not included (PDF images couldn't be extracted in-env; cards are emoji-based by design).
- ~~Swipe doesn't init Quiz/Match~~ — **fixed**: `navSetScreen` calls `quizNext()` when reaching the quiz screen.
- ~~Search is EN-only~~ — **fixed**: `renderBar()` search now includes `w.nose.tags[lang]` + EN fallback + `palateNotes[lang]`.
- ~~Event screen in swipe chain~~ — **fixed**: Event removed from swipe (`minIdx()` always returns 1); accessible via nav button only.


---

## Owner

Bar: **House of Louie / The Alligator Bar**, London.
GitHub: `https://github.com/ZerO970/AlligatorGuide`
User email: wwwetal97@gmail.com
