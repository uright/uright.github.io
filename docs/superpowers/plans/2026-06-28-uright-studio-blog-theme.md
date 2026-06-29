# uright Studio Blog Theme Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reskin the `jekyll-theme-chirpy` blog into a dark, IDE-inspired "uright Studio" theme — fixed titlebar, left Explorer file-tree, right context rail, bottom status bar — pixel-faithful on desktop, collapsing to drawers on mobile.

**Architecture:** Keep Chirpy as a gem. Customize via three override surfaces: (1) a repo-local SCSS tree under `_sass/uright/` mapping uright Studio tokens onto CSS custom properties + Chirpy's variables, imported after Chirpy's bundle; (2) a custom `_layouts/default.html` that defines the IDE shell grid and injects Chirpy's content-rendering partials into the center column; (3) new `_includes/` partials for each chrome region, driven by Jekyll collections + a `_data/uright.yml` file. Self-hosted Geist/Geist Mono fonts + an inline Lucide SVG sprite.

**Tech Stack:** Jekyll, jekyll-theme-chirpy 7.3, SCSS (Dart Sass via `@use`), Liquid, CSS Grid, vanilla JS (drawers), self-hosted woff2 fonts, inline SVG icon sprite.

## Global Constraints

- Chirpy gem pinned `~> 7.3` (already in Gemfile). Do not fork the theme.
- `theme_mode: dark` forced; the theme is dark-only.
- All visual values come from `docs/design/blog_theme/tokens/*.css` — copy hex/values verbatim. Components reference **semantic aliases** (`--surface-panel`, `--text-secondary`, `--accent-500`), never raw scale values where an alias exists.
- Casing: sentence case in all UI copy. Eyebrows are UPPERCASE per design.
- Fonts: Geist (UI), Geist Mono (code/paths/identifiers/dates/tags). Self-hosted woff2, `font-display: swap`, system fallback stack. Do NOT use the Google Fonts `@import`.
- Icons: Lucide, 24×24, 2px round stroke, no fill, `currentColor`. Inline SVG sprite, referenced via `<svg><use>`.
- Explorer/tab rows show post **titles**, never filenames. Code-block headers keep real code filenames.
- Accent (`#f26a21` ramp) used sparingly — never as a large fill or page background.
- Mobile breakpoint for drawer collapse: `1024px` (max-width).
- Respect `prefers-reduced-motion`: disable transitions + drawer slide animation.
- Build must stay green: `bundle exec jekyll build` clean and `bundle exec htmlproofer` passes after each phase.
- Commit after every task. Branch: `feature/theme-rebuild` (current).

## Reference files (read before starting)

- Spec: `docs/superpowers/specs/2026-06-28-uright-studio-blog-theme-design.md`
- Design README: `docs/design/blog_theme/README.md` (view-by-view spec)
- Prototype: `docs/design/blog_theme/Uright Blog Theme.dc.html` (read for structure/measurements only — ignore its React runtime)
- Tokens: `docs/design/blog_theme/tokens/{colors,elevation,typography,spacing,fonts,base}.css`
- Chirpy gem (read-only reference for overrides): `/Users/jack/.rbenv/versions/3.4.4/lib/ruby/gems/3.4.0/gems/jekyll-theme-chirpy-7.3.0/`

## Build/verify commands (used throughout)

- Build: `bundle exec jekyll build` → expect "done in N seconds", no errors.
- Serve (manual visual check): `bundle exec jekyll serve --livereload` → http://localhost:4000
- Link check: `bundle exec htmlproofer _site --disable-external --allow-hash-href` (skip external to keep fast/offline; run after build).
- Inspect output HTML/CSS: `grep -r "<pattern>" _site/`

> **Note on "tests":** This is a static-site theming project; there is no unit-test runner for SCSS/Liquid. Each task's verification step is a real build + a concrete grep/visual check. Treat a clean build + the stated grep/visual result as the passing condition.

## File structure (created/modified)

```
Gemfile.lock                                  # (regenerated if needed)
assets/css/jekyll-theme-chirpy.scss           # CREATE — entry: import chirpy + uright tree
_sass/uright/_tokens.scss                     # CREATE — all uright CSS custom properties
_sass/uright/_fonts.scss                      # CREATE — @font-face for Geist/Geist Mono
_sass/uright/_chirpy-bridge.scss              # CREATE — remap Chirpy vars → uright tokens
_sass/uright/_base.scss                       # CREATE — body, scrollbars, focus, reduced-motion
_sass/uright/_chrome.scss                     # CREATE — IDE grid, titlebar, explorer, rail, statusbar, drawers
_sass/uright/_views.scss                      # CREATE — home, post, archives, categories, tags, about
_sass/uright/_components.scss                 # CREATE — cards, badges, callouts, code, tables, chips, mermaid
_data/uright.yml                              # CREATE — category map + about-card content
_includes/uright-icon.html                    # CREATE — <svg><use> sprite helper
_includes/category-color.html                 # CREATE — category → color/icon resolver
_includes/titlebar.html                       # CREATE
_includes/explorer.html                       # CREATE
_includes/right-rail.html                     # CREATE
_includes/statusbar.html                      # CREATE
_layouts/default.html                         # CREATE (overrides gem) — IDE shell grid
assets/fonts/                                 # CREATE — Geist + Geist Mono woff2
assets/img/lucide-sprite.svg                  # CREATE — inline SVG sprite
assets/js/uright-drawers.js                   # CREATE — mobile drawer toggles
_config.yml                                    # MODIFY — theme_mode dark, feature flags
_posts/*.md                                    # MODIFY — re-tag 17 posts to 4 categories
_tabs/about.md                                 # MODIFY — IDE about layout content
```

---

# PHASE 1 — Foundation (tokens, fonts, icons, data)

### Task 1: SCSS entry point + token layer

**Files:**
- Create: `assets/css/jekyll-theme-chirpy.scss`
- Create: `_sass/uright/_tokens.scss`

**Interfaces:**
- Produces: a CSS `:root` block exposing every uright token as a custom property (`--gray-950`…`--white`, `--accent-100`…`--accent-900`, `--accent-contrast`, semantic hues, alpha tints, `--surface-*`, `--text-*`, `--border-*`, `--action-*`, `--status-*`, `--shadow-*`, `--glow-accent`, `--ring-focus`, `--dur-*`, `--ease-*`). Later tasks reference these by name.

- [ ] **Step 1: Create the entry point that imports Chirpy then the uright tree**

Create `assets/css/jekyll-theme-chirpy.scss` (the `---` front-matter fences are required so Jekyll processes it):

```scss
---
---

/* prettier-ignore */
@use 'main
{%- if jekyll.environment == 'production' -%}
  .bundle
{%- endif -%}
';

/* uright Studio theme overrides */
@use 'uright/tokens';
@use 'uright/fonts';
@use 'uright/chirpy-bridge';
@use 'uright/base';
@use 'uright/chrome';
@use 'uright/components';
@use 'uright/views';
```

> Note: the later `@use` lines reference partials created in subsequent tasks. They will fail to build until those files exist. To keep the build green per-task, comment out the not-yet-created `@use` lines and uncomment each as its file is created. For THIS task, keep only `tokens` and `fonts`-through-`views` commented except `tokens`. (Simplest: add `@use 'uright/tokens';` now, add the rest as you create them.)

For this task, the file ends with only:

```scss
/* uright Studio theme overrides */
@use 'uright/tokens';
```

- [ ] **Step 2: Create `_sass/uright/_tokens.scss` with all tokens verbatim**

Copy values from `docs/design/blog_theme/tokens/colors.css` and `elevation.css`. Full content:

```scss
:root {
  /* ---- surfaces (deepest → highest) ---- */
  --gray-950: #0a0b0d;
  --gray-900: #0f1113;
  --gray-850: #131519;
  --gray-800: #16181c;
  --gray-750: #1a1d22;
  --gray-700: #1f232a;
  --gray-600: #272b33;
  --gray-500: #353a44;
  --gray-400: #4a515c;
  --gray-300: #6b7280;
  --gray-200: #8b94a1;
  --gray-150: #a8b0bb;
  --gray-100: #c8cdd5;
  --gray-50:  #e6e9ee;
  --white:    #f3f5f8;

  /* ---- accent ramp ---- */
  --accent-100: #ffe7d6;
  --accent-200: #ffcaa6;
  --accent-300: #ffa973;
  --accent-400: #ff8a44;
  --accent-500: #f26a21;
  --accent-600: #db5715;
  --accent-700: #b5440f;
  --accent-800: #8a340c;
  --accent-900: #5e230a;
  --accent-contrast: #1f0d04;

  /* ---- semantic hues ---- */
  --green-500: #34d399;
  --amber-500: #f5b544;
  --amber-600: #e09a1f;
  --red-500: #f0584f;
  --red-600: #dc4138;
  --blue-500: #4aa3ff;
  --blue-600: #2f8ae8;
  --violet-500: #9d7bff;
  --agent-datadoug: #4cc9b0;

  /* ---- alpha tints ---- */
  --accent-alpha-08: rgba(242, 106, 33, 0.08);
  --accent-alpha-12: rgba(242, 106, 33, 0.12);
  --accent-alpha-16: rgba(242, 106, 33, 0.16);
  --accent-alpha-24: rgba(242, 106, 33, 0.24);
  --accent-alpha-40: rgba(242, 106, 33, 0.40);
  --white-alpha-04: rgba(255, 255, 255, 0.04);
  --white-alpha-06: rgba(255, 255, 255, 0.06);
  --white-alpha-08: rgba(255, 255, 255, 0.08);
  --white-alpha-10: rgba(255, 255, 255, 0.10);
  --white-alpha-14: rgba(255, 255, 255, 0.14);
  --black-alpha-30: rgba(0, 0, 0, 0.30);
  --black-alpha-50: rgba(0, 0, 0, 0.50);

  /* ---- semantic aliases ---- */
  --surface-canvas: var(--gray-950);
  --surface-panel: var(--gray-900);
  --surface-raised: var(--gray-800);
  --surface-overlay: var(--gray-750);
  --surface-sunken: var(--gray-850);
  --surface-hover: var(--white-alpha-04);
  --surface-active: var(--white-alpha-08);
  --surface-selected: var(--accent-alpha-12);

  --text-primary: var(--white);
  --text-secondary: var(--gray-150);
  --text-tertiary: var(--gray-300);
  --text-muted: var(--gray-200);
  --text-disabled: var(--gray-400);
  --text-accent: var(--accent-400);
  --text-on-accent: var(--accent-contrast);
  --text-link: var(--accent-400);

  --border-subtle: var(--white-alpha-06);
  --border-default: var(--white-alpha-10);
  --border-strong: var(--white-alpha-14);
  --border-accent: var(--accent-alpha-40);
  --border-focus: var(--accent-500);

  --action-primary: var(--accent-500);
  --action-primary-hover: var(--accent-400);
  --action-primary-active: var(--accent-600);
  --focus-ring: var(--accent-alpha-40);

  --status-success: var(--green-500);
  --status-success-bg: rgba(52, 211, 153, 0.12);
  --status-warning: var(--amber-500);
  --status-warning-bg: rgba(245, 181, 68, 0.12);
  --status-danger: var(--red-500);
  --status-danger-bg: rgba(240, 88, 79, 0.12);
  --status-info: var(--blue-500);
  --status-info-bg: rgba(74, 163, 255, 0.12);

  --graph-edge: var(--white-alpha-14);
  --graph-node-bg: var(--gray-800);

  /* ---- elevation ---- */
  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.30);
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.40), 0 1px 1px rgba(0, 0, 0, 0.24);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.45), 0 1px 2px rgba(0, 0, 0, 0.30);
  --shadow-lg: 0 12px 32px rgba(0, 0, 0, 0.55), 0 2px 6px rgba(0, 0, 0, 0.35);
  --shadow-xl: 0 24px 60px rgba(0, 0, 0, 0.62), 0 4px 12px rgba(0, 0, 0, 0.40);
  --shadow-popover: 0 12px 32px rgba(0, 0, 0, 0.55), 0 0 0 1px var(--white-alpha-08);
  --glow-accent: 0 0 0 1px var(--accent-alpha-40), 0 4px 20px rgba(242, 106, 33, 0.24);
  --glow-accent-soft: 0 0 20px rgba(242, 106, 33, 0.18);
  --ring-focus: 0 0 0 2px var(--surface-canvas), 0 0 0 4px var(--accent-alpha-40);
  --ring-focus-tight: 0 0 0 2px var(--accent-alpha-40);
  --inset-top-highlight: inset 0 1px 0 var(--white-alpha-06);
  --inset-input: inset 0 1px 2px rgba(0, 0, 0, 0.35);

  /* ---- motion ---- */
  --dur-instant: 80ms;
  --dur-fast: 130ms;
  --dur-base: 190ms;
  --dur-slow: 280ms;
  --dur-slower: 420ms;
  --ease-standard: cubic-bezier(0.2, 0, 0.2, 1);
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);

  /* ---- chrome dimensions ---- */
  --titlebar-h: 48px;
  --statusbar-h: 26px;
  --explorer-w: 286px;
  --rail-w: 264px;
  --tab-h: 36px;

  /* ---- radii ---- */
  --radius-xs: 4px;
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 10px;
  --radius-xl: 12px;
  --radius-2xl: 16px;
  --radius-pill: 999px;
}
```

