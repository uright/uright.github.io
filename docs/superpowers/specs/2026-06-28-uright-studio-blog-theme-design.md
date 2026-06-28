# Design: uright Studio theme for the Chirpy blog

**Date:** 2026-06-28
**Status:** Approved (brainstorming)
**Source design:** `docs/design/blog_theme/` (README.md, `Uright Blog Theme.dc.html`, `tokens/*.css`)

## Summary

Reskin the uright tech blog into a dark, IDE-inspired theme aligned to the **uright Studio**
design system. The blog is presented as if it were the uright Studio desktop app: a fixed
titlebar, a left **Explorer** panel (categories as folders, posts as a file-tree), the main
reading panel, a contextual right rail (About card / post Outline), and a bottom status bar.

The site stays on `jekyll-theme-chirpy` (gem, pinned `~> 7.3`). We customize Chirpy via its
override mechanisms rather than replacing Jekyll or forking the theme. Fidelity target:
**full, pixel-faithful IDE chrome** on desktop, collapsing to slide-in drawers on mobile.

## Goals

- Pixel-faithful reproduction of the uright Studio IDE chrome (titlebar, Explorer, right rail,
  status bar) and the six views, using the exact tokens in `docs/design/blog_theme/tokens/`.
- Keep Chirpy's working plumbing: client-side search, TOC, Rouge syntax highlighting +
  copy-to-clipboard, categories/tags/archives generation, pagination, RSS/atom, SEO, PWA,
  Disqus, Google Analytics, mermaid.
- Self-hosted Geist + Geist Mono fonts and an inline Lucide SVG sprite (no runtime font/icon
  network dependency).
- Usable, identity-preserving mobile experience via drawers.

## Non-goals (handled separately)

- Domain migration to `blog.uright.ai` (update `url` in `_config.yml` + `CNAME`). Decoupled
  DNS/deploy concern, not part of this theme work.
- Real "About" page content (experience/education) — stubbed with design placeholder copy and
  flagged for the author to fill.

## Decisions (from brainstorming)

| Topic | Decision |
|---|---|
| Fidelity | Full IDE chrome, pixel-faithful |
| Mobile | Collapse Explorer + right rail to toggleable slide-in drawers |
| Categories | Re-tag all 17 posts to the 4-category model |
| Infra in scope | Geist/Geist Mono fonts, Lucide icons, mermaid theming |
| Infra out of scope | Domain migration (blog.uright.ai) |
| Foundation | Stay on Chirpy (keep plumbing); do not go ground-up |
| Override strategy | Custom layout wrapper (`_layouts/default.html`) + minimal partial overrides |
| Assets delivery | Self-host fonts (woff2); build-time inline Lucide SVG sprite |
| Spec scope | One complete spec; phased implementation plan with checkpoints |

## Architecture

Three override surfaces, touching as few gem files as possible:

1. **SCSS token layer.** Entry point `assets/css/jekyll-theme-chirpy.scss` imports Chirpy's
   bundle, then a repo-local SCSS tree under `_sass/uright/` that maps uright Studio tokens
   onto CSS custom properties + Chirpy's variables, and restyles components.
2. **Custom layout wrapper.** Repo-local `_layouts/default.html` defines the IDE shell and
   injects Chirpy's page content into the center column. `home`, `post`, `archives`,
   `categories`, `tags`, `page` inherit from it as Chirpy expects. We override only
   `default.html` plus the few partials needing structural change.
3. **New `_includes/` partials.** One per chrome region plus helpers.

Data-driven chrome: Explorer categories/posts, status-bar post count, right-rail About card,
and category colors come from Jekyll collections + a new `_data/uright.yml`. No hardcoded
post lists.

### File layout (new/changed)

