# Handoff: blog.uright.ai — uright Studio Jekyll/Chirpy theme

## Overview
A dark, IDE-inspired reskin of the **uright tech blog** (migrating from `uright.ca` → `blog.uright.ai`), aligned to the **uright Studio** product design system. The blog is presented as if it were the uright Studio desktop app: a fixed titlebar with the `uright · blog` wordmark and a `~/path` breadcrumb, a left **Explorer** panel (categories as folders, posts as a file-tree), the main reading panel, a contextual right rail (About / post Outline), and a bottom status bar.

The current site runs the stock **Chirpy** Jekyll theme (`jekyll-theme-chirpy`, dark mode). This handoff is the **target visual design** for that site. The job is to apply this look to the existing Chirpy install — not to replace Jekyll.

## About the design files
The file in this bundle — `Uright Blog Theme.dc.html` — is a **design reference created in HTML**. It is a prototype showing the intended look, layout, and behavior. **It is not production code to copy directly.**

The target codebase is the existing **Jekyll + Chirpy** site (`github.com/uright/uright.github.io`, branch `master`). Implement this design by **customizing Chirpy** using its established mechanisms:
- SCSS overrides in `_sass/` (Chirpy exposes theme variables and an overrides hook),
- layout/include overrides in `_layouts/` and `_includes/` (copy the gem's file into the repo to override it),
- `assets/css/jekyll-theme-chirpy.scss` as the stylesheet entry point.

Chirpy already provides post lists, pagination, categories, tags, archives, TOC, syntax highlighting (Rouge), and an About tab — so most of this is **restyling + light layout changes**, not new functionality. The IDE chrome (Explorer panel, Outline rail, titlebar, status bar) is the main net-new layout work; it can be built as Chirpy `_includes` partials + SCSS, or you may decide a custom layout wrapper is cleaner.

> The HTML prototype uses a small React-based component runtime to render — ignore that runtime entirely. Read it for **structure, exact tokens, copy, and measurements** only.

## Fidelity
**High-fidelity.** Final colors, typography, spacing, radii, and interactions are all specified below and embedded in the prototype as inline styles using CSS custom properties. Recreate pixel-faithfully using the token values in the **Design Tokens** section. All values come from the uright Studio design system (`_ds/` tokens, reproduced below).

---

## Design system foundation

All visual values derive from the **uright Studio** design system. The token CSS files are included in this bundle under `tokens/` (copied from the design system). Wire these values into Chirpy's SCSS variable layer rather than hardcoding hex where Chirpy already has a variable.

- **Type:** Geist (UI), Geist Mono (code, paths, identifiers, dates, tags, data). Load both (Google Fonts or self-hosted woff2).
- **Accent:** a single orange ramp, base `#f26a21`. Used sparingly — active nav/tab, focus ring, selected row, primary CTA, the 2px hairline atop the featured card, the wordmark dot, links. **Never** as a large fill or page background.
- **Surfaces:** flat, near-black, cool-charcoal. Elevation reads through hairline borders + low-spread shadows. **No gradient backgrounds** (the only gradients allowed are the 2px accent hairline and the wordmark dot).
- **Casing:** sentence case everywhere.
- **Icons:** Lucide, 24×24, 2px round stroke, no fill, inherit text color.

---

## Screens / Views

The prototype is a single-page app with 6 routes switched by the top nav and the left Explorer. In Jekyll these map to real pages/layouts.

### 0. Global chrome (present on every page)

**Titlebar** (`height: 48px`, `background: --surface-panel #0f1113`, `border-bottom: 1px solid --border-subtle`):
- Left: orange dot (`9px` circle, `--accent-500`, soft glow `box-shadow: 0 0 10px --accent-alpha-40`) · wordmark `uright` (16px/600, tracking -0.02em) · `blog` chip (Geist Mono 11px, `--accent-contrast #1f0d04` on `--accent-500`, radius 5px, padding 2px 6px).
- Breadcrumb: Geist Mono 12px, `~/` in `--text-muted` + current path in `--text-secondary` (e.g. `~/ posts`, `~/ posts / <post title>`, `~/ archives`). Truncate with ellipsis, max-width ~300px.
- Center-right: search field (width 300px, height 32px, `--surface-sunken #131519`, inset shadow, search icon + `Search posts…` placeholder + `⌘K` kbd hint).
- Nav: `Home · Archives · Categories · Tags · About` (13px/500, ghost buttons; active = `color --text-primary` + `background --surface-active`; idle = `--text-tertiary`; hover = `--surface-hover` + `--text-primary`).
- Right: social icons (GitHub, LinkedIn, RSS) — 30px square ghost buttons, `--text-tertiary` (RSS in `--accent-400`).

**Left Explorer** (`width: 286px`, `background --surface-panel`, `border-right --border-subtle`):
- 36px header: eyebrow `EXPLORER` (10px/600 uppercase, tracking 0.06em, `--text-tertiary`) + two 24px icon buttons.
- Section `CATEGORIES`: one row per category — chevron + folder icon (in category color) + name (13px, `--text-secondary`) + count (mono 11px). Row height 30px, hover `--surface-hover`.
- Section `RECENT POSTS`: one row per post — file-text icon (in category color) + **post title** (12.5px/500, `--text-secondary`, ellipsis) + date below (mono 10px `YYYY-MM-DD`). Row min-height 34px, indented `padding-left 26px`, hover wash. **Note: rows show the post TITLE, never the filename.**
- Footer (38px): RSS icon + `Subscribe to the feed` + `atom.xml` (mono).

**Right rail** (`width: 264px`, `--surface-panel`, `border-left --border-subtle`) — context-dependent:
- On Home/Archives/Categories/Tags/About → **About card**: avatar (40px, initials `JW`, accent ring), name + role, one-line bio, social row, `POPULAR TAGS` chips, `STATS` table (mono key/value rows on `--surface-sunken`).
- On Post → **Outline**: `ON THIS PAGE` TOC (active item `--accent-400` with a 2px accent indicator on a vertical rail), `DETAILS` mono table (category/published/words/reading), `SHARE` icons.

**Status bar** (`height: 26px`, `--surface-panel`, `border-top --border-subtle`, Geist Mono 11px, `--text-tertiary`): `⎇ main` · `▤ 17 posts` · `jekyll · chirpy` · (right) `RSS` (accent) · `blog.uright.ai` · green dot `deployed`.

### 1. Home / post list  → Jekyll `home`/`index`
- Centered column (max-width 780px, padding 30px 40px 80px).
- Header block: eyebrow `JACK WONG · DEV NOTES` (10px/600 uppercase, `--accent-400`); H1 `Building with LLMs, in the open.` (32px/600, tracking -0.02em); sub-paragraph (15px, `--text-secondary`).
- **Featured card** (first/most-recent post): raised surface, radius `--radius-xl` 12px, `--shadow-sm`, 2px accent gradient hairline on top edge. Left: 104px thumbnail tile (`--surface-sunken`, category-colored Lucide glyph). Right: `FEATURED ·` eyebrow + category badge, H2 title (21px/600), description, meta row (mono: date · clock+`N min read` · `Read post →` in accent). Hover: border → `--accent-alpha-40`.
- Divider row: `ALL POSTS` (mono caption) + count + `⇄ Newest first`.
- **Post list**: stacked cards (raised surface, radius `--radius-lg` 10px). Each: 62px category-colored thumbnail tile + body (category badge + mono date + `N min` · H3 title 15px/600 · one-line description, ellipsis). Hover: lift 1px + border `--border-strong`.
- (Tweakable: thumbnails and descriptions can be toggled — see State.)

### 2. Single post  → Chirpy `post` layout
- **Editor tab strip** (sticky, height 36px): active tab = file-text icon (violet) + **post title** (12.5px/500, ellipsis, max-width 300px) + close `×`, with a 2px accent bar on top; a dimmed second tab; right side `markdown` label. Tabs show TITLES, not filenames.
- Article column (max-width 760px, padding 34px 44px 90px):
  - Category badge + mono date; H1 (34px/600, tracking -0.022em); lead paragraph (16px/1.6, `--text-secondary`); byline row (24px avatar + name, `clock 7 min read`, `Share`) with bottom hairline.
  - Body: H2 sections (21px/600), paragraphs (15.5px/1.72, `--gray-100`), inline `code` chips (mono 0.85em, `--surface-sunken` bg, hairline border, `--accent-300` text), links (`--accent-400` with accent-alpha underline).
  - **Callout** (warning): flex row, `--status-warning-bg`, left border 3px `--amber-500`, triangle-alert icon, radius `--radius-md`.
  - **Diagram block** (the mermaid graph rendered as a node diagram): `--surface-sunken` with a subtle dot-grid (`radial-gradient(--white-alpha-04 1px, transparent 1px)` 16px), node pills connected by 1px `--graph-edge` lines; the LiteLLM node highlighted in accent, NIM node in blue; `fig 1 —` caption. *(In Chirpy, keep using the `mermaid: true` front-matter and just theme mermaid to match; the prototype hand-builds it only because it's a static mock.)*
  - **Code block**: header bar (height 36px, `--gray-850`, file icon + filename like `config.yaml` + language chip + `copy`), body `<pre>` (mono 12.5px/1.75, `--surface-sunken`, token colors: keys `--violet-500`, sub-keys `--blue-500`, strings/values `--green-500`, booleans `--accent-300`, comments/`$` prompt `--text-tertiary`). **Keep real code filenames here** — these are code, not blog posts.
  - **Table**: full-width, header row on `--gray-850`, hairline row borders, mono for ID-like cells (`--accent-300`).
  - Tags row (mono `#tag` chips) after a top hairline; prev/next cards.

### 3. Archives  → Chirpy `archives`
- Eyebrow `git log --all`; H1 `Archives`; per-year sections. Year header: mono year (22px/600) + hairline + `N posts` pill. Below: a git-log timeline — vertical 2px rail with a commit-dot per post (ringed in the category color), `Mon DD` (mono, right-aligned 54px) + title (ellipsis) + category badge. Row hover wash.

### 4. Categories  → Chirpy `categories`
- Eyebrow `~/posts`; H1 `Categories`; 2-column grid of folder cards (raised surface, radius `--radius-xl`). Each: 42px category-colored icon tile + `N posts` pill, H2 name, description, then up to 3 recent post titles (dot + ellipsized title) under a hairline. Hover: lift + `--border-strong`.

### 5. Tags  → Chirpy `tags`
- Eyebrow `grep -r #`; H1 `Tags`; mono tag cloud inside a raised panel. Each tag `#name` sized by frequency (8+ posts → 19px/600 `--accent-300`; 2–4 → 14–16px `--text-secondary`; 1 → 13px `--text-tertiary`) with a small superscript count. `white-space: nowrap` per tag so names never break mid-word. Legend row below.

### 6. About  → `_tabs/about.md`
- Mono `cat about.md`; header row: 56px avatar (initials `JW`, accent ring) + H1 `Jack Wong` + mono role `Enterprise Architect · tech evangelist` + GitHub/LinkedIn pill buttons; bottom hairline.
- Lead paragraph (16px/1.7).
- `SKILLS` — mono pill chips (AWS Bedrock, Azure OpenAI, PGVector, Qdrant, LLMs & deep learning, Enterprise architecture).
- `EXPERIENCE` — timeline (accent dot for current role, neutral ringed dot for past): role (15px/600) + mono date range (right), company (accent for current), description.
- `EDUCATION` — single card: 40px icon tile + degree + school + mono `Honours Computer Science · Business Option`.

---

## Interactions & behavior
- **Navigation:** top nav and Explorer rows both route between the 6 views. Active route → accent-tinted nav button + breadcrumb update. In Jekyll these are real page loads; mirror the active state via Chirpy's nav-active logic.
- **Hover:** surfaces lighten with a white-alpha wash (`--surface-hover` .04 → `--surface-active` .08); text tertiary→primary; cards lift 1px and strengthen their border; primary button lightens to `--accent-400` and gains `--glow-accent`.
- **Press:** controls shrink slightly (`scale .92–.99`, translateY .5px). No color inversion.
- **Focus:** 2px orange ring at ~40% alpha via box-shadow (`--ring-focus`); inputs also swap border to `--border-focus`.
- **Motion:** 80–280ms; standard easing `cubic-bezier(.2,0,.2,1)`, entrances `ease-out`. No bounce on chrome. Respect `prefers-reduced-motion`.
- **Scrollbars:** thin (10px), `--gray-600` thumb, transparent track; panels scroll independently while chrome stays fixed.
- **Code copy:** the `copy` control in code-block headers should copy the block (Chirpy already ships clipboard copy — keep it, restyle the button).
- **Post Outline:** the right-rail TOC highlights the section in view (Chirpy's TOC via Tocbot — restyle to the accent indicator look).

## State management
The prototype is static; the only real interactive state worth carrying into Chirpy:
- **Active route** (which of the 6 views) → native Jekyll routing + active-nav class.
- Two prototype-only display toggles exist as Tweaks and are **not required** in production (they were for design review): `showThumbnails` and `showPostDescriptions` on the home list. If wanted, expose as `_config.yml` flags.
- No data fetching. Post/category/tag/archive data all come from Jekyll collections & front matter.

---

## Design tokens

Exact values (see `tokens/*.css` for the full set). Map these onto Chirpy's SCSS variables.

### Colors — surfaces
```
--gray-950 #0a0b0d  canvas / deepest        (--surface-canvas)
--gray-900 #0f1113  primary panel/sidebar   (--surface-panel)
--gray-850 #131519  sunken inputs/code well (--surface-sunken)
--gray-800 #16181c  raised card/popover     (--surface-raised)
--gray-750 #1a1d22  secondary surface
--gray-700 #1f232a  hover surface
--gray-600 #272b33  active/pressed; scrollbar thumb
--gray-500 #353a44  strong divider/control bg
```
### Colors — text
```
--text-primary   #f3f5f8 (--white)
--text-secondary #a8b0bb (--gray-150)
--text-tertiary  #6b7280 (--gray-300)
--text-muted     #8b94a1 (--gray-200)
--gray-100       #c8cdd5  (body copy in articles)
```
### Colors — accent (orange)
```
--accent-100 #ffe7d6   --accent-200 #ffcaa6   --accent-300 #ffa973
--accent-400 #ff8a44   --accent-500 #f26a21 (base)   --accent-600 #db5715
--accent-700 #b5440f   --accent-contrast #1f0d04 (text on filled accent)
--accent-alpha-08/12/16/24/40  rgba(242,106,33, .08/.12/.16/.24/.40)
--text-link / --text-accent = --accent-400
```
### Colors — category / status hues (neutral identity markers, used at low density)
```
AI & LLMs   --blue-500   #4aa3ff   (bg rgba(74,163,255,.12),  border .24)
Claude Code --violet-500 #9d7bff   (bg rgba(157,123,255,.12), border .24)
DevOps      --agent-datadoug #4cc9b0 (bg rgba(76,201,176,.12), border .24)
Quick Tips  --amber-500  #f5b544   (bg rgba(245,181,68,.12),  border .24)
green/success #34d399   red/danger #f0584f   info #4aa3ff
status-warning-bg rgba(245,181,68,.12)
```
### Borders (white-alpha)
```
--border-subtle  rgba(255,255,255,.06)
--border-default rgba(255,255,255,.10)
--border-strong  rgba(255,255,255,.14)
--border-accent  rgba(242,106,33,.40)
```
### Typography
```
Families: Geist (UI), Geist Mono (code/paths/identifiers/dates/tags)
Weights: 400 / 500 / 600 / 700
Sizes used: 10,11,12,12.5,13,13.5,14,15,15.5,16,17,21,26,30,32,34 px
Leading: 1.2 tight (headings) · 1.5 normal (body) · 1.7–1.75 (article/code)
Tracking: -0.022em (H1) · -0.02em (display) · -0.015em (H2) · 0.06em (eyebrow caps)
Eyebrow: 10px/600 uppercase, tracking 0.06em, --accent-400 or --text-tertiary
```
### Spacing / radii / elevation
```
Spacing: 4px base grid (4,6,8,10,12,14,16,20,24,28,32,40 …)
Radii: xs 4 · sm 6 · md 8 (controls) · lg 10 · xl 12 (cards/panels) · 2xl 16 · pill 999
Chrome: titlebar 48 (DS default 38) · sidebar 286 · right rail 264 · tab 36 · statusbar 26
Shadows: --shadow-xs 0 1px 2px rgba(0,0,0,.30); --shadow-sm 0 1px 2px/.40 + 0 1px 1px/.24
--glow-accent 0 0 0 1px --accent-alpha-40, 0 4px 20px rgba(242,106,33,.24)  (primary hover / active node only)
--ring-focus 0 0 0 2px --surface-canvas, 0 0 0 4px --accent-alpha-40
Motion: 80/130/190/280ms; ease-standard cubic-bezier(.2,0,.2,1); ease-out cubic-bezier(.16,1,.3,1)
```

## Assets
- **Icons:** Lucide (MIT), 2px round stroke. The prototype embeds the exact Lucide path subset in its logic class — for Jekyll, just include Lucide (the inline-SVG sprite or the `lucide` web font/JS) and reference the same glyph names: `search, file-text, folder, folder-open, chevron-right, command, terminal, database, git-branch, git-commit, network, zap, sparkles, bot, refresh-cw, trash-2, message-square, clock, calendar, hash, rss, github, linkedin, link, copy, external-link, list-tree, sliders-horizontal, layers, triangle-alert, arrow-right, x`.
- **Avatar:** real author photo not supplied — prototype uses an `JW` initials avatar with an accent ring. Drop in `assets/img/jack-avatar-squared.png` (already in the repo) and keep the accent ring treatment.
- **Fonts:** Geist + Geist Mono. Self-host woff2 for production if you want to avoid the Google Fonts request.
- **No uright logo** exists yet — the wordmark (`● uright [blog]`) is a typographic placeholder. Swap in a real SVG logo when available.
- **Post thumbnails:** the prototype uses category-colored Lucide glyph tiles as placeholders. Real posts have hero images (`image.path` front matter) — use those in the list/featured tiles, falling back to the glyph tile when a post has no image.

## Category mapping (prototype → posts)
The prototype groups the 17 real posts into 4 categories. Your real front matter uses `[Tech, AI]` etc. — reconcile to these four (or adjust the design to your taxonomy): **AI & LLMs**, **Claude Code**, **DevOps**, **Quick Tips**.

## Files
- `Uright Blog Theme.dc.html` — the full high-fidelity prototype (all 6 views + chrome). Open in a browser to interact; read the source for exact structure, copy, and inline-style token values.
- `tokens/` — the uright Studio design-system token CSS (colors, typography, spacing, elevation, fonts, base). Source of truth for all values above.
- `_screenshots/` — *(optional, ask)* rendered captures of each view.

## Target repo
`github.com/uright/uright.github.io` (branch `master`) — Jekyll + `jekyll-theme-chirpy`, `theme_mode: dark`. Customize via `_sass/` overrides, `_includes/`/`_layouts/` overrides, and `assets/css/jekyll-theme-chirpy.scss`. The blog is moving to `blog.uright.ai` (update `url`/`CNAME`).