- [ ] **Step 3: Ensure `theme_mode: dark` is set in `_config.yml`**

Open `_config.yml`, find the `theme_mode:` key (Chirpy ships it commented or empty). Set:

```yaml
theme_mode: dark
```

- [ ] **Step 4: Build and verify tokens reach the output CSS**

Run: `bundle exec jekyll build`
Expected: completes with no SCSS errors.

Run: `grep -c "\-\-accent-500: #f26a21" _site/assets/css/jekyll-theme-chirpy.css`
Expected: `1` (the token is present in compiled output).

- [ ] **Step 5: Commit**

```bash
git add assets/css/jekyll-theme-chirpy.scss _sass/uright/_tokens.scss _config.yml
git commit -m "feat(theme): add SCSS entry point and uright token layer"
```

---

### Task 2: Self-hosted fonts

**Files:**
- Create: `assets/fonts/` (woff2 files)
- Create: `_sass/uright/_fonts.scss`
- Modify: `assets/css/jekyll-theme-chirpy.scss` (uncomment `@use 'uright/fonts';`)

**Interfaces:**
- Produces: CSS font families `Geist` and `Geist Mono` available via `@font-face`; a `--font-sans` and `--font-mono` custom property for consumers.

- [ ] **Step 1: Download Geist + Geist Mono woff2 into `assets/fonts/`**

Geist is OFL-licensed (Vercel). Download the woff2 weights used by the design (400/500/600/700 for Geist; 400/500/600 for Geist Mono).

Run:

```bash
mkdir -p assets/fonts
cd assets/fonts
# Geist (sans) weights
for w in 400 500 600 700; do
  curl -fsSL -o "geist-$w.woff2" "https://cdn.jsdelivr.net/fontsource/fonts/geist@latest/latin-$w-normal.woff2"
done
# Geist Mono weights
for w in 400 500 600; do
  curl -fsSL -o "geist-mono-$w.woff2" "https://cdn.jsdelivr.net/fontsource/fonts/geist-mono@latest/latin-$w-normal.woff2"
done
cd ../..
ls -la assets/fonts/
```

Expected: 7 `.woff2` files, each > 5 KB. If any download is 0 bytes or fails, stop and report — do NOT fall back to the Google `@import`.

- [ ] **Step 2: Create `_sass/uright/_fonts.scss`**

```scss
@font-face {
  font-family: 'Geist';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('/assets/fonts/geist-400.woff2') format('woff2');
}
@font-face {
  font-family: 'Geist';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url('/assets/fonts/geist-500.woff2') format('woff2');
}
@font-face {
  font-family: 'Geist';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url('/assets/fonts/geist-600.woff2') format('woff2');
}
@font-face {
  font-family: 'Geist';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url('/assets/fonts/geist-700.woff2') format('woff2');
}
@font-face {
  font-family: 'Geist Mono';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('/assets/fonts/geist-mono-400.woff2') format('woff2');
}
@font-face {
  font-family: 'Geist Mono';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url('/assets/fonts/geist-mono-500.woff2') format('woff2');
}
@font-face {
  font-family: 'Geist Mono';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url('/assets/fonts/geist-mono-600.woff2') format('woff2');
}

:root {
  --font-sans: 'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
}
```

- [ ] **Step 3: Enable the import in the entry point**

In `assets/css/jekyll-theme-chirpy.scss`, ensure this line is present and uncommented:

```scss
@use 'uright/fonts';
```

- [ ] **Step 4: Build and verify**

Run: `bundle exec jekyll build`
Expected: clean build.

Run: `grep -c "font-family: 'Geist'" _site/assets/css/jekyll-theme-chirpy.css`
Expected: `>= 1`.

Run: `ls _site/assets/fonts/*.woff2 | wc -l`
Expected: `7`.

- [ ] **Step 5: Commit**

```bash
git add assets/fonts _sass/uright/_fonts.scss assets/css/jekyll-theme-chirpy.scss
git commit -m "feat(theme): self-host Geist and Geist Mono fonts"
```

---

### Task 3: Lucide icon sprite + helper include

**Files:**
- Create: `assets/img/lucide-sprite.svg`
- Create: `_includes/uright-icon.html`

**Interfaces:**
- Produces: an SVG `<symbol id="lucide-NAME">` per glyph; `{% include uright-icon.html name="folder" class="..." %}` renders `<svg class="ur-icon ..."><use href="/assets/img/lucide-sprite.svg#lucide-folder"/></svg>`.

- [ ] **Step 1: Build the sprite from Lucide source**

Lucide ships individual SVGs (ISC license). Assemble a single sprite with one `<symbol>` per needed glyph. Needed names (from spec): `search, file-text, folder, folder-open, chevron-right, command, terminal, database, git-branch, git-commit, network, zap, sparkles, bot, refresh-cw, trash-2, message-square, clock, calendar, hash, rss, github, linkedin, link, copy, external-link, list-tree, sliders-horizontal, layers, triangle-alert, arrow-right, x, menu, info, panel-right`.

Generate it:

```bash
mkdir -p assets/img
NAMES="search file-text folder folder-open chevron-right command terminal database git-branch git-commit network zap sparkles bot refresh-cw trash-2 message-square clock calendar hash rss github linkedin link copy external-link list-tree sliders-horizontal layers triangle-alert arrow-right x menu info panel-right"
{
  echo '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">'
  for n in $NAMES; do
    body=$(curl -fsSL "https://cdn.jsdelivr.net/npm/lucide-static@latest/icons/$n.svg" \
      | sed -e 's/.*<svg[^>]*>//' -e 's#</svg>##')
    echo "  <symbol id=\"lucide-$n\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\">$body</symbol>"
  done
  echo '</svg>'
} > assets/img/lucide-sprite.svg
grep -c '<symbol' assets/img/lucide-sprite.svg
```

Expected: the final `grep -c` prints `35` (one symbol per name). If any symbol body is empty (curl failed for a name), stop and report which name failed.

- [ ] **Step 2: Create the helper include `_includes/uright-icon.html`**

```liquid
{%- comment -%} Renders a Lucide glyph from the sprite. Params: name (required), class (optional), size (optional, default 24). {%- endcomment -%}
{%- assign sz = include.size | default: 24 -%}
<svg class="ur-icon {{ include.class }}" width="{{ sz }}" height="{{ sz }}" aria-hidden="true" focusable="false">
  <use href="{{ '/assets/img/lucide-sprite.svg' | relative_url }}#lucide-{{ include.name }}"></use>
</svg>
```

- [ ] **Step 3: Add base icon styling to tokens-adjacent base (temporary inline check)**

No SCSS needed yet (base styles come in Task 5). For now verify the include renders by adding a temporary reference. Skip styling; just confirm Liquid compiles in Step 4.

- [ ] **Step 4: Build and verify the sprite ships and include compiles**

Add a one-line temporary use to `_tabs/about.md` body (top of file content, after front matter): `{% include uright-icon.html name="terminal" %}` — then:

Run: `bundle exec jekyll build`
Expected: clean build (proves the include has no Liquid errors).

Run: `grep -c 'lucide-sprite.svg#lucide-terminal' _site/about/index.html`
Expected: `>= 1`.

Run: `ls -la _site/assets/img/lucide-sprite.svg`
Expected: file exists, > 2 KB.

Then REMOVE the temporary `{% include uright-icon.html name="terminal" %}` line from `_tabs/about.md`.

- [ ] **Step 5: Commit**

```bash
git add assets/img/lucide-sprite.svg _includes/uright-icon.html
git commit -m "feat(theme): add Lucide icon sprite and include helper"
```

---

### Task 4: Category data + resolver include

**Files:**
- Create: `_data/uright.yml`
- Create: `_includes/category-color.html`

**Interfaces:**
- Produces: `site.data.uright.categories` (a list of `{name, slug, color, icon, description}`); `{% include category-color.html category="AI & LLMs" field="color" %}` outputs the resolved value (color hex via `var(--token)`, or icon name, or description), with a neutral fallback for unknown categories.

- [ ] **Step 1: Create `_data/uright.yml`**

```yaml
# uright Studio theme data — category map + about-card content.

categories:
  - name: "AI & LLMs"
    slug: "ai-llms"
    color: "var(--blue-500)"
    icon: "sparkles"
    description: "Working with large language models, inference, and AI tooling."
  - name: "Claude Code"
    slug: "claude-code"
    color: "var(--violet-500)"
    icon: "terminal"
    description: "Tips, workflows, and setups for the Claude Code CLI."
  - name: "DevOps"
    slug: "devops"
    color: "var(--agent-datadoug)"
    icon: "git-branch"
    description: "Infrastructure, tooling, and developer environment notes."
  - name: "Quick Tips"
    slug: "quick-tips"
    color: "var(--amber-500)"
    icon: "zap"
    description: "Short, practical tips you can apply in a few minutes."

fallback:
  color: "var(--text-tertiary)"
  icon: "file-text"
  description: ""

# Right-rail About card.
about:
  initials: "JW"
  name: "Jack Wong"
  role: "Enterprise Architect · tech evangelist"
  bio: "Building with LLMs in the open — notes on AI tooling, Claude Code, and dev workflows."
  popular_tags: [claude-code, litellm, aws, openwebui, llm]
```

- [ ] **Step 2: Create `_includes/category-color.html`**

```liquid
{%- comment -%}
Resolves a category to a field from _data/uright.yml.
Params: category (required, the category name), field (color|icon|description|slug).
Falls back to site.data.uright.fallback for unknown categories.
{%- endcomment -%}
{%- assign _field = include.field | default: 'color' -%}
{%- assign _match = nil -%}
{%- for c in site.data.uright.categories -%}
  {%- if c.name == include.category -%}{%- assign _match = c -%}{%- endif -%}
{%- endfor -%}
{%- if _match -%}
  {%- case _field -%}
    {%- when 'color' -%}{{ _match.color }}
    {%- when 'icon' -%}{{ _match.icon }}
    {%- when 'description' -%}{{ _match.description }}
    {%- when 'slug' -%}{{ _match.slug }}
  {%- endcase -%}
{%- else -%}
  {%- case _field -%}
    {%- when 'color' -%}{{ site.data.uright.fallback.color }}
    {%- when 'icon' -%}{{ site.data.uright.fallback.icon }}
    {%- else -%}{{ site.data.uright.fallback.description }}
  {%- endcase -%}
{%- endif -%}
```

- [ ] **Step 3: Build and verify the resolver works for known + unknown categories**

Temporarily append to `_tabs/about.md` body: `KNOWN:{% include category-color.html category="Claude Code" field="icon" %} UNKNOWN:{% include category-color.html category="Nope" field="icon" %}`

Run: `bundle exec jekyll build`
Run: `grep -o 'KNOWN:[a-z-]* UNKNOWN:[a-z-]*' _site/about/index.html`
Expected: `KNOWN:terminal UNKNOWN:file-text`