```
assets/css/jekyll-theme-chirpy.scss   # entry: import chirpy bundle + uright tree, force dark
_sass/uright/
  _tokens.scss        # all uright Studio CSS custom properties (verbatim from tokens/*.css)
  _chirpy-bridge.scss # remap Chirpy SCSS/CSS vars → uright tokens
  _base.scss          # body bg, Geist/Geist Mono wiring, scrollbars, focus rings, reduced-motion
  _chrome.scss        # titlebar, explorer, right-rail, statusbar, IDE grid shell, mobile drawers
  _views.scss         # home/featured/post-list, post article, archives, categories, tags, about
  _components.scss    # cards, badges, callouts, code blocks, tables, tag chips, mermaid theming
_layouts/
  default.html        # IDE shell wrapper (overrides Chirpy's)
  # plus targeted overrides of home/post/archives/categories/tags only where structure changes
_includes/
  titlebar.html
  explorer.html
  right-rail.html
  statusbar.html
  uright-icon.html    # <svg><use> helper referencing the sprite
  category-color.html # resolves a category → color/icon from _data/uright.yml
_data/
  uright.yml          # category → {color, icon, description}; about-card content
assets/fonts/         # self-hosted Geist + Geist Mono woff2
assets/img/lucide-sprite.svg  # build-time inline sprite, ~30 named glyphs
```

## Design tokens & SCSS

All raw values from `docs/design/blog_theme/tokens/*.css` go into `_tokens.scss` verbatim as
CSS custom properties: full gray scale (`--gray-950`…`--white`), accent ramp
(`--accent-100`…`--accent-900`, `--accent-contrast`), semantic hues, alpha tints, semantic
aliases (`--surface-*`, `--text-*`, `--border-*`, `--action-*`, `--status-*`), elevation
(`--shadow-*`, `--glow-accent`, `--ring-focus`), and motion (`--dur-*`, `--ease-*`).

**Rule:** components reference **semantic aliases**, never raw scale values (matches the design
system's own convention).

**Fonts:** `@font-face` from self-hosted woff2 under `assets/fonts/`. Do NOT use the Google
`@import` from `tokens/fonts.css`. `font-display: swap` + system fallback stack
(`-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif` for UI; `ui-monospace,
SFMono-Regular, Menlo, monospace` for mono).

**Chirpy bridge:** force dark mode; point Chirpy's color variables (`--main-bg`, `--text-color`,
`--link-color`, code/border colors, etc.) at uright tokens so anything not explicitly restyled
still inherits the palette.

### Category color map (`_data/uright.yml`)

| Category | Token | Hex | Lucide icon |
|---|---|---|---|
| AI & LLMs | `--blue-500` | `#4aa3ff` | `sparkles` / `bot` |
| Claude Code | `--violet-500` | `#9d7bff` | `terminal` |
| DevOps | `--agent-datadoug` | `#4cc9b0` | `git-branch` |
| Quick Tips | `--amber-500` | `#f5b544` | `zap` |
| (fallback) | `--text-tertiary` | `#6b7280` | `file-text` |

## Layout shell & chrome

**Grid.** `default.html` defines a CSS grid: fixed titlebar (top, 48px) + fixed status bar
(bottom, 26px) sandwiching a 3-column middle row — Explorer (286px) · content (1fr, scrolls) ·
right rail (264px). Chrome is fixed/sticky; only the center column scrolls. Panels get thin
(10px) scrollbars, `--gray-600` thumb, transparent track.

**Titlebar** (`_includes/titlebar.html`, 48px, `--surface-panel`, bottom `--border-subtle`):
- Orange dot (9px, `--accent-500`, glow `0 0 10px --accent-alpha-40`) · `uright` wordmark
  (16px/600, tracking -0.02em) · `blog` chip (Geist Mono 11px, `--accent-contrast` on
  `--accent-500`, radius 5px, pad 2px 6px).
- Breadcrumb: Geist Mono 12px, `~/` in `--text-muted` + current path in `--text-secondary`;
  ellipsis, max-width ~300px; path derived from current page.
- Search field (300×32, `--surface-sunken`, inset shadow, search icon + `Search posts…`
  placeholder + `⌘K` kbd hint) wired to Chirpy's existing search.
- Nav `Home · Archives · Categories · Tags · About` (13px/500 ghost buttons; active =
  `--text-primary` + `--surface-active`; idle `--text-tertiary`; hover `--surface-hover` +
  `--text-primary`). Active state from current page URL.
- Social icons (GitHub, LinkedIn, RSS) from `_config.yml`; 30px ghost buttons, RSS in
  `--accent-400`.

**Left Explorer** (`_includes/explorer.html`, 286px, `--surface-panel`, right `--border-subtle`):
- 36px header: eyebrow `EXPLORER` (10px/600 uppercase, tracking 0.06em, `--text-tertiary`) +
  two 24px icon buttons.
- `CATEGORIES`: one row per category from `_data/uright.yml` — chevron + folder icon (category
  color) + name (13px `--text-secondary`) + count (mono 11px). Row 30px, hover `--surface-hover`.
- `RECENT POSTS`: one row per recent post — file-text icon (category color) + post **title**
  (12.5px/500, ellipsis) + date below (mono 10px `YYYY-MM-DD`). Min-height 34px, indent
  `padding-left 26px`. **Rows show the post TITLE, never the filename.**
- Footer (38px): RSS icon + `Subscribe to the feed` + `atom.xml` (mono).

**Right rail** (`_includes/right-rail.html`, 264px, `--surface-panel`, left `--border-subtle`):
- On post pages → **Outline**: `ON THIS PAGE` TOC (restyle Chirpy's Tocbot; active item
  `--accent-400` with a 2px accent indicator on a vertical rail) + `DETAILS` mono table
  (category/published/words/reading) + `SHARE` icons.
- On all other pages → **About card**: 40px avatar (initials `JW`, accent ring) + name/role +
  one-line bio + social row + `POPULAR TAGS` chips + `STATS` mono table on `--surface-sunken`.
- Switched by page type/`layout`.

**Status bar** (`_includes/statusbar.html`, 26px, `--surface-panel`, top `--border-subtle`,
Geist Mono 11px, `--text-tertiary`): `⎇ main` · `▤ N posts` (`site.posts.size`) ·
`jekyll · chirpy` · (right) `RSS` (accent) · site host · green dot `deployed`.

**Mobile (drawers).** Below ~1024px (`$tablet`): grid collapses to one column. Explorer and
right rail become off-canvas slide-in drawers toggled by a hamburger (left) and an info button
(right) added to the titlebar; search collapses to an icon; status bar simplifies; content goes
full-width. CSS-driven with a small JS toggle. Respects `prefers-reduced-motion` (no slide
animation, instant show/hide).

## Views

Each maps to a Chirpy layout, restyled to the prototype (exact tokens in the design README §1–6).

1. **Home** (`home`): centered 780px column (pad 30/40/80); eyebrow `JACK WONG · DEV NOTES`;
   H1 `Building with LLMs, in the open.` (32px/600, tracking -0.02em); sub-paragraph.
   **Featured card** (most-recent post): raised, radius 12px, `--shadow-sm`, 2px accent
   gradient hairline on top; 104px thumbnail tile; `FEATURED ·` eyebrow + category badge; H2
   (21px/600); description; meta row (date · `N min read` · `Read post →` accent). Hover →
   border `--accent-alpha-40`. Divider `ALL POSTS` + count + `⇄ Newest first`. **Post list**:
   stacked cards (radius 10px), 62px category-colored thumbnail + badge + mono date + `N min`
   + H3 (15px/600) + one-line description (ellipsis). Hover lift 1px + `--border-strong`.
   Thumbnails use `image.path`, falling back to a category-colored Lucide glyph tile.
   `showThumbnails` / `showPostDescriptions` exposed as `_config.yml` flags (default on).

