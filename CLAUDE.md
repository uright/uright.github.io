# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Hugo-based static site for the uright tech blog. It uses the `hugo-profile` theme as a git submodule and focuses on technology content related to AWS Bedrock, Azure OpenAI, LLMs, and deep learning.

## Common Commands

```bash
# Install Hugo (required)
brew install hugo

# Initialize git submodules (required for theme)
git submodule update --init

# Run development server
hugo server -D

# Build for production
hugo build
```

## Site Structure

- **`hugo.yaml`**: Main configuration file containing site settings, theme configuration, and content parameters
- **`content/blogs/`**: Blog posts in Markdown format, organized by date
- **`static/`**: Static assets including images, CSS, and favicon files
- **`layouts/`**: Custom Hugo templates and shortcodes
- **`themes/hugo-profile/`**: Git submodule containing the Hugo theme

## Content Management

- Blog posts are located in `content/blogs/` with date-prefixed folders
- Images for posts go in `static/img/` or `static/posts/`
- Site uses dark theme by default (`defaultTheme: "dark"`)
- Navigation is configured in `hugo.yaml` under `Menus.main`

## Theme Configuration

The site uses the hugo-profile theme with extensive customization in `hugo.yaml`:
- Custom CSS is enabled (`customCSS: true`)
- Bootstrap CDN is disabled (`useBootstrapCDN: false`)
- Various sections can be enabled/disabled (experience, education, projects, etc.)
- Social links and contact information are configured in the params section

## Development Notes

- The theme is included as a git submodule, so changes to theme files should be handled carefully
- Custom scripts are embedded in the configuration for background image handling
- Site includes Google Analytics and Disqus integration
- Mermaid diagrams are supported via custom render hook
 No newline at end of file