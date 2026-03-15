# New Post Creation Workflow Example

This document shows a complete example of the new-post skill workflow from start to finish.

## Scenario

User wants to create a blog post about setting up GitHub Actions for automated testing.

## Step-by-Step Workflow

### 1. User Initiates Skill

**User says**: "Create a new post"

**Claude activates**: new-post skill

### 2. Collect Post Idea

**Claude asks**: "Describe your blog post idea in 1-2 sentences"

**User responds**: "A tutorial showing how to set up GitHub Actions for automated testing in a Python project with pytest"

### 3. Generate Intelligent Suggestions

Claude analyzes the input and generates options:

#### Title Options Generated:
1. "Setting Up GitHub Actions for Automated Testing with pytest"
2. "Quick Tutorial: GitHub Actions CI/CD for Python Projects"
3. "How to Automate Python Testing with GitHub Actions"
4. "GitHub Actions for pytest: A Complete Guide"

#### Description Options Generated:
1. "Step-by-step guide for setting up GitHub Actions to automate pytest testing in Python projects"
2. "Learn how to configure GitHub Actions CI/CD pipeline for automated Python testing with pytest"
3. "Complete guide to automating Python tests using GitHub Actions and pytest"

#### Category Options Generated:
1. "Tech, Tutorial"
2. "Tech, Development"
3. "Tech, AI" (less relevant, but offered)

#### Tag Options Generated:
1. "github-actions, ci-cd, python, pytest, automation, testing"
2. "github, actions, python, testing, devops, pytest"
3. "ci-cd, automation, testing, python, github-actions, tutorial"

### 4. Collect User Choices

Claude uses `AskUserQuestion` to present each set of options:

#### Question 1: Title
```
Question: "Choose a title for your post or enter your own:"
Header: "Title"
Options:
  - "Setting Up GitHub Actions for Automated Testing with pytest"
  - "Quick Tutorial: GitHub Actions CI/CD for Python Projects"
  - "How to Automate Python Testing with GitHub Actions"
  - "GitHub Actions for pytest: A Complete Guide"
```

**User selects**: "Quick Tutorial: GitHub Actions CI/CD for Python Projects"

#### Question 2: Description
```
Question: "Choose a description or enter your own:"
Header: "Description"
Options:
  - "Step-by-step guide for setting up GitHub Actions to automate pytest testing in Python projects"
  - "Learn how to configure GitHub Actions CI/CD pipeline for automated Python testing with pytest"
  - "Complete guide to automating Python tests using GitHub Actions and pytest"
```

**User selects**: "Learn how to configure GitHub Actions CI/CD pipeline for automated Python testing with pytest"

#### Question 3: Categories
```
Question: "Select the categories for this post:"
Header: "Categories"
Options:
  - "Tech, Tutorial"
  - "Tech, Development"
  - "Tech, AI"
```

**User selects**: "Tech, Tutorial"

#### Question 4: Tags
```
Question: "Select a tag set or enter your own (comma-separated):"
Header: "Tags"
Options:
  - "github-actions, ci-cd, python, pytest, automation, testing"
  - "github, actions, python, testing, devops, pytest"
  - "ci-cd, automation, testing, python, github-actions, tutorial"
```

**User selects**: "github-actions, ci-cd, python, pytest, automation, testing"

#### Question 5: Mermaid Diagrams
```
Question: "Will this post include Mermaid diagrams?"
Header: "Mermaid"
Options:
  - "Yes (Recommended)"
  - "No"
```

**User selects**: "Yes (Recommended)"

#### Question 6: Featured Image
```
Question: "Do you want to add a featured image?"
Header: "Image"
Options:
  - "Yes (Recommended)"
  - "No"
```

**User selects**: "Yes (Recommended)"

### 5. Generate Image Metadata

Claude generates:
- **Filename**: `github-actions-pytest-ci.png`
- **Alt text**: "GitHub Actions CI/CD pipeline for Python pytest automation"
- **Full path**: `/assets/img/2026-02-08-quick-tutorial-github-actions-ci-cd-for-python-projects/github-actions-pytest-ci.png`

### 6. Execute Script

Claude runs:

```bash
source .venv/bin/activate && python3 tools/new-post.py \
  --title "Quick Tutorial: GitHub Actions CI/CD for Python Projects" \
  --description "Learn how to configure GitHub Actions CI/CD pipeline for automated Python testing with pytest" \
  --categories "Tech, Tutorial" \
  --tags "github-actions, ci-cd, python, pytest, automation, testing" \
  --mermaid \
  --image-path "github-actions-pytest-ci.png" \
  --image-alt "GitHub Actions CI/CD pipeline for Python pytest automation"
```

### 7. Draft Initial Post Content

After the script creates the file, Claude reads it to confirm the front matter, then writes the full draft body. For example:

```markdown
## The Problem

Manually running `pytest` before every commit is easy to forget — and CI failures that could have been caught earlier slow everyone down. GitHub Actions solves this by running your test suite automatically on every push and pull request, with zero changes to your local workflow.

This guide walks you through setting up a GitHub Actions workflow for a Python project that uses `pytest`.

## Prerequisites

- A GitHub repository with a Python project
- `pytest` installed and tests passing locally (`pip install pytest`)
- A `requirements.txt` or `pyproject.toml` listing your dependencies

## Step 1: Create the Workflow File

GitHub Actions workflows live in `.github/workflows/`. Create the directory if it doesn't exist:

```bash
mkdir -p .github/workflows
```

Create `.github/workflows/test.yml`:

```yaml
name: Run Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest
```

## Step 2: Commit and Push

```bash
git add .github/workflows/test.yml
git commit -m "Add GitHub Actions CI workflow for pytest"
git push
```

Navigate to **Actions** tab in your GitHub repo — you'll see the workflow running immediately.

## Step 3: Add a Status Badge (Optional)

Add this to your `README.md` to display the CI status:

```markdown
![Tests](https://github.com/{your-org}/{your-repo}/actions/workflows/test.yml/badge.svg)
```

## Tips

**Run only on changed files** using `paths` filters to avoid running tests on documentation-only changes:

```yaml
on:
  push:
    paths:
      - "**.py"
      - "requirements.txt"
```

**Cache pip dependencies** to speed up runs:

```yaml
- name: Cache pip
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

- name: Install dependencies
  run: pip install -r requirements.txt
```

**Matrix testing** across multiple Python versions:

```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
```
```

Claude then uses the Edit tool to write this draft into the created post file, replacing the empty body section left by the generator script.

### 8. Report Results

Claude responds:

```
✅ Created new post: _posts/2026-02-08-quick-tutorial-github-actions-ci-cd-for-python-projects.md

📁 Created image directory: assets/img/2026-02-08-quick-tutorial-github-actions-ci-cd-for-python-projects/

🖼️ Featured image placeholder: assets/img/2026-02-08-quick-tutorial-github-actions-ci-cd-for-python-projects/github-actions-pytest-ci.png

📝 Draft written — sections: Prerequisites, Step 1 (workflow file), Step 2 (push), Step 3 (badge), Tips

Next steps:
1. Review and refine the draft in the markdown file
2. Add your featured image to the image directory
3. Preview with: bundle exec jekyll serve
4. Commit and push when ready
```

## Key Features Demonstrated

### Intelligent Analysis
- Extracted key technologies: GitHub Actions, Python, pytest, CI/CD
- Identified content type: Tutorial
- Matched to existing patterns

### Multiple Options
- Generated 4 title variations
- Created 3 description options
- Suggested relevant category combinations
- Provided 3 tag set alternatives

### Smart Defaults
- Mermaid diagrams: "Yes (Recommended)" as default
- Featured image: "Yes (Recommended)" as default

### Automated Metadata Generation
- Image filename automatically generated from title
- Alt text created from post content
- Full image path constructed properly

### User Flexibility
- "Other" option available for all fields
- Can mix and match suggestions
- Can provide completely custom values

## Benefits Over Manual Creation

1. **Speed**: 5 questions + auto-drafted content vs starting from blank
2. **Consistency**: Follows established patterns automatically
3. **Quality**: SEO-optimized descriptions, proper formatting, and complete initial draft
4. **Intelligence**: Learns from existing posts for both metadata and writing style
5. **Convenience**: Pre-filled defaults for common choices
6. **Draft velocity**: Produces a publishable starting point — not just scaffolding