2. **Post** (`post`): sticky **editor tab strip** (36px): active tab = file-text icon (violet)
   + post **title** (12.5px/500, ellipsis, max-width 300px) + close `×`, 2px accent bar on top;
   a dimmed second tab; right `markdown` label. **Tabs show TITLES, not filenames.** Article
   column (760px, pad 34/44/90): category badge + mono date; H1 (34px/600, tracking -0.022em);
   lead paragraph (16px/1.6 `--text-secondary`); byline row (24px avatar + name + `clock 7 min
   read` + `Share`) with bottom hairline. Body: H2 (21px/600), paragraphs (15.5px/1.72
   `--gray-100`), inline `code` chips (mono 0.85em, `--surface-sunken` bg, hairline border,
   `--accent-300` text), links (`--accent-400` + accent-alpha underline). **Warning callout**
   (`--status-warning-bg`, left border 3px `--amber-500`, triangle-alert icon, radius md).
   **Mermaid** themed to the diagram block look (`--surface-sunken` + radial-gradient dot-grid
   16px, node pills + 1px `--graph-edge` lines, accent/blue node highlights) — keep
   `mermaid: true` front matter and theme mermaid to match. **Code blocks**: header bar (36px,
   `--gray-850`, file icon + filename + language chip + restyled `copy` button — keep Chirpy's
   clipboard JS), body `<pre>` (mono 12.5px/1.75, `--surface-sunken`, token colors: keys
   `--violet-500`, sub-keys `--blue-500`, strings/values `--green-500`, booleans `--accent-300`,
   comments/`$` `--text-tertiary`). Keep real code filenames here. **Tables**: header on
   `--gray-850`, hairline rows, mono for ID cells (`--accent-300`). Tags row (mono `#tag`
   chips) after a hairline; prev/next cards.

3. **Archives** (`archives`): eyebrow `git log --all`; H1 `Archives`; per-year sections (mono
   year 22px/600 + hairline + `N posts` pill); **git-log timeline** — vertical 2px rail,
   commit-dot per post ringed in category color, `Mon DD` (mono, right-aligned 54px) + title
   (ellipsis) + category badge. Row hover wash.

4. **Categories** (`categories`): eyebrow `~/posts`; H1 `Categories`; 2-column grid of folder
   cards (raised, radius 12px): 42px category-colored icon tile + `N posts` pill + H2 name +
   description + up to 3 recent post titles (dot + ellipsized title) under a hairline. Hover
   lift + `--border-strong`.

5. **Tags** (`tags`): eyebrow `grep -r #`; H1 `Tags`; mono tag cloud in a raised panel; each
   `#name` sized by frequency (8+ → 19px/600 `--accent-300`; 2–4 → 14–16px `--text-secondary`;
   1 → 13px `--text-tertiary`) with superscript count; `white-space: nowrap` per tag. Legend
   row below.

6. **About** (`_tabs/about.md`): mono `cat about.md`; header row: 56px avatar (`JW`, accent
   ring) + H1 `Jack Wong` + mono role `Enterprise Architect · tech evangelist` +
   GitHub/LinkedIn pill buttons; bottom hairline. Lead paragraph (16px/1.7). `SKILLS` mono pill
   chips. `EXPERIENCE` timeline (accent dot current role, neutral ringed dot past): role
   (15px/600) + mono date range + company (accent for current) + description. `EDUCATION` single
   card: 40px icon tile + degree + school + mono `Honours Computer Science · Business Option`.
   **Experience/education content stubbed with placeholder copy from design README §6; flagged
   for author to fill.**

## Assets

- **Fonts:** self-host Geist + Geist Mono woff2 in `assets/fonts/`; `@font-face` with
  `font-display: swap` + system fallback.
- **Icons:** build-time inline Lucide SVG sprite (`assets/img/lucide-sprite.svg`) containing
  only the named glyphs: `search, file-text, folder, folder-open, chevron-right, command,
  terminal, database, git-branch, git-commit, network, zap, sparkles, bot, refresh-cw, trash-2,
  message-square, clock, calendar, hash, rss, github, linkedin, link, copy, external-link,
  list-tree, sliders-horizontal, layers, triangle-alert, arrow-right, x`. Referenced via
  `<svg><use href="…#name">`; 24×24, 2px round stroke, inherit text color.
- **Avatar:** `assets/img/jack-avatar-squared.png` (already in repo) with accent ring; `JW`
  initials fallback.
- **Wordmark:** typographic placeholder `● uright [blog]`; swap real SVG logo when available.
- **Post thumbnails:** use `image.path` front matter; fall back to category-colored Lucide
  glyph tile when absent.

## Content reconciliation — category re-tagging

All 17 posts move to the 4-category model. `Tech` parent dropped.

| Post (slug fragment) | Current | → New |
|---|---|---|
| private-gpt-clear-ingested-files | Tech, Ai | AI & LLMs |
| codellama-instruct-13b-snake-game | Tech, Ai | AI & LLMs |
| azure-openai-on-open-webui | Tech, AI | AI & LLMs |
| top-10-hugo-themes-with-chatgpt | Tech, AI | AI & LLMs |
| using-aws-bedrock-models-from-openwebui | Tech, AI | AI & LLMs |
| github-copilot-models-via-litellm-proxy | Tech, AI | AI & LLMs |
| docker-desktop-volume-backup-and-restore | Tech, Docker | DevOps |
| sharing-git-credentials-wsl-windows | Tech, Development | DevOps |
| managing-jekyll-blogs-openclaw-tailscale | Tech, Tutorial | DevOps |
| shiftenter-shortcut-claude-code-antigravity | Tech, Development | Claude Code |
| sound-notifications-claude-code-wsl | Tech, AI | Claude Code |
| switching-claude-profiles-anthropic-bedrock | Tech, Tutorial | Claude Code |
| run-claude-code-cli-github-copilot | Tech, AI | Claude Code |
| sound-notifications-claude-code-macos | Tech, AI | Claude Code |
| running-claude-code-free-nvidia-nim | Tech, AI | Claude Code |
| installing-aws-cli-v2-with-uv-tool | Tech, Tools | Quick Tips |
| text-to-speech-macos-windows | Tech, Quick Tips | Quick Tips |

Result: AI & LLMs 6 · Claude Code 6 · DevOps 3 · Quick Tips 2. Tags are left unchanged
(the Tags view + cloud uses existing tags).

## Error handling & edge cases

- Post with no `image.path` → category-colored Lucide glyph tile.
- Empty category/tag → renders with zero count, no crash.
- Uncategorized / off-model category → neutral fallback color + `file-text` icon.
- Self-hosted fonts → `font-display: swap` + system fallback so text renders before woff2 loads.
- `prefers-reduced-motion` → disable transitions and drawer slide animation.
- Mermaid absent on a post → diagram styles simply don't apply.
- Long breadcrumb / post title → ellipsis truncation (max-widths specified above).

## Testing & verification

- `bundle exec jekyll build` completes clean.
- `html-proofer` (existing dev dep) passes.
- Local serve checked at desktop + mobile widths: drawer toggle works, panels scroll
  independently, chrome stays fixed.
- Each of the 6 views renders with real content; featured + fallback thumbnails both exercised.
- Chirpy JS intact: search opens via `⌘K`, code copy-to-clipboard works, TOC highlights on
  scroll.
- Lighthouse pass (validates self-hosted-font perf; no render-blocking font/icon network calls).

## Implementation phasing (plan checkpoints)

1. **Foundation** — tokens, SCSS bridge, self-hosted fonts, Lucide sprite, `_data/uright.yml`,
   category helpers.
2. **Chrome shell** — `_layouts/default.html` grid + titlebar/explorer/right-rail/statusbar
   partials + mobile drawers.
3. **Views** — home, post, archives, categories, tags, about; re-tag the 17 posts.
4. **Polish** — mermaid + code-block theming, interactions/hover/focus, full verification pass.

## Open items for author

- Fill real About content (experience, education) — stubbed for now.
- Provide a real uright SVG logo if/when available (wordmark is a placeholder).
- Domain migration (`blog.uright.ai`) tracked separately.