Then REMOVE the temporary line from `_tabs/about.md`.

- [ ] **Step 4: Commit**

```bash
git add _data/uright.yml _includes/category-color.html
git commit -m "feat(theme): add category data map and resolver include"
```

---

# PHASE 2 — Chrome shell (layout grid + regions + drawers)

> **Phase 2 checkpoint:** after Task 9, the site should render with the full IDE chrome on desktop and working drawers on mobile, even if individual views are not yet restyled.

### Task 5: Base styles + Chirpy bridge

**Files:**
- Create: `_sass/uright/_base.scss`
- Create: `_sass/uright/_chirpy-bridge.scss`
- Modify: `assets/css/jekyll-theme-chirpy.scss` (enable `@use` for both)

**Interfaces:**
- Consumes: tokens from Task 1, `--font-sans`/`--font-mono` from Task 2.
- Produces: global body/canvas styling, scrollbar styling, `.ur-icon` sizing, focus rings, reduced-motion guard; Chirpy color variables pointed at uright tokens.

- [ ] **Step 1: Create `_sass/uright/_base.scss`**

```scss
html {
  scrollbar-color: var(--gray-600) transparent;
}

body {
  background: var(--surface-canvas);
  color: var(--text-primary);
  font-family: var(--font-sans);
  -webkit-font-smoothing: antialiased;
}

code, pre, kbd, .ur-mono {
  font-family: var(--font-mono);
}

/* Thin scrollbars on scrollable panels */
.ur-scroll {
  scrollbar-width: thin;
  scrollbar-color: var(--gray-600) transparent;
}
.ur-scroll::-webkit-scrollbar { width: 10px; height: 10px; }
.ur-scroll::-webkit-scrollbar-track { background: transparent; }
.ur-scroll::-webkit-scrollbar-thumb {
  background: var(--gray-600);
  border-radius: var(--radius-pill);
  border: 2px solid transparent;
  background-clip: content-box;
}

.ur-icon {
  display: inline-block;
  flex: none;
  vertical-align: middle;
  color: currentColor;
}

:focus-visible {
  outline: none;
  box-shadow: var(--ring-focus);
  border-radius: var(--radius-sm);
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: 0.001ms !important;
    animation-duration: 0.001ms !important;
  }
}
```

- [ ] **Step 2: Create `_sass/uright/_chirpy-bridge.scss`**

Point Chirpy's CSS variables (used by its un-overridden components) at uright tokens. Chirpy 7.x exposes these under `:root` / `[data-mode="dark"]`.

```scss
html[data-mode="dark"],
:root {
  --main-bg: var(--surface-canvas);
  --mask-bg: var(--surface-panel);
  --main-border-color: var(--border-subtle);

  --text-color: var(--text-secondary);
  --text-muted-color: var(--text-tertiary);
  --heading-color: var(--text-primary);
  --link-color: var(--text-link);
  --link-underline-color: var(--accent-alpha-40);

  --card-bg: var(--surface-raised);
  --card-border-color: var(--border-subtle);
  --card-box-shadow: var(--shadow-sm);

  --button-bg: var(--surface-raised);
  --btn-border-color: var(--border-default);

  --blockquote-border-color: var(--border-strong);
  --blockquote-text-color: var(--text-muted);

  --code-bg: var(--surface-sunken);
  --code-color: var(--accent-300);
  --code-border-color: var(--border-subtle);
  --highlight-bg-color: var(--surface-sunken);

  --tb-border-color: var(--border-subtle);
  --tb-odd-bg: var(--surface-sunken);
  --tb-even-bg: var(--surface-panel);
}
```

- [ ] **Step 3: Enable both imports in the entry point**

In `assets/css/jekyll-theme-chirpy.scss`, ensure present:

```scss
@use 'uright/chirpy-bridge';
@use 'uright/base';
```

- [ ] **Step 4: Build and verify**

Run: `bundle exec jekyll build`
Expected: clean build.

Run: `grep -c "\-\-main-bg: var(\-\-surface-canvas)" _site/assets/css/jekyll-theme-chirpy.css`
Expected: `>= 1`.

- [ ] **Step 5: Commit**

```bash
git add _sass/uright/_base.scss _sass/uright/_chirpy-bridge.scss assets/css/jekyll-theme-chirpy.scss
git commit -m "feat(theme): add base styles and Chirpy variable bridge"
```

---

### Task 6: Titlebar partial

**Files:**
- Create: `_includes/titlebar.html`
- Modify: `_sass/uright/_chrome.scss` (create file; add titlebar styles)
- Modify: `assets/css/jekyll-theme-chirpy.scss` (enable `@use 'uright/chrome';`)

**Interfaces:**
- Consumes: `site.title`, `site.social.links`, `site.posts`, the current `page` for breadcrumb/active-nav; `uright-icon.html`.
- Produces: a `<header class="ur-titlebar">` element with breadcrumb (`.ur-breadcrumb`), search trigger (`.ur-search`), nav (`.ur-nav`), social (`.ur-social`), and two mobile toggle buttons (`#ur-explorer-toggle`, `#ur-rail-toggle`). The toggles are wired by JS in Task 9.

- [ ] **Step 1: Create `_includes/titlebar.html`**

```liquid
{%- comment -%} Builds the breadcrumb path from page context. {%- endcomment -%}
{%- assign crumb = 'home' -%}
{%- if page.layout == 'post' -%}{%- assign crumb = 'posts / ' | append: page.title -%}
{%- elsif page.layout == 'archives' -%}{%- assign crumb = 'archives' -%}
{%- elsif page.layout == 'categories' or page.layout == 'category' -%}{%- assign crumb = 'categories' -%}
{%- elsif page.layout == 'tags' or page.layout == 'tag' -%}{%- assign crumb = 'tags' -%}
{%- elsif page.url == '/about/' -%}{%- assign crumb = 'about' -%}
{%- else -%}{%- assign crumb = 'posts' -%}{%- endif -%}

<header class="ur-titlebar">
  <button id="ur-explorer-toggle" class="ur-icon-btn ur-mobile-only" aria-label="Toggle explorer" aria-expanded="false">
    {% include uright-icon.html name="menu" size=20 %}
  </button>

  <a class="ur-wordmark" href="{{ '/' | relative_url }}">
    <span class="ur-dot" aria-hidden="true"></span>
    <span class="ur-wordmark-text">uright</span>
    <span class="ur-chip">blog</span>
  </a>

  <nav class="ur-breadcrumb ur-mono" aria-label="Breadcrumb">
    <span class="ur-crumb-root">~/</span><span class="ur-crumb-path">{{ crumb }}</span>
  </nav>

  <button class="ur-search" id="ur-search-trigger" aria-label="Search posts">
    {% include uright-icon.html name="search" size=16 %}
    <span class="ur-search-placeholder">Search posts…</span>
    <kbd class="ur-kbd">⌘K</kbd>
  </button>

  <nav class="ur-nav" aria-label="Primary">
    <a href="{{ '/' | relative_url }}" class="ur-nav-link{% if page.layout == 'home' %} active{% endif %}">Home</a>
    <a href="{{ '/archives/' | relative_url }}" class="ur-nav-link{% if page.layout == 'archives' %} active{% endif %}">Archives</a>
    <a href="{{ '/categories/' | relative_url }}" class="ur-nav-link{% if page.layout == 'categories' or page.layout == 'category' %} active{% endif %}">Categories</a>
    <a href="{{ '/tags/' | relative_url }}" class="ur-nav-link{% if page.layout == 'tags' or page.layout == 'tag' %} active{% endif %}">Tags</a>
    <a href="{{ '/about/' | relative_url }}" class="ur-nav-link{% if page.url == '/about/' %} active{% endif %}">About</a>
  </nav>

  <div class="ur-social">
    {%- for link in site.social.links -%}
      {%- if link contains 'github' -%}<a href="{{ link }}" class="ur-icon-btn" aria-label="GitHub">{% include uright-icon.html name="github" size=18 %}</a>{%- endif -%}
      {%- if link contains 'linkedin' -%}<a href="{{ link }}" class="ur-icon-btn" aria-label="LinkedIn">{% include uright-icon.html name="linkedin" size=18 %}</a>{%- endif -%}
    {%- endfor -%}
    <a href="{{ '/feed.xml' | relative_url }}" class="ur-icon-btn ur-rss" aria-label="RSS">{% include uright-icon.html name="rss" size=18 %}</a>
  </div>

  <button id="ur-rail-toggle" class="ur-icon-btn ur-mobile-only" aria-label="Toggle info panel" aria-expanded="false">
    {% include uright-icon.html name="info" size=20 %}
  </button>
</header>
```

- [ ] **Step 2: Create `_sass/uright/_chrome.scss` with titlebar styles**

```scss
/* ===== IDE grid shell (filled in Task 9; placeholder vars used now) ===== */

/* ===== Titlebar ===== */
.ur-titlebar {
  display: flex;
  align-items: center;
  gap: 14px;
  height: var(--titlebar-h);
  padding: 0 12px;
  background: var(--surface-panel);
  border-bottom: 1px solid var(--border-subtle);
}

.ur-wordmark {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: var(--text-primary);
}
.ur-dot {
  width: 9px; height: 9px; border-radius: 50%;
  background: var(--accent-500);
  box-shadow: 0 0 10px var(--accent-alpha-40);
}
.ur-wordmark-text { font-size: 16px; font-weight: 600; letter-spacing: -0.02em; }
.ur-chip {
  font-family: var(--font-mono); font-size: 11px;
  color: var(--accent-contrast); background: var(--accent-500);
  border-radius: 5px; padding: 2px 6px;
}

.ur-breadcrumb { font-size: 12px; max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ur-crumb-root { color: var(--text-muted); }
.ur-crumb-path { color: var(--text-secondary); }

.ur-search {
  display: flex; align-items: center; gap: 8px;
  width: 300px; height: 32px; margin-left: auto;
  padding: 0 10px;
  background: var(--surface-sunken);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  box-shadow: var(--inset-input);
  color: var(--text-tertiary);
  cursor: pointer;
  transition: var(--transition-colors, all var(--dur-fast) var(--ease-standard));
}
.ur-search:hover { border-color: var(--border-default); }
.ur-search-placeholder { font-size: 13px; }
.ur-kbd {
  margin-left: auto; font-family: var(--font-mono); font-size: 11px;
  color: var(--text-tertiary); background: var(--surface-raised);
  border: 1px solid var(--border-subtle); border-radius: var(--radius-xs);
  padding: 1px 5px;
}

.ur-nav { display: flex; gap: 2px; }
.ur-nav-link {
  font-size: 13px; font-weight: 500; text-decoration: none;
  color: var(--text-tertiary);
  padding: 6px 10px; border-radius: var(--radius-md);
  transition: all var(--dur-fast) var(--ease-standard);
}
.ur-nav-link:hover { color: var(--text-primary); background: var(--surface-hover); }
.ur-nav-link.active { color: var(--text-primary); background: var(--surface-active); }

.ur-social { display: flex; gap: 2px; }
.ur-icon-btn {
  display: inline-flex; align-items: center; justify-content: center;
  width: 30px; height: 30px; border-radius: var(--radius-md);
  background: transparent; border: none; color: var(--text-tertiary);
  cursor: pointer;
  transition: all var(--dur-fast) var(--ease-standard);
}
.ur-icon-btn:hover { color: var(--text-primary); background: var(--surface-hover); }
.ur-rss { color: var(--accent-400); }

.ur-mobile-only { display: none; }
```

- [ ] **Step 3: Enable chrome import**

In `assets/css/jekyll-theme-chirpy.scss` ensure: `@use 'uright/chrome';`

- [ ] **Step 4: Verify it compiles (full wiring happens in Task 9)**

Run: `bundle exec jekyll build`
Expected: clean build.

Run: `grep -c "ur-titlebar" _site/assets/css/jekyll-theme-chirpy.css`
Expected: `>= 1`.

> The partial isn't included in any layout yet — that happens in Task 9. This task verifies styles compile and the include has no Liquid errors (proven in Task 9's build).

- [ ] **Step 5: Commit**

```bash
git add _includes/titlebar.html _sass/uright/_chrome.scss assets/css/jekyll-theme-chirpy.scss
git commit -m "feat(theme): add titlebar partial and styles"
```

---

### Task 7: Explorer + status bar partials

**Files:**
- Create: `_includes/explorer.html`
- Create: `_includes/statusbar.html`
- Modify: `_sass/uright/_chrome.scss` (append explorer + statusbar styles)

**Interfaces:**
- Consumes: `site.categories`, `site.posts`, `site.data.uright`, `uright-icon.html`, `category-color.html`.
- Produces: `<nav class="ur-explorer ur-scroll">` and `<footer class="ur-statusbar">`.

- [ ] **Step 1: Create `_includes/explorer.html`**

```liquid
<nav class="ur-explorer ur-scroll" aria-label="Explorer">
  <div class="ur-explorer-head">
    <span class="ur-eyebrow">EXPLORER</span>
    <span class="ur-explorer-actions">
      {% include uright-icon.html name="list-tree" size=16 %}
      {% include uright-icon.html name="refresh-cw" size=16 %}
    </span>
  </div>

  <div class="ur-section">
    <div class="ur-section-title ur-eyebrow">CATEGORIES</div>
    {%- for c in site.data.uright.categories -%}
      {%- assign posts_in = site.categories[c.name] -%}
      <a class="ur-folder-row" href="{{ '/categories/' | append: c.slug | append: '/' | relative_url }}">
        {% include uright-icon.html name="chevron-right" size=14 class="ur-chevron" %}
        <span class="ur-folder-icon" style="color: {{ c.color }}">{% include uright-icon.html name=c.icon size=16 %}</span>
        <span class="ur-folder-name">{{ c.name }}</span>
        <span class="ur-count ur-mono">{{ posts_in.size | default: 0 }}</span>
      </a>
    {%- endfor -%}
  </div>

  <div class="ur-section">
    <div class="ur-section-title ur-eyebrow">RECENT POSTS</div>
    {%- assign recent = site.posts | slice: 0, 8 -%}
    {%- for post in recent -%}
      {%- assign cat = post.categories | last -%}
      {%- capture catcolor %}{% include category-color.html category=cat field="color" %}{% endcapture -%}
      <a class="ur-file-row" href="{{ post.url | relative_url }}">
        <span class="ur-file-icon" style="color: {{ catcolor }}">{% include uright-icon.html name="file-text" size=15 %}</span>
        <span class="ur-file-body">
          <span class="ur-file-title">{{ post.title }}</span>
          <span class="ur-file-date ur-mono">{{ post.date | date: '%Y-%m-%d' }}</span>
        </span>
      </a>
    {%- endfor -%}
  </div>

  <div class="ur-explorer-foot">
    {% include uright-icon.html name="rss" size=15 %}
    <a href="{{ '/feed.xml' | relative_url }}">Subscribe to the feed</a>
    <span class="ur-mono ur-muted">atom.xml</span>
  </div>
</nav>
```

- [ ] **Step 2: Create `_includes/statusbar.html`**

```liquid
{%- assign host = site.url | remove: 'https://' | remove: 'http://' -%}
<footer class="ur-statusbar ur-mono">
  <span class="ur-status-item">{% include uright-icon.html name="git-branch" size=12 %} main</span>
  <span class="ur-status-item">▤ {{ site.posts.size }} posts</span>
  <span class="ur-status-item">jekyll · chirpy</span>
  <span class="ur-status-spacer"></span>
  <span class="ur-status-item ur-status-rss">RSS</span>
  <span class="ur-status-item">{{ host | default: 'blog.uright.ai' }}</span>
  <span class="ur-status-item ur-status-deployed"><span class="ur-green-dot"></span> deployed</span>
</footer>
```

- [ ] **Step 3: Append explorer + statusbar styles to `_sass/uright/_chrome.scss`**

```scss
/* ===== Explorer ===== */
.ur-explorer {
  width: var(--explorer-w);
  background: var(--surface-panel);
  border-right: 1px solid var(--border-subtle);
  overflow-y: auto;
  padding-bottom: 12px;
}
.ur-explorer-head {
  display: flex; align-items: center; justify-content: space-between;
  height: 36px; padding: 0 12px;
}
.ur-explorer-actions { display: flex; gap: 4px; color: var(--text-tertiary); }
.ur-eyebrow {
  font-size: 10px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.06em; color: var(--text-tertiary);
}
.ur-section { padding: 6px 0; }
.ur-section-title { padding: 6px 12px; }

.ur-folder-row, .ur-file-row {
  display: flex; align-items: center; gap: 6px;
  padding: 0 12px; text-decoration: none;
  transition: background var(--dur-fast) var(--ease-standard);
}
.ur-folder-row { height: 30px; }
.ur-folder-row:hover, .ur-file-row:hover { background: var(--surface-hover); }
.ur-folder-name { font-size: 13px; color: var(--text-secondary); flex: 1; }
.ur-chevron { color: var(--text-tertiary); }
.ur-count { font-size: 11px; color: var(--text-tertiary); }

.ur-file-row { min-height: 34px; padding-left: 26px; align-items: flex-start; padding-top: 5px; padding-bottom: 5px; }
.ur-file-body { display: flex; flex-direction: column; min-width: 0; }
.ur-file-title {
  font-size: 12.5px; font-weight: 500; color: var(--text-secondary);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 210px;
}
.ur-file-date { font-size: 10px; color: var(--text-tertiary); }

.ur-explorer-foot {
  display: flex; align-items: center; gap: 6px;
  height: 38px; padding: 0 12px; margin-top: 8px;
  border-top: 1px solid var(--border-subtle);
  font-size: 12px; color: var(--text-tertiary);
}
.ur-explorer-foot a { color: var(--text-secondary); text-decoration: none; }
.ur-muted { color: var(--text-tertiary); }

/* ===== Status bar ===== */
.ur-statusbar {
  display: flex; align-items: center; gap: 16px;
  height: var(--statusbar-h); padding: 0 14px;
  background: var(--surface-panel);
  border-top: 1px solid var(--border-subtle);
  font-size: 11px; color: var(--text-tertiary);
}
.ur-status-item { display: inline-flex; align-items: center; gap: 5px; }
.ur-status-spacer { flex: 1; }
.ur-status-rss { color: var(--accent-400); }
.ur-green-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--green-500); display: inline-block; }
```

- [ ] **Step 4: Verify compile**

Run: `bundle exec jekyll build`
Expected: clean build.

Run: `grep -c "ur-explorer" _site/assets/css/jekyll-theme-chirpy.css`
Expected: `>= 1`.

- [ ] **Step 5: Commit**

```bash
git add _includes/explorer.html _includes/statusbar.html _sass/uright/_chrome.scss
git commit -m "feat(theme): add explorer and status bar partials"
```

---

### Task 8: Right rail partial (About card + Outline)

**Files:**
- Create: `_includes/right-rail.html`
- Modify: `_sass/uright/_chrome.scss` (append right-rail styles)

**Interfaces:**
- Consumes: `site.data.uright.about`, `page.layout`, `site.posts`, Chirpy's TOC (`#toc` / Tocbot mount); `uright-icon.html`.
- Produces: `<aside class="ur-rail ur-scroll">` containing either `.ur-outline` (post pages) or `.ur-about-card` (everything else).

- [ ] **Step 1: Create `_includes/right-rail.html`**

```liquid
<aside class="ur-rail ur-scroll" aria-label="Context panel">
{%- if page.layout == 'post' -%}
  <div class="ur-outline">
    <div class="ur-eyebrow">ON THIS PAGE</div>
    <nav class="ur-toc" id="toc"></nav>

    <div class="ur-eyebrow ur-outline-section">DETAILS</div>
    <dl class="ur-detail-table ur-mono">
      {%- assign cat = page.categories | last -%}
      <div><dt>category</dt><dd>{{ cat }}</dd></div>
      <div><dt>published</dt><dd>{{ page.date | date: '%Y-%m-%d' }}</dd></div>
      <div><dt>words</dt><dd>{{ content | number_of_words }}</dd></div>
      <div><dt>reading</dt><dd>{% include read-time.html content=content %}</dd></div>
    </dl>

    <div class="ur-eyebrow ur-outline-section">SHARE</div>
    <div class="ur-share">
      {% include uright-icon.html name="link" size=18 %}
      {% include uright-icon.html name="message-square" size=18 %}
      {% include uright-icon.html name="external-link" size=18 %}
    </div>
  </div>
{%- else -%}
  {%- assign a = site.data.uright.about -%}
  <div class="ur-about-card">
    <div class="ur-avatar">{{ a.initials }}</div>
    <div class="ur-about-name">{{ a.name }}</div>
    <div class="ur-about-role ur-mono">{{ a.role }}</div>
    <p class="ur-about-bio">{{ a.bio }}</p>
    <div class="ur-about-social">
      {%- for link in site.social.links -%}
        {%- if link contains 'github' -%}<a href="{{ link }}" class="ur-icon-btn" aria-label="GitHub">{% include uright-icon.html name="github" size=18 %}</a>{%- endif -%}
        {%- if link contains 'linkedin' -%}<a href="{{ link }}" class="ur-icon-btn" aria-label="LinkedIn">{% include uright-icon.html name="linkedin" size=18 %}</a>{%- endif -%}
      {%- endfor -%}
    </div>

    <div class="ur-eyebrow ur-about-section">POPULAR TAGS</div>
    <div class="ur-tag-chips">
      {%- for t in a.popular_tags -%}<a class="ur-tag-chip ur-mono" href="{{ '/tags/' | append: t | relative_url }}">#{{ t }}</a>{%- endfor -%}
    </div>

    <div class="ur-eyebrow ur-about-section">STATS</div>
    <dl class="ur-detail-table ur-mono">
      <div><dt>posts</dt><dd>{{ site.posts.size }}</dd></div>
      <div><dt>categories</dt><dd>{{ site.data.uright.categories.size }}</dd></div>
      <div><dt>tags</dt><dd>{{ site.tags.size }}</dd></div>
    </dl>
  </div>
{%- endif -%}
</aside>
```

- [ ] **Step 2: Append right-rail styles to `_sass/uright/_chrome.scss`**

```scss
/* ===== Right rail ===== */
.ur-rail {
  width: var(--rail-w);
  background: var(--surface-panel);
  border-left: 1px solid var(--border-subtle);
  overflow-y: auto;
  padding: 16px 14px;
}
.ur-outline-section, .ur-about-section { margin-top: 20px; margin-bottom: 8px; display: block; }

/* TOC (Tocbot mount restyle) */
.ur-toc :is(ul, ol) { list-style: none; padding-left: 0; margin: 0; }
.ur-toc a {
  display: block; padding: 4px 0 4px 12px;
  font-size: 13px; color: var(--text-tertiary); text-decoration: none;
  border-left: 2px solid transparent;
}
.ur-toc a:hover { color: var(--text-secondary); }
.ur-toc a.is-active-link, .ur-toc .toc-active > a {
  color: var(--accent-400); border-left-color: var(--accent-500);
}

.ur-detail-table { font-size: 12px; }
.ur-detail-table > div { display: flex; justify-content: space-between; padding: 4px 8px; }
.ur-detail-table dt { color: var(--text-tertiary); margin: 0; }
.ur-detail-table dd { color: var(--text-secondary); margin: 0; }
.ur-detail-table { background: var(--surface-sunken); border-radius: var(--radius-md); padding: 4px 0; }

.ur-share { display: flex; gap: 8px; color: var(--text-tertiary); }

/* About card */
.ur-avatar {
  width: 40px; height: 40px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: 600; color: var(--text-primary);
  background: var(--surface-sunken);
  box-shadow: 0 0 0 2px var(--accent-500);
}
.ur-about-name { font-size: 15px; font-weight: 600; margin-top: 10px; }
.ur-about-role { font-size: 11px; color: var(--text-tertiary); }
.ur-about-bio { font-size: 13px; color: var(--text-secondary); line-height: 1.6; margin: 10px 0; }
.ur-about-social { display: flex; gap: 4px; }
.ur-tag-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.ur-tag-chip {
  font-size: 11px; color: var(--text-secondary); text-decoration: none;
  background: var(--surface-sunken); border: 1px solid var(--border-subtle);
  border-radius: var(--radius-pill); padding: 3px 8px;
}
.ur-tag-chip:hover { border-color: var(--border-accent); color: var(--accent-300); }
```

- [ ] **Step 3: Verify compile**

Run: `bundle exec jekyll build`
Expected: clean build.

Run: `grep -c "ur-about-card" _site/assets/css/jekyll-theme-chirpy.css`
Expected: `>= 1`.

- [ ] **Step 4: Commit**

```bash
git add _includes/right-rail.html _sass/uright/_chrome.scss
git commit -m "feat(theme): add right-rail partial with about card and outline"
```

---

### Task 9: IDE shell layout + grid + mobile drawers

**Files:**
- Create: `_layouts/default.html` (overrides the gem's)
- Create: `assets/js/uright-drawers.js`
- Modify: `_sass/uright/_chrome.scss` (prepend the grid shell + drawer styles)

**Interfaces:**
- Consumes: all four chrome partials; Chirpy's `head.html`, `refactor-content.html`, `footer.html`, `js-selector.html` for content processing + script loading; Chirpy's search modal.
- Produces: the assembled page. This is the integration task — after it, the chrome renders on every page.

- [ ] **Step 1: Create `_layouts/default.html`**

Model the head/script includes on the gem's `default.html` (read `/Users/jack/.rbenv/.../jekyll-theme-chirpy-7.3.0/_layouts/default.html`). Keep Chirpy's `head.html`, content refactor, search modal, and JS so search/TOC/copy keep working.

```liquid
---
layout: compress
---

<!doctype html>
{% include origin-type.html %}
{% include lang.html %}
{% capture prefer_mode %}data-mode="dark"{% endcapture %}
<html lang="{{ page.lang | default: site.alt_lang | default: site.lang }}" {{ prefer_mode }}>
  {% include head.html %}
  <body>
    <div class="ur-shell">
      {% include titlebar.html %}
      <div class="ur-body">
        {% include explorer.html %}
        <main class="ur-main ur-scroll" aria-label="Main Content">
          <div class="ur-content">
            {% if layout.refactor or layout.layout == 'default' %}
              {% include refactor-content.html content=content lang=lang %}
            {% else %}
              {{ content }}
            {% endif %}
            {% for _include in layout.tail_includes %}
              {% assign _include_path = _include | append: '.html' %}
              {% include {{ _include_path }} lang=lang %}
            {% endfor %}
          </div>
        </main>
        {% include right-rail.html %}
      </div>
      {% include statusbar.html %}
    </div>

    <!-- mobile drawer scrim -->
    <div class="ur-scrim" id="ur-scrim" hidden></div>

    <!-- Chirpy search modal + mask (keeps ⌘K search working) -->
    <div id="mask"></div>
    {% include_cached search-results.html lang=lang %}

    {% include js-selector.html lang=lang %}
    {% if site.pwa.enabled %}{% include_cached pwa-loader.html %}{% endif %}
    <script src="{{ '/assets/js/uright-drawers.js' | relative_url }}" defer></script>
  </body>
</html>
```

> If `pwa-loader.html` does not exist in the gem, omit that line — check with `ls /Users/jack/.rbenv/.../jekyll-theme-chirpy-7.3.0/_includes/ | grep pwa`. The other includes (`js-selector.html`, `search-results.html`, `refactor-content.html`) are confirmed present.

- [ ] **Step 2: Prepend grid shell + drawer styles to `_sass/uright/_chrome.scss`**

```scss
/* ===== IDE grid shell ===== */
.ur-shell {
  display: grid;
  grid-template-rows: var(--titlebar-h) 1fr var(--statusbar-h);
  height: 100vh;
  height: 100dvh;
}
.ur-body {
  display: grid;
  grid-template-columns: var(--explorer-w) 1fr var(--rail-w);
  min-height: 0;
}
.ur-main { overflow-y: auto; background: var(--surface-canvas); }
.ur-content { max-width: 860px; margin: 0 auto; }

.ur-scrim {
  position: fixed; inset: 0; background: var(--black-alpha-50);
  z-index: 40; opacity: 0; transition: opacity var(--dur-base) var(--ease-standard);
}
.ur-scrim.is-open { opacity: 1; }

/* ===== Mobile drawers ===== */
@media (max-width: 1024px) {
  .ur-body { grid-template-columns: 1fr; }
  .ur-mobile-only { display: inline-flex; }
  .ur-search { width: auto; }
  .ur-search-placeholder, .ur-kbd { display: none; }
  .ur-nav, .ur-breadcrumb { display: none; }

  .ur-explorer, .ur-rail {
    position: fixed; top: var(--titlebar-h); bottom: var(--statusbar-h);
    z-index: 50; transition: transform var(--dur-base) var(--ease-out);
  }
  .ur-explorer { left: 0; transform: translateX(-100%); }
  .ur-rail { right: 0; transform: translateX(100%); }
  .ur-explorer.is-open, .ur-rail.is-open { transform: translateX(0); }
}

@media (max-width: 600px) {
  .ur-explorer { width: 86vw; }
  .ur-rail { width: 86vw; }
}
```

- [ ] **Step 3: Create `assets/js/uright-drawers.js`**

```js
(function () {
  var scrim = document.getElementById('ur-scrim');
  var explorer = document.querySelector('.ur-explorer');
  var rail = document.querySelector('.ur-rail');
  var expBtn = document.getElementById('ur-explorer-toggle');
  var railBtn = document.getElementById('ur-rail-toggle');

  function close() {
    if (explorer) explorer.classList.remove('is-open');
    if (rail) rail.classList.remove('is-open');
    if (scrim) { scrim.classList.remove('is-open'); scrim.hidden = true; }
    if (expBtn) expBtn.setAttribute('aria-expanded', 'false');
    if (railBtn) railBtn.setAttribute('aria-expanded', 'false');
  }

  function open(panel, btn) {
    close();
    if (panel) panel.classList.add('is-open');
    if (scrim) { scrim.hidden = false; requestAnimationFrame(function () { scrim.classList.add('is-open'); }); }
    if (btn) btn.setAttribute('aria-expanded', 'true');
  }

  if (expBtn) expBtn.addEventListener('click', function () {
    explorer && explorer.classList.contains('is-open') ? close() : open(explorer, expBtn);
  });
  if (railBtn) railBtn.addEventListener('click', function () {
    rail && rail.classList.contains('is-open') ? close() : open(rail, railBtn);
  });
  if (scrim) scrim.addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
})();
```

- [ ] **Step 4: Build, serve, and verify the chrome renders**

Run: `bundle exec jekyll build`
Expected: clean build.

Run: `grep -c "ur-titlebar" _site/index.html`
Expected: `>= 1` (titlebar is now in the rendered page).

Run: `grep -c "ur-explorer" _site/index.html && grep -c "ur-statusbar" _site/index.html`
Expected: both `>= 1`.

Manual: `bundle exec jekyll serve` → open http://localhost:4000 → confirm: titlebar at top, Explorer left with category folders + recent post titles, status bar at bottom, About card in right rail. Resize browser below 1024px → confirm hamburger + info buttons appear and toggle the drawers with scrim.

- [ ] **Step 5: Commit**

```bash
git add _layouts/default.html assets/js/uright-drawers.js _sass/uright/_chrome.scss
git commit -m "feat(theme): assemble IDE shell layout with grid and mobile drawers"
```

---

# PHASE 3 — Views + content re-tagging

> **Phase 3 checkpoint:** after Task 15, all six views render in the uright style with real content, and posts use the 4-category taxonomy.

### Task 10: Components — cards, badges, callouts, tables, chips

**Files:**
- Create: `_sass/uright/_components.scss`
- Modify: `assets/css/jekyll-theme-chirpy.scss` (enable `@use 'uright/components';`)

**Interfaces:**
- Produces: reusable classes `.ur-card`, `.ur-badge`, `.ur-eyebrow` (already in chrome; keep single definition there — do NOT redefine), `.ur-thumb`, `.ur-callout`, styled article tables, `#tag` chips. Consumed by view tasks.

- [ ] **Step 1: Create `_sass/uright/_components.scss`**

```scss
/* ===== Eyebrow accent variant ===== */
.ur-eyebrow-accent { color: var(--accent-400); }

/* ===== Category badge ===== */
.ur-badge {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 11px; font-weight: 500;
  padding: 2px 8px; border-radius: var(--radius-pill);
  border: 1px solid currentColor;
  /* color set inline per-category via style attr */
}

/* ===== Thumbnail tile ===== */
.ur-thumb {
  display: flex; align-items: center; justify-content: center;
  background: var(--surface-sunken);
  border-radius: var(--radius-lg);
  flex: none;
  overflow: hidden;
}
.ur-thumb img { width: 100%; height: 100%; object-fit: cover; }

/* ===== Cards ===== */
.ur-card {
  background: var(--surface-raised);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: transform var(--dur-fast) var(--ease-out), border-color var(--dur-fast) var(--ease-standard);
}
.ur-card:hover { transform: translateY(-1px); border-color: var(--border-strong); }

/* ===== Callout (warning) ===== */
.ur-callout, .prompt-warning {
  display: flex; gap: 10px;
  background: var(--status-warning-bg);
  border-left: 3px solid var(--amber-500);
  border-radius: var(--radius-md);
  padding: 12px 14px; margin: 18px 0;
  color: var(--text-secondary);
}

/* ===== Article tables ===== */
.ur-content table, .content table {
  width: 100%; border-collapse: collapse; margin: 18px 0; font-size: 14px;
}
.ur-content thead th, .content thead th {
  background: var(--gray-850); color: var(--text-secondary);
  text-align: left; padding: 8px 12px; border-bottom: 1px solid var(--border-subtle);
}
.ur-content tbody td, .content tbody td {
  padding: 8px 12px; border-bottom: 1px solid var(--border-subtle); color: var(--gray-100);
}

/* ===== #tag chips (article footer + tags view) ===== */
.ur-hashtag {
  font-family: var(--font-mono); font-size: 13px;
  color: var(--text-secondary); text-decoration: none;
  background: var(--surface-sunken); border: 1px solid var(--border-subtle);
  border-radius: var(--radius-pill); padding: 3px 10px; white-space: nowrap;
}
.ur-hashtag:hover { color: var(--accent-300); border-color: var(--border-accent); }
```

- [ ] **Step 2: Enable import**

In `assets/css/jekyll-theme-chirpy.scss` ensure: `@use 'uright/components';`

- [ ] **Step 3: Build and verify**

Run: `bundle exec jekyll build`
Run: `grep -c "ur-callout" _site/assets/css/jekyll-theme-chirpy.css`
Expected: `>= 1`.

- [ ] **Step 4: Commit**

```bash
git add _sass/uright/_components.scss assets/css/jekyll-theme-chirpy.scss
git commit -m "feat(theme): add shared component styles"
```

---

### Task 11: Re-tag the 17 posts to the 4-category model

**Files:**
- Modify: all 17 files in `_posts/*.md` (front-matter `categories:` line only)

**Interfaces:**
- Produces: every post categorized as exactly one of `AI & LLMs`, `Claude Code`, `DevOps`, `Quick Tips`, matching `_data/uright.yml`.

- [ ] **Step 1: Apply the mapping from the spec**

Edit the `categories:` line in each file to the single new category (drop the `Tech` parent):

```
_posts/2024-01-27-private-gpt-clear-ingested-files.md            → categories: [AI & LLMs]
_posts/2024-02-01-codellama-instruct-13b-writing-snake-game.md   → categories: [AI & LLMs]
_posts/2024-07-29-unlocking-the-power-of-azure-openai-on-open-webui.md → categories: [AI & LLMs]
_posts/2024-08-11-how-i-identified-the-top-10-hugo-themes-with-chatgpt.md → categories: [AI & LLMs]
_posts/2026-02-16-using-aws-bedrock-models-from-openwebui.md     → categories: [AI & LLMs]
_posts/2026-03-14-using-github-copilot-models-via-litellm-proxy.md → categories: [AI & LLMs]
_posts/2026-01-07-docker-desktop-volume-backup-and-restore.md    → categories: [DevOps]
_posts/2026-02-08-sharing-git-credentials-between-wsl-and-windows-host.md → categories: [DevOps]
_posts/2026-02-09-managing-jekyll-blogs-with-openclaw-and-tailscale.md → categories: [DevOps]
_posts/2026-02-05-shiftenter-shortcut-key-solved-in-claude-code-antigravity.md → categories: [Claude Code]
_posts/2026-02-24-sound-notifications-for-claude-code-on-wsl.md  → categories: [Claude Code]
_posts/2026-02-28-quick-tip-switching-between-claude-profiles-on-anthropic-and-bedrock.md → categories: [Claude Code]
_posts/2026-03-02-run-claude-code-cli-on-your-github-copilot-subscription.md → categories: [Claude Code]
_posts/2026-03-15-sound-notifications-for-claude-code-on-macos.md → categories: [Claude Code]
_posts/2026-03-22-running-claude-code-for-free-with-nvidia-nim.md → categories: [Claude Code]
_posts/2026-02-04-quick-tip-installing-aws-cli-v2-with-uv-tool.md → categories: [Quick Tips]
_posts/2026-02-08-text-to-speech-tools-for-macos-and-windows-superwhisper-handy.md → categories: [Quick Tips]
```

For each file, use Edit to replace the existing `categories: [...]` line with the new single-category value.

- [ ] **Step 2: Verify the taxonomy**

Run: `cd _posts && grep -h "^categories:" *.md | sort | uniq -c; cd ..`
Expected:
```
   6 categories: [AI & LLMs]
   6 categories: [Claude Code]
   3 categories: [DevOps]
   2 categories: [Quick Tips]
```

- [ ] **Step 3: Build and confirm categories generate**

Run: `bundle exec jekyll build`
Run: `ls _site/categories/`
Expected: directories for the slugs Chirpy generates (e.g. `ai-llms` style — confirm Chirpy's category page generation picks up all 4).

- [ ] **Step 4: Commit**

```bash
git add _posts
git commit -m "content: re-tag posts to 4-category taxonomy"
```

---

### Task 12: Home view (featured + post list)

**Files:**
- Create: `_layouts/home.html` (overrides gem; renders featured + list)
- Modify: `_sass/uright/_views.scss` (create; add home styles)
- Modify: `assets/css/jekyll-theme-chirpy.scss` (enable `@use 'uright/views';`)
- Modify: `_config.yml` (add `uright:` feature flags)

**Interfaces:**
- Consumes: `site.posts`, `image.path`, `category-color.html`, `uright-icon.html`, `read-time.html`, `_config.yml` flags `site.uright.show_thumbnails` / `site.uright.show_descriptions`.
- Produces: the home page content (no chrome — chrome comes from `default.html` which `home` inherits via `layout: default` semantics; set `home.html` to use the shell).

- [ ] **Step 1: Add feature flags to `_config.yml`**

```yaml
uright:
  show_thumbnails: true
  show_descriptions: true
```

- [ ] **Step 2: Create `_layouts/home.html`**

```liquid
---
layout: default
refactor: true
---

{%- assign posts = site.posts -%}
{%- assign featured = posts | first -%}

<div class="ur-home">
  <div class="ur-home-head">
    <div class="ur-eyebrow ur-eyebrow-accent">JACK WONG · DEV NOTES</div>
    <h1 class="ur-h1">Building with LLMs, in the open.</h1>
    <p class="ur-home-sub">Notes on AI tooling, Claude Code, and the workflows behind shipping with large language models.</p>
  </div>

  {%- if featured -%}
  {%- assign fcat = featured.categories | last -%}
  {%- capture fcolor %}{% include category-color.html category=fcat field="color" %}{% endcapture -%}
  {%- capture ficon %}{% include category-color.html category=fcat field="icon" %}{% endcapture -%}
  <a class="ur-featured ur-card" href="{{ featured.url | relative_url }}">
    <div class="ur-featured-bar"></div>
    <div class="ur-featured-inner">
      <div class="ur-thumb ur-featured-thumb" style="color: {{ fcolor }}">
        {%- if featured.image.path and site.uright.show_thumbnails -%}
          <img src="{{ featured.image.path | relative_url }}" alt="{{ featured.image.alt | default: featured.title }}">
        {%- else -%}{% include uright-icon.html name=ficon size=34 %}{%- endif -%}
      </div>
      <div class="ur-featured-body">
        <div class="ur-featured-meta">
          <span class="ur-eyebrow ur-eyebrow-accent">FEATURED ·</span>
          <span class="ur-badge" style="color: {{ fcolor }}">{{ fcat }}</span>
        </div>
        <h2 class="ur-featured-title">{{ featured.title }}</h2>
        {%- if site.uright.show_descriptions -%}<p class="ur-featured-desc">{{ featured.description }}</p>{%- endif -%}
        <div class="ur-meta-row ur-mono">
          <span>{{ featured.date | date: '%Y-%m-%d' }}</span>
          <span>{% include uright-icon.html name="clock" size=13 %} {% include read-time.html content=featured.content %}</span>
          <span class="ur-read-link">Read post {% include uright-icon.html name="arrow-right" size=13 %}</span>
        </div>
      </div>
    </div>
  </a>
  {%- endif -%}

  <div class="ur-list-divider">
    <span class="ur-eyebrow">ALL POSTS</span>
    <span class="ur-count ur-mono">{{ posts.size }}</span>
    <span class="ur-sort ur-mono">⇄ Newest first</span>
  </div>

  <div class="ur-post-list">
    {%- for post in posts offset: 1 -%}
    {%- assign cat = post.categories | last -%}
    {%- capture color %}{% include category-color.html category=cat field="color" %}{% endcapture -%}
    {%- capture icon %}{% include category-color.html category=cat field="icon" %}{% endcapture -%}
    <a class="ur-post-card ur-card" href="{{ post.url | relative_url }}">
      {%- if site.uright.show_thumbnails -%}
      <div class="ur-thumb ur-post-thumb" style="color: {{ color }}">
        {%- if post.image.path -%}<img src="{{ post.image.path | relative_url }}" alt="{{ post.image.alt | default: post.title }}">
        {%- else -%}{% include uright-icon.html name=icon size=22 %}{%- endif -%}
      </div>
      {%- endif -%}
      <div class="ur-post-body">
        <div class="ur-post-meta">
          <span class="ur-badge" style="color: {{ color }}">{{ cat }}</span>
          <span class="ur-mono ur-muted">{{ post.date | date: '%Y-%m-%d' }} · {% include read-time.html content=post.content %}</span>
        </div>
        <h3 class="ur-post-title">{{ post.title }}</h3>
        {%- if site.uright.show_descriptions -%}<p class="ur-post-desc">{{ post.description }}</p>{%- endif -%}
      </div>
    </a>
    {%- endfor -%}
  </div>
</div>
```

- [ ] **Step 3: Create `_sass/uright/_views.scss` with home styles**

```scss
/* ===== Home ===== */
.ur-home { padding: 30px 40px 80px; max-width: 780px; margin: 0 auto; }
.ur-home-head { margin-bottom: 28px; }
.ur-h1 { font-size: 32px; font-weight: 600; letter-spacing: -0.02em; margin: 8px 0; color: var(--text-primary); }
.ur-home-sub { font-size: 15px; color: var(--text-secondary); line-height: 1.6; }

.ur-featured { position: relative; display: block; padding: 0; overflow: hidden; border-radius: var(--radius-xl); text-decoration: none; }
.ur-featured-bar { height: 2px; background: linear-gradient(90deg, var(--accent-500), var(--accent-300)); }
.ur-featured-inner { display: flex; gap: 18px; padding: 18px; }
.ur-featured-thumb { width: 104px; height: 104px; }
.ur-featured-body { display: flex; flex-direction: column; gap: 8px; min-width: 0; }
.ur-featured-meta { display: flex; align-items: center; gap: 8px; }
.ur-featured-title { font-size: 21px; font-weight: 600; color: var(--text-primary); margin: 0; }
.ur-featured-desc { font-size: 14px; color: var(--text-secondary); margin: 0; }
.ur-meta-row { display: flex; gap: 14px; font-size: 12px; color: var(--text-tertiary); align-items: center; }
.ur-read-link { color: var(--accent-400); display: inline-flex; align-items: center; gap: 4px; }

.ur-list-divider { display: flex; align-items: center; gap: 10px; margin: 28px 0 14px; }
.ur-sort { margin-left: auto; color: var(--text-tertiary); }

.ur-post-list { display: flex; flex-direction: column; gap: 10px; }
.ur-post-card { display: flex; gap: 14px; padding: 14px; text-decoration: none; }
.ur-post-thumb { width: 62px; height: 62px; }
.ur-post-body { display: flex; flex-direction: column; gap: 5px; min-width: 0; }
.ur-post-meta { display: flex; align-items: center; gap: 8px; font-size: 11px; }
.ur-post-title { font-size: 15px; font-weight: 600; color: var(--text-primary); margin: 0; }
.ur-post-desc {
  font-size: 13px; color: var(--text-secondary); margin: 0;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}

@media (max-width: 1024px) { .ur-home { padding: 24px 18px 60px; } }
```

- [ ] **Step 4: Enable views import**

In `assets/css/jekyll-theme-chirpy.scss` ensure: `@use 'uright/views';`

- [ ] **Step 5: Build, serve, verify**

Run: `bundle exec jekyll build`
Run: `grep -c "ur-featured" _site/index.html`
Expected: `>= 1`.

Manual: serve → home shows the featured card (most recent post) with accent hairline + thumbnail/fallback glyph, then the stacked list. Toggle `show_thumbnails: false` in `_config.yml`, rebuild, confirm thumbnails disappear; revert to `true`.

- [ ] **Step 6: Commit**

```bash
git add _layouts/home.html _sass/uright/_views.scss assets/css/jekyll-theme-chirpy.scss _config.yml
git commit -m "feat(theme): style home view with featured card and post list"
```

---

### Task 13: Post view (tab strip, article, code blocks, mermaid)

**Files:**
- Create: `_layouts/post.html` (overrides gem; wraps Chirpy post content with tab strip)
- Modify: `_sass/uright/_views.scss` (append post styles)
- Modify: `_sass/uright/_components.scss` (append code-block + mermaid styles)

**Interfaces:**
- Consumes: gem's `post.html` structure (read it first), `category-color.html`, Chirpy's TOC + clipboard. The right-rail Outline (Task 8) already activates on `layout == 'post'`.
- Produces: a post page with the editor tab strip + styled article. Keep Chirpy's content pipeline (it injects TOC anchors, image lazyload, clipboard).

- [ ] **Step 1: Read the gem's post layout to preserve its content blocks**

Run: `cat /Users/jack/.rbenv/versions/3.4.4/lib/ruby/gems/3.4.0/gems/jekyll-theme-chirpy-7.3.0/_layouts/post.html`
Note which includes it uses (e.g. `related-posts`, `post-nav`, comments, `tail_includes`). Reuse them inside the new layout's content area so functionality is preserved.

- [ ] **Step 2: Create `_layouts/post.html`**

```liquid
---
layout: default
refactor: true
panel_includes:
  - toc
tail_includes:
  - related-posts
  - post-nav
  - comments
---

{%- assign cat = page.categories | last -%}
{%- capture color %}{% include category-color.html category=cat field="color" %}{% endcapture -%}

<div class="ur-tabstrip">
  <div class="ur-tab active">
    <span style="color: var(--violet-500)">{% include uright-icon.html name="file-text" size=15 %}</span>
    <span class="ur-tab-title">{{ page.title }}</span>
    {% include uright-icon.html name="x" size=14 class="ur-tab-close" %}
  </div>
  <div class="ur-tab dimmed"><span class="ur-tab-title">README.md</span></div>
  <span class="ur-tab-lang ur-mono">markdown</span>
</div>

<article class="ur-article">
  <div class="ur-article-meta">
    <span class="ur-badge" style="color: {{ color }}">{{ cat }}</span>
    <span class="ur-mono ur-muted">{{ page.date | date: '%Y-%m-%d' }}</span>
  </div>
  <h1 class="ur-article-h1">{{ page.title }}</h1>
  {%- if page.description -%}<p class="ur-lead">{{ page.description }}</p>{%- endif -%}
  <div class="ur-byline">
    <span class="ur-byline-avatar">JW</span>
    <span>{{ site.social.name }}</span>
    <span class="ur-mono ur-muted">{% include uright-icon.html name="clock" size=13 %} {% include read-time.html content=content %}</span>
  </div>

  <div class="ur-content-body content">
    {{ content }}
  </div>

  <div class="ur-tags-row">
    {%- for tag in page.tags -%}
      <a class="ur-hashtag" href="{{ '/tags/' | append: tag | relative_url }}">#{{ tag }}</a>
    {%- endfor -%}
  </div>
</article>
```

> `content` here is the already-refactored content from `default.html`'s `refactor-content` include — Chirpy will have added heading anchors, image wrappers, and clipboard buttons. Do NOT re-run refactor.

- [ ] **Step 3: Append post + byline styles to `_sass/uright/_views.scss`**

```scss
/* ===== Post ===== */
.ur-tabstrip {
  position: sticky; top: 0; z-index: 5;
  display: flex; align-items: center; gap: 2px;
  height: var(--tab-h); padding: 0 8px;
  background: var(--surface-panel); border-bottom: 1px solid var(--border-subtle);
}
.ur-tab {
  position: relative; display: flex; align-items: center; gap: 6px;
  height: var(--tab-h); padding: 0 12px;
  font-size: 12.5px; font-weight: 500; color: var(--text-secondary);
}
.ur-tab.active { background: var(--surface-canvas); }
.ur-tab.active::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: var(--accent-500); }
.ur-tab.dimmed { color: var(--text-tertiary); opacity: 0.6; }
.ur-tab-title { max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ur-tab-close { color: var(--text-tertiary); }
.ur-tab-lang { margin-left: auto; font-size: 11px; color: var(--text-tertiary); }

.ur-article { max-width: 760px; margin: 0 auto; padding: 34px 44px 90px; }
.ur-article-meta { display: flex; align-items: center; gap: 8px; }
.ur-article-h1 { font-size: 34px; font-weight: 600; letter-spacing: -0.022em; color: var(--text-primary); margin: 14px 0; }
.ur-lead { font-size: 16px; line-height: 1.6; color: var(--text-secondary); }
.ur-byline {
  display: flex; align-items: center; gap: 10px; font-size: 13px; color: var(--text-secondary);
  padding-bottom: 16px; border-bottom: 1px solid var(--border-subtle); margin-bottom: 24px;
}
.ur-byline-avatar {
  width: 24px; height: 24px; border-radius: 50%; font-size: 10px; font-weight: 600;
  display: flex; align-items: center; justify-content: center;
  background: var(--surface-sunken); box-shadow: 0 0 0 1px var(--accent-500); color: var(--text-primary);
}

/* Article body typography */
.ur-content-body { font-size: 15.5px; line-height: 1.72; color: var(--gray-100); }
.ur-content-body h2 { font-size: 21px; font-weight: 600; letter-spacing: -0.015em; color: var(--text-primary); margin: 32px 0 12px; }
.ur-content-body :not(pre) > code {
  font-family: var(--font-mono); font-size: 0.85em;
  background: var(--surface-sunken); border: 1px solid var(--border-subtle);
  color: var(--accent-300); border-radius: var(--radius-xs); padding: 1px 5px;
}
.ur-content-body a { color: var(--accent-400); text-decoration-color: var(--accent-alpha-40); }

.ur-tags-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 28px; padding-top: 18px; border-top: 1px solid var(--border-subtle); }

@media (max-width: 1024px) { .ur-article { padding: 24px 18px 60px; } }
```

- [ ] **Step 4: Append code-block + mermaid styles to `_sass/uright/_components.scss`**

```scss
/* ===== Code blocks (restyle Chirpy/Rouge) ===== */
.ur-content-body div.highlighter-rouge, .content div.highlighter-rouge {
  background: var(--surface-sunken);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  overflow: hidden; margin: 18px 0;
}
.ur-content-body .highlight, .content .highlight { background: var(--surface-sunken); }
.ur-content-body .highlight pre, .content .highlight pre {
  font-family: var(--font-mono); font-size: 12.5px; line-height: 1.75;
  padding: 14px 16px; margin: 0; background: transparent;
}
/* Chirpy code header bar (filename + copy) */
.ur-content-body .code-header, .content .code-header {
  background: var(--gray-850); border-bottom: 1px solid var(--border-subtle);
  height: 36px; color: var(--text-tertiary);
}
.content .code-header .copy-badge, .content button.copy { color: var(--text-tertiary); }

/* Rouge token colors */
.highlight .nt, .highlight .k { color: var(--violet-500); }    /* keys / keywords */
.highlight .na { color: var(--blue-500); }                      /* sub-keys / attrs */
.highlight .s, .highlight .s2, .highlight .s1 { color: var(--green-500); } /* strings */
.highlight .kc, .highlight .m, .highlight .mi { color: var(--accent-300); } /* booleans / numbers */
.highlight .c, .highlight .c1, .highlight .cm, .highlight .gp { color: var(--text-tertiary); } /* comments / prompt */

/* ===== Mermaid diagram block ===== */
.ur-content-body .mermaid, .content .mermaid {
  background: var(--surface-sunken);
  background-image: radial-gradient(var(--white-alpha-04) 1px, transparent 1px);
  background-size: 16px 16px;
  border: 1px solid var(--border-subtle); border-radius: var(--radius-md);
  padding: 20px; margin: 18px 0;
}
.content .mermaid .node rect, .content .mermaid .node polygon {
  fill: var(--graph-node-bg); stroke: var(--border-default);
}
.content .mermaid .edgePath path { stroke: var(--graph-edge); }
```

- [ ] **Step 5: Build, serve, verify**

Run: `bundle exec jekyll build`
Run: `grep -c "ur-tabstrip" _site/posts/*/index.html 2>/dev/null | head -1` (or pick a known post URL)
Expected: `>= 1`.

Manual: serve → open the NVIDIA NIM post (has mermaid + code). Confirm: tab strip with post title + accent bar; styled H1/lead/byline; code block with header + copy button works; inline code chips; mermaid renders on the dot-grid surface; right-rail Outline shows TOC that highlights on scroll.

- [ ] **Step 6: Commit**

```bash
git add _layouts/post.html _sass/uright/_views.scss _sass/uright/_components.scss
git commit -m "feat(theme): style post view, code blocks, and mermaid"
```

---

### Task 14: Archives + Categories views

**Files:**
- Create: `_layouts/archives.html` (overrides gem)
- Create: `_layouts/categories.html` (overrides gem)
- Modify: `_sass/uright/_views.scss` (append archives + categories styles)

**Interfaces:**
- Consumes: `site.posts` grouped by year (archives), `site.categories` + `_data/uright.yml` (categories), helper includes.
- Produces: the git-log timeline (archives) and folder-card grid (categories).

- [ ] **Step 1: Create `_layouts/archives.html`**

```liquid
---
layout: default
---

<div class="ur-page">
  <div class="ur-eyebrow ur-eyebrow-accent">git log --all</div>
  <h1 class="ur-h1">Archives</h1>

  {%- assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" -%}
  {%- for year in posts_by_year -%}
  <section class="ur-year">
    <div class="ur-year-head">
      <span class="ur-year-num ur-mono">{{ year.name }}</span>
      <span class="ur-hairline"></span>
      <span class="ur-count-pill ur-mono">{{ year.items.size }} posts</span>
    </div>
    <div class="ur-timeline">
      {%- for post in year.items -%}
      {%- assign cat = post.categories | last -%}
      {%- capture color %}{% include category-color.html category=cat field="color" %}{% endcapture -%}
      <a class="ur-commit" href="{{ post.url | relative_url }}">
        <span class="ur-commit-date ur-mono">{{ post.date | date: '%b %d' }}</span>
        <span class="ur-commit-dot" style="box-shadow: 0 0 0 2px {{ color }}"></span>
        <span class="ur-commit-title">{{ post.title }}</span>
        <span class="ur-badge" style="color: {{ color }}">{{ cat }}</span>
      </a>
      {%- endfor -%}
    </div>
  </section>
  {%- endfor -%}
</div>
```

- [ ] **Step 2: Create `_layouts/categories.html`**

```liquid
---
layout: default
---

<div class="ur-page">
  <div class="ur-eyebrow ur-eyebrow-accent">~/posts</div>
  <h1 class="ur-h1">Categories</h1>

  <div class="ur-cat-grid">
    {%- for c in site.data.uright.categories -%}
    {%- assign posts_in = site.categories[c.name] -%}
    <a class="ur-cat-card ur-card" href="{{ '/categories/' | append: c.slug | append: '/' | relative_url }}">
      <div class="ur-cat-head">
        <span class="ur-cat-icon" style="color: {{ c.color }}">{% include uright-icon.html name=c.icon size=22 %}</span>
        <span class="ur-count-pill ur-mono">{{ posts_in.size | default: 0 }} posts</span>
      </div>
      <h2 class="ur-cat-name">{{ c.name }}</h2>
      <p class="ur-cat-desc">{{ c.description }}</p>
      <div class="ur-cat-recent">
        {%- assign recent3 = posts_in | slice: 0, 3 -%}
        {%- for post in recent3 -%}
        <span class="ur-cat-recent-item"><span class="ur-dot-sm" style="background: {{ c.color }}"></span>{{ post.title }}</span>
        {%- endfor -%}
      </div>
    </a>
    {%- endfor -%}
  </div>
</div>
```

> Chirpy's category pages (the per-category listing at `/categories/<slug>/`) are generated by the gem's `category.html` layout via the `jekyll-archives`-like generator. This `categories.html` is the index grid only. Verify in Step 4 that per-category links resolve; if Chirpy's generated slug differs from `_data/uright.yml` `slug`, adjust the `slug` values to match Chirpy's slugify output (lowercased, spaces→hyphens, `&` dropped).

- [ ] **Step 3: Append archives + categories styles to `_sass/uright/_views.scss`**

```scss
/* ===== Shared page wrapper ===== */
.ur-page { max-width: 820px; margin: 0 auto; padding: 30px 40px 80px; }
.ur-hairline { flex: 1; height: 1px; background: var(--border-subtle); }
.ur-count-pill { font-size: 11px; color: var(--text-tertiary); background: var(--surface-sunken); border-radius: var(--radius-pill); padding: 2px 10px; }

/* ===== Archives ===== */
.ur-year { margin-top: 28px; }
.ur-year-head { display: flex; align-items: center; gap: 12px; }
.ur-year-num { font-size: 22px; font-weight: 600; color: var(--text-primary); }
.ur-timeline { margin: 14px 0 0 8px; border-left: 2px solid var(--border-subtle); }
.ur-commit { display: flex; align-items: center; gap: 12px; padding: 8px 12px; text-decoration: none; position: relative; }
.ur-commit:hover { background: var(--surface-hover); }
.ur-commit-date { width: 54px; text-align: right; font-size: 12px; color: var(--text-tertiary); }
.ur-commit-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--surface-canvas); margin-left: -5px; }
.ur-commit-title { flex: 1; font-size: 14px; color: var(--text-secondary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

/* ===== Categories ===== */
.ur-cat-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; margin-top: 24px; }
.ur-cat-card { display: block; padding: 18px; text-decoration: none; }
.ur-cat-head { display: flex; align-items: center; justify-content: space-between; }
.ur-cat-icon { width: 42px; height: 42px; display: flex; align-items: center; justify-content: center; background: var(--surface-sunken); border-radius: var(--radius-lg); }
.ur-cat-name { font-size: 17px; font-weight: 600; color: var(--text-primary); margin: 12px 0 6px; }
.ur-cat-desc { font-size: 13px; color: var(--text-secondary); margin: 0 0 12px; }
.ur-cat-recent { border-top: 1px solid var(--border-subtle); padding-top: 10px; display: flex; flex-direction: column; gap: 6px; }
.ur-cat-recent-item { display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--text-tertiary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ur-dot-sm { width: 6px; height: 6px; border-radius: 50%; flex: none; }

@media (max-width: 1024px) { .ur-page { padding: 24px 18px 60px; } .ur-cat-grid { grid-template-columns: 1fr; } }
```

- [ ] **Step 4: Build, serve, verify**

Run: `bundle exec jekyll build`
Run: `grep -c "ur-timeline" _site/archives/index.html && grep -c "ur-cat-grid" _site/categories/index.html`
Expected: both `>= 1`.

Manual: serve → `/archives/` shows per-year git-log timeline with category-ringed dots; `/categories/` shows 4 folder cards with correct counts; click a card → resolves to Chirpy's per-category page (adjust `_data/uright.yml` slugs if any 404).

- [ ] **Step 5: Commit**

```bash
git add _layouts/archives.html _layouts/categories.html _sass/uright/_views.scss
git commit -m "feat(theme): style archives timeline and categories grid"
```

---

### Task 15: Tags view + About page

**Files:**
- Create: `_layouts/tags.html` (overrides gem)
- Modify: `_tabs/about.md` + create `_sass` rules for about (in `_views.scss`)
- Modify: `_sass/uright/_views.scss` (append tags + about styles)

**Interfaces:**
- Consumes: `site.tags`, `site.data.uright`, helper includes.
- Produces: the mono tag cloud (tags) and the IDE about page.

- [ ] **Step 1: Create `_layouts/tags.html`**

```liquid
---
layout: default
---

<div class="ur-page">
  <div class="ur-eyebrow ur-eyebrow-accent">grep -r #</div>
  <h1 class="ur-h1">Tags</h1>

  <div class="ur-tag-cloud ur-card">
    {%- assign tags = site.tags | sort -%}
    {%- for tag in tags -%}
    {%- assign n = tag[1].size -%}
    {%- assign sz = 'sm' -%}
    {%- if n >= 8 -%}{%- assign sz = 'xl' -%}
    {%- elsif n >= 5 -%}{%- assign sz = 'lg' -%}
    {%- elsif n >= 2 -%}{%- assign sz = 'md' -%}{%- endif -%}
    <a class="ur-cloud-tag ur-cloud-{{ sz }} ur-mono" href="{{ '/tags/' | append: tag[0] | relative_url }}">#{{ tag[0] }}<sup>{{ n }}</sup></a>
    {%- endfor -%}
  </div>
</div>
```

- [ ] **Step 2: Replace `_tabs/about.md` content with the IDE about layout**

Keep the front matter, replace the body. Use placeholder experience/education copy (flagged for the author).

```markdown
---
# the default layout is 'page'
icon: fas fa-info-circle
order: 4
layout: page
---

<div class="ur-about">
  <div class="ur-about-head">
    <div class="ur-eyebrow ur-mono">cat about.md</div>
    <div class="ur-about-id">
      <span class="ur-about-avatar-lg">JW</span>
      <div>
        <h1 class="ur-h1">Jack Wong</h1>
        <div class="ur-about-role ur-mono">Enterprise Architect · tech evangelist</div>
      </div>
      <div class="ur-about-pills">
        <a class="ur-pill" href="https://github.com/uright">GitHub</a>
        <a class="ur-pill" href="https://www.linkedin.com/in/jackwong3">LinkedIn</a>
      </div>
    </div>
  </div>

  <p class="ur-lead">Building with LLMs in the open. I write about AI tooling, Claude Code, and the workflows behind shipping with large language models.</p>

  <div class="ur-eyebrow ur-about-section">SKILLS</div>
  <div class="ur-skill-chips">
    <span class="ur-pill ur-mono">AWS Bedrock</span>
    <span class="ur-pill ur-mono">Azure OpenAI</span>
    <span class="ur-pill ur-mono">PGVector</span>
    <span class="ur-pill ur-mono">Qdrant</span>
    <span class="ur-pill ur-mono">LLMs &amp; deep learning</span>
    <span class="ur-pill ur-mono">Enterprise architecture</span>
  </div>

  <div class="ur-eyebrow ur-about-section">EXPERIENCE</div>
  <!-- TODO(author): replace with real experience entries -->
  <div class="ur-exp">
    <div class="ur-exp-item">
      <span class="ur-exp-dot current"></span>
      <div class="ur-exp-body">
        <div class="ur-exp-role">Enterprise Architect <span class="ur-mono ur-muted">present</span></div>
        <div class="ur-exp-company current">uright</div>
        <p class="ur-exp-desc">Placeholder — add role description.</p>
      </div>
    </div>
  </div>

  <div class="ur-eyebrow ur-about-section">EDUCATION</div>
  <div class="ur-edu ur-card">
    <span class="ur-edu-icon">{% include uright-icon.html name="layers" size=18 %}</span>
    <div>
      <div class="ur-edu-degree">B.Sc. Computer Science</div>
      <div class="ur-mono ur-muted">Honours Computer Science · Business Option</div>
    </div>
  </div>
</div>
```

> `layout: page` keeps Chirpy's page semantics but inherits our `default.html` shell (page → default). The about content is custom HTML inside the markdown.

- [ ] **Step 3: Append tags + about styles to `_sass/uright/_views.scss`**

```scss
/* ===== Tags cloud ===== */
.ur-tag-cloud { display: flex; flex-wrap: wrap; gap: 14px 18px; padding: 24px; margin-top: 24px; align-items: baseline; }
.ur-cloud-tag { text-decoration: none; white-space: nowrap; }
.ur-cloud-tag sup { font-size: 0.6em; margin-left: 2px; }
.ur-cloud-xl { font-size: 19px; font-weight: 600; color: var(--accent-300); }
.ur-cloud-lg { font-size: 16px; color: var(--text-secondary); }
.ur-cloud-md { font-size: 14px; color: var(--text-secondary); }
.ur-cloud-sm { font-size: 13px; color: var(--text-tertiary); }

/* ===== About ===== */
.ur-about { max-width: 760px; margin: 0 auto; padding: 30px 44px 80px; }
.ur-about-id { display: flex; align-items: center; gap: 16px; padding: 14px 0; border-bottom: 1px solid var(--border-subtle); }
.ur-about-avatar-lg {
  width: 56px; height: 56px; border-radius: 50%; flex: none;
  display: flex; align-items: center; justify-content: center;
  font-weight: 600; background: var(--surface-sunken); box-shadow: 0 0 0 2px var(--accent-500); color: var(--text-primary);
}
.ur-about-pills { margin-left: auto; display: flex; gap: 8px; }
.ur-pill {
  font-size: 12px; color: var(--text-secondary); text-decoration: none;
  background: var(--surface-sunken); border: 1px solid var(--border-default);
  border-radius: var(--radius-pill); padding: 4px 12px; display: inline-block;
}
.ur-pill:hover { border-color: var(--border-accent); color: var(--accent-300); }
.ur-skill-chips { display: flex; flex-wrap: wrap; gap: 8px; }

.ur-exp { display: flex; flex-direction: column; gap: 16px; border-left: 2px solid var(--border-subtle); margin-left: 6px; }
.ur-exp-item { display: flex; gap: 14px; position: relative; padding-left: 16px; }
.ur-exp-dot { width: 9px; height: 9px; border-radius: 50%; background: var(--surface-canvas); box-shadow: 0 0 0 2px var(--text-tertiary); position: absolute; left: -5px; top: 4px; }
.ur-exp-dot.current { box-shadow: 0 0 0 2px var(--accent-500); background: var(--accent-500); }
.ur-exp-role { font-size: 15px; font-weight: 600; color: var(--text-primary); }
.ur-exp-company { font-size: 13px; color: var(--text-secondary); }
.ur-exp-company.current { color: var(--accent-400); }
.ur-exp-desc { font-size: 13px; color: var(--text-secondary); margin: 4px 0 0; }

.ur-edu { display: flex; gap: 14px; align-items: center; padding: 16px; margin-top: 8px; }
.ur-edu-icon { width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; background: var(--surface-sunken); border-radius: var(--radius-lg); color: var(--text-secondary); }
.ur-edu-degree { font-size: 15px; font-weight: 600; color: var(--text-primary); }

@media (max-width: 1024px) { .ur-about { padding: 24px 18px 60px; } }
```

- [ ] **Step 4: Build, serve, verify**

Run: `bundle exec jekyll build`
Run: `grep -c "ur-tag-cloud" _site/tags/index.html && grep -c "ur-about" _site/about/index.html`
Expected: both `>= 1`.

Manual: serve → `/tags/` shows the mono cloud sized by frequency with superscript counts; `/about/` shows the IDE about page (avatar, skills, experience placeholder, education).

- [ ] **Step 5: Commit**

```bash
git add _layouts/tags.html _tabs/about.md _sass/uright/_views.scss
git commit -m "feat(theme): style tags cloud and about page"
```

---

# PHASE 4 — Polish + verification

### Task 16: Cross-view polish, interactions, and full verification

**Files:**
- Modify: any `_sass/uright/*.scss` as needed for fixes found during review.

**Interfaces:** none new — this is the integration/verification pass.

- [ ] **Step 1: Hover/press/focus pass**

Serve the site and check each interaction against the spec §Interactions:
- Cards lift 1px + border strengthens on hover (home list, category cards).
- Nav active state + hover wash works.
- Primary "Read post →" link is accent.
- Focus ring (Tab through nav/search/links) shows the 2px orange ring.
- Press: confirm no color inversion (the default is fine).

Fix any gaps inline in the relevant SCSS file, rebuild, recommit per fix.

- [ ] **Step 2: Mobile drawer pass at 3 widths**

Serve, use browser devtools responsive mode at 1200px (desktop, no drawers), 900px (drawers, hamburger+info), 375px (phone, 86vw drawers). Confirm:
- Drawers slide in/out, scrim closes them, Esc closes them.
- Content column is full-width and readable.
- Status bar + titlebar remain usable.

- [ ] **Step 3: Verify Chirpy functionality survived**

- `⌘K` (or click search) opens Chirpy's search and returns results.
- Code-block copy button copies.
- Post TOC in the right rail highlights the active section on scroll.
- RSS feed builds: `ls _site/feed.xml` exists.

If search/TOC are broken, confirm `js-selector.html` and `search-results.html` are included in `default.html` (Task 9) and that Chirpy's required mount points (`#toc`, `#mask`, search ids) are present.

- [ ] **Step 4: Full build + link check**

Run: `bundle exec jekyll build`
Expected: clean.

Run: `bundle exec htmlproofer _site --disable-external --allow-hash-href --ignore-empty-alt`
Expected: passes (0 failures). Fix any broken internal links/images surfaced.

- [ ] **Step 5: Reduced-motion + prefers check**

In devtools, emulate `prefers-reduced-motion: reduce`; confirm drawers snap (no slide) and transitions are disabled.

- [ ] **Step 6: Final commit**

```bash
git add -A
git commit -m "polish(theme): interactions, responsive, and verification fixes"
```

---

## Verification summary (definition of done)

- [ ] `bundle exec jekyll build` clean.
- [ ] `bundle exec htmlproofer _site --disable-external --allow-hash-href` passes.
- [ ] All 6 views render in uright style with real content (home, post, archives, categories, tags, about).
- [ ] IDE chrome (titlebar, Explorer, right rail, status bar) present on every page; Explorer shows category folders + recent post titles (titles, not filenames).
- [ ] Posts use the 4-category taxonomy (6 / 6 / 3 / 2).
- [ ] Self-hosted fonts load (no Google Fonts request); 7 woff2 files in `_site/assets/fonts/`.
- [ ] Lucide sprite ships and icons render via `<use>`.
- [ ] Mobile: drawers work at <1024px; content full-width.
- [ ] Chirpy search, code-copy, and TOC still function.
- [ ] `prefers-reduced-motion` respected.

## Open items handed to author (not blocking)

- Real About experience/education content (currently placeholder, marked `TODO(author)`).
- Real uright SVG logo (wordmark is typographic placeholder).
- Domain migration to `blog.uright.ai` (`url` + `CNAME`) — out of scope per spec.
- Lighthouse perf pass (optional validation of the self-hosted-font claim).
