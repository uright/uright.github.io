# Jekyll Blog Post Generator

A complete system for creating new blog posts for the uright.github.io Jekyll blog with proper front matter, automatic slug generation, and directory creation.

## Overview

This system provides two ways to create new posts:

1. **CLI Script** (`tools/new-post.py`) - Direct command-line usage
2. **Claude Code Slash Command** (`/new-post`) - Interactive prompts within Claude Code

Both methods ensure consistent post formatting, proper YAML front matter, and automatic image directory creation.

## Quick Start

### Using CLI Script

```bash
# Install dependencies (first time only)
pip install -r tools/requirements.txt

# Create a basic post
python3 tools/new-post.py \
  --title "My Awesome Post" \
  --description "Learn something cool" \
  --categories "Tech, AI" \
  --tags "python, tutorial, beginner"
```

### Using Claude Code Slash Command

Simply type `/new-post` in Claude Code and follow the interactive prompts.

## CLI Usage

### Required Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `--title` | `-t` | Post title |
| `--description` | `-d` | Post description (for SEO and previews) |
| `--categories` | `-c` | Comma-separated categories (e.g., "Tech, AI") |
| `--tags` | | Comma-separated tags (e.g., "python, tutorial") |

### Optional Arguments

| Argument | Description |
|----------|-------------|
| `--image-path` | Image filename (e.g., "hero-image.png") |
| `--image-alt` | Image alt text (required if --image-path is provided) |
| `--mermaid` | Enable Mermaid diagram support |
| `--date` | Custom date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) |
| `--dry-run` | Preview what would be created without actually creating files |

### Examples

#### Basic Post

```bash
python3 tools/new-post.py \
  --title "Getting Started with Python" \
  --description "A beginner's guide to Python programming" \
  --categories "Tech, Programming" \
  --tags "python, beginner, tutorial"
```

#### Post with Featured Image

```bash
python3 tools/new-post.py \
  --title "Understanding Neural Networks" \
  --description "Deep dive into neural network architecture" \
  --categories "Tech, AI" \
  --tags "deep-learning, neural-networks, ml" \
  --image-path "neural-network-diagram.png" \
  --image-alt "Neural network architecture diagram"
```

#### Post with Mermaid Diagrams

```bash
python3 tools/new-post.py \
  --title "System Architecture Overview" \
  --description "Visual guide to our system architecture" \
  --categories "Tech, Architecture" \
  --tags "architecture, diagrams, systems" \
  --mermaid
```

#### Preview with Dry Run

```bash
python3 tools/new-post.py \
  --title "Test Post" \
  --description "Testing the generator" \
  --categories "Tech" \
  --tags "test" \
  --dry-run
```

#### Backdated Post

```bash
python3 tools/new-post.py \
  --title "My Earlier Post" \
  --description "Posted with a custom date" \
  --categories "Tech" \
  --tags "archive" \
  --date "2024-06-15"
```

## Slash Command Usage

The `/new-post` command in Claude Code provides an interactive experience:

1. Type `/new-post` in Claude Code
2. Answer each prompt:
   - Post title
   - Description
   - Categories (comma-separated)
   - Tags (comma-separated)
   - Mermaid diagram support (yes/no)
   - Featured image (optional)
3. The post and image directory are created automatically

## Generated File Structure

When you create a post titled "My Awesome Post" on January 7, 2025:

```
uright.github.io/
├── _posts/
│   └── 2025-01-07-my-awesome-post.md    # Your new post
└── assets/
    └── img/
        └── 2025-01-07-my-awesome-post/  # Image directory
```

## Front Matter Format

The generator creates posts with this front matter structure:

```yaml
---
title: "My Awesome Post"
description: "Post description for SEO"
date: 2025-01-07 14:30:00 -0400
categories: [Tech, AI]
tags: [python, tutorial, beginner]
image:                          # Optional
  path: /assets/img/2025-01-07-my-awesome-post/hero-image.png
  alt: "Image description"
mermaid: true                   # Optional
---
```

## Slug Generation

Titles are automatically converted to URL-safe slugs:

| Title | Slug |
|-------|------|
| "How I Built This!" | `how-i-built-this` |
| "Python 3.11: New Features" | `python-311-new-features` |
| "AI & ML in 2024" | `ai-ml-in-2024` |
| "  Spaces   Everywhere  " | `spaces-everywhere` |

## Categories and Tags

### Categories
- Use Title Case: "Tech", "AI", "Development"
- Recommended: 1-3 categories
- Comma-separated in CLI: `"Tech, AI"`

### Tags
- Use lowercase: "python", "tutorial", "git"
- Recommended: 3-10 tags
- Hyphens allowed: "azure-openai", "claude-code"
- Comma-separated in CLI: `"python, tutorial, beginner"`

## Troubleshooting

### Common Errors

**"Error: Title cannot be empty"**
- Ensure you provide a non-empty title

**"Error: At least one category required"**
- Provide at least one category with `--categories`

**"Error: Post already exists at {path}"**
- A post with the same date and slug already exists
- Use a different title or date

**"Error: Template not found"**
- Ensure `tools/templates/post-template.j2` exists
- Run from the project root directory

**"Error: Cannot write to {path}. Check permissions"**
- Check file system permissions
- Ensure `_posts/` and `assets/img/` directories exist

### Tips

1. **Run from project root**: The script expects to be run from the project root or `tools/` directory
2. **Use dry-run first**: Preview with `--dry-run` to verify before creating
3. **Check slug conflicts**: If a post with the same slug exists, change the title slightly
4. **Timezone**: All dates use America/Toronto timezone (-0400)

## Development

### File Locations

```
tools/
├── new-post.py              # Main Python script
├── requirements.txt         # Python dependencies
└── templates/
    └── post-template.j2     # Jinja2 template

.claude/
└── commands/
    └── new-post.md          # Slash command definition
```

### Dependencies

- Python 3.8+
- jinja2 >= 3.1.2
- python-dateutil >= 2.8.2
- pytz >= 2023.3

### Extending the Generator

To modify the post template, edit `tools/templates/post-template.j2`.

To add new CLI arguments, modify the `argparse` section in `tools/new-post.py`.

To update the slash command behavior, edit `.claude/commands/new-post.md`.
