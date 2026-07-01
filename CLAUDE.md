# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Jekyll static site for the uright tech blog (https://uright.ca), built on the
`jekyll-theme-chirpy` gem (~> 7.3). Content focuses on AI/LLM tooling, Claude Code,
DevOps, and quick tips. **The site does not use Chirpy's stock look** — it ships a
custom "uright Studio" theme: a dark, IDE-inspired reskin with its own layouts,
includes, and SCSS layered on top of the gem. Understanding that reskin is the main
thing needed to work here productively (see Architecture below).

## Commands

Dev server (Docker, no local Ruby needed):

```bash
docker-compose up --build          # serves at http://localhost:4000, LiveReload on 35729
docker-compose down
docker-compose run --rm jekyll bundle exec jekyll build   # production build
```

Dev server (local Ruby):

```bash
bundle install
bundle exec jekyll serve           # or: bash tools/run.sh   (add -p for production env)
JEKYLL_ENV=production bundle exec jekyll build
```

Link-check the built site (html-proofer is in the `:test` bundle group):

```bash
bundle exec htmlproofer _site
```

New blog post — prefer the `/new-post` slash command (skill in `.claude/skills/new-post/`),
which generates front matter, slug, and image dir interactively. CLI equivalent:

```bash
pip install -r tools/requirements.txt   # first time only
python3 tools/new-post.py -t "Title" -d "Description" -c "DevOps" --tags "a, b" [--mermaid] [--dry-run]
```

## Architecture: the uright Studio theme

The custom theme replaces Chirpy's sidebar/topbar shell with an IDE-style shell
(titlebar + file explorer + editor pane + right rail + status bar). The pieces:

- **`_layouts/default.html`** is the root shell every page renders through. It builds
  `.ur-shell` → titlebar / `.ur-body` (explorer + `.ur-main` + right-rail) / statusbar.
  Post layouts opt into the right-rail TOC via `panel_includes: [toc]`; the layout
  branches on that so `<article>` is a direct child of `<main>` (tocbot needs
  `main>article[data-toc="true"]`).
- **`_layouts/home.html`, `post.html`, `categories.html`, `tags.html`, `archives.html`**
  all set `layout: default` and render custom `.ur-*` markup (featured card, post list,
  editor tab strip, byline, etc.). They do **not** resemble stock Chirpy layouts.
- **`_includes/`** holds the custom chrome: `titlebar.html`, `explorer.html` (file-tree
  nav), `right-rail.html` (TOC + About card), `statusbar.html`, `uright-icon.html`
  (inline SVG icon set, referenced by `name=`), `category-color.html`.
- **`_data/uright.yml`** is the single source of truth for the **category → color/icon/
  description** map and the right-rail About card. `_includes/category-color.html`
  resolves a category name to any of those fields, falling back to `fallback:` for
  unknown categories. When adding a category, add it here or it renders with the
  fallback color/icon.

### SCSS (token-driven)

Entry point `assets/css/jekyll-theme-chirpy.scss` `@use`s Chirpy's compiled `main`,
then the uright layers **in order**:

`uright/tokens` → `fonts` → `chirpy-bridge` → `base` → `chrome` → `components` → `views`
(all in `_sass/uright/`).

- **`_tokens.scss`** — CSS custom properties: gray/accent ramps, semantic hues, alpha
  tints, and semantic aliases (`--surface-canvas`, `--text-primary`, etc.). Change
  colors here, not in component files.
- **`_chirpy-bridge.scss`** — repoints Chirpy's own CSS variables (`--main-bg`,
  `--card-bg`, `--link-color`, …) at the uright tokens so un-overridden Chirpy
  components inherit the dark palette. Touch this when a stock Chirpy element looks
  wrong.
- **`_chrome.scss`** (largest) styles the shell; `_components.scss` the reusable
  `.ur-*` pieces; `_views.scss` the per-page layouts.

### Chirpy JS compatibility (important gotcha)

Chirpy's minified JS hard-codes DOM IDs (`#sidebar`, `#mode-toggle`, `#toc-wrapper`,
`#search-trigger`, …) that our custom layout doesn't render. `default.html` provides
**hidden no-op stubs** for all of them near the end of `<body>` so Chirpy's JS doesn't
throw `TypeError`. If you strip or rename those stubs, search and comment link/TOC/PWA
break. Our own titlebar search button clicks the hidden `#search-trigger` to reuse
Chirpy's search overlay.

Two custom scripts bridge behaviors Chirpy assumes: `assets/js/uright-drawers.js`
(mobile drawer toggle) and `assets/js/uright-toc.js` (tocbot assumes `window` scroll,
but ours lives on `.ur-main`; only loaded when `panel_includes` contains `toc`).

## Content & config

- Posts live in `_posts/` as `YYYY-MM-DD-title.md`. Front matter uses `categories` and
  `tags` as YAML lists, plus an optional `image: { path, alt }` block and `mermaid: true`.
  Per-post images go in `assets/img/<post-slug>/`.
- `_plugins/posts-lastmod-hook.rb` sets `last_modified_at` from git history (a post
  with >1 commit gets its last commit date), so committing edits updates the displayed
  mod date.
- `_config.yml`: `theme_mode: dark`, Disqus comments (`urightblog`), Google Analytics
  (`G-6MVNSG6PNN`), PWA enabled, permalinks `/posts/:title/`. `site.uright.show_thumbnails`
  / `show_descriptions` toggle those on list views.
- `docs/` and `tools/` are excluded from the build (see `exclude:` in `_config.yml`).
