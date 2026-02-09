# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Jekyll-based static site for the uright tech blog. It uses the `jekyll-theme-chirpy` theme and focuses on technology content related to AWS Bedrock, Azure OpenAI, LLMs, and deep learning.

## Development Setup

You can run this Jekyll site using either local Ruby installation or Docker. Choose the method that works best for your environment.

### Option 1: Docker (Recommended - No local Ruby needed)

**Prerequisites:** Docker Desktop installed

```bash
# Build and start development server
docker-compose up --build

# Access site at http://localhost:4000
# LiveReload enabled on port 35729

# Stop server
docker-compose down

# Build for production
docker-compose run --rm jekyll bundle exec jekyll build
```

See [README.Docker.md](README.Docker.md) for comprehensive Docker documentation.

### Option 2: Local Ruby Installation

**Prerequisites:** Ruby and Bundler installed locally

```bash
# Install Ruby (if not already installed)
# macOS: brew install ruby
# Ubuntu: sudo apt-get install ruby-full

# Install bundler
gem install bundler

# Install dependencies
bundle install

# Run development server
bundle exec jekyll serve

# Build for production
bundle exec jekyll build
```

## Site Structure

- **`_config.yml`**: Main configuration file containing site settings, theme configuration, and content parameters
- **`_posts/`**: Blog posts in Markdown format with date-prefixed filenames
- **`assets/`**: Static assets including images, CSS, and favicon files
- **`_includes/`**: Reusable Jekyll includes and custom components
- **`_data/`**: Site data files (contact.yml, share.yml)
- **`_tabs/`**: Static pages (about, archives, categories, tags)
- **`_plugins/`**: Custom Jekyll plugins

## Content Management

- Blog posts are located in `_posts/` with date-prefixed filenames (YYYY-MM-DD-title.md)
- Images for posts go in `assets/img/`
- Site uses dark theme by default (`theme_mode: dark`)
- Navigation tabs are configured in `_tabs/` directory
- Categories and tags are automatically generated from post front matter

## Theme Configuration

The site uses the jekyll-theme-chirpy theme with customization in `_config.yml`:
- Dark theme is enabled by default
- Google Analytics integration (G-6MVNSG6PNN)
- Disqus comments enabled (shortname: urightblog)
- Social links and contact information are configured in the social section
- PWA (Progressive Web App) features are enabled

## Development Notes

- The theme is installed as a Ruby gem via Gemfile
- Site includes Google Analytics and Disqus integration
- Built-in support for syntax highlighting, TOC, and search functionality
- Supports categories, tags, and archives pages automatically