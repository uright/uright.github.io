---
name: new-post
description: Creates new Jekyll blog posts with AI-powered metadata generation. Use when the user asks to "create a new post", "write a new blog post", "start a new article", or mentions creating Jekyll blog content.
---

# New Blog Post Creator

Creates Jekyll blog posts by collecting a brief description and intelligently generating suggestions for title, description, categories, tags, and featured image.

## Quick Start

1. Get user's post idea (1-2 sentences)
2. Generate intelligent metadata suggestions using existing post patterns
3. Present options via AskUserQuestion for each field
4. Execute the post generator script
5. Report results

## Detailed Resources

**Complete walkthrough**: See [examples/workflow-example.md](examples/workflow-example.md) for a full step-by-step example from start to finish.

**Metadata patterns**: See [references/post-patterns.md](references/post-patterns.md) for title patterns, tag strategies, and generation guidelines based on existing posts.

## Workflow

### Step 1: Collect Post Idea

Ask the user: "Describe your blog post idea in 1-2 sentences (e.g., 'A guide on setting up AWS Bedrock with OpenWebUI')"

### Step 2: Generate Metadata Suggestions

Analyze the description and generate 3-4 options for each field:

- **Titles**: Follow site patterns ("Quick Tip:", "Using X from Y", "How to..."), use title case
- **Descriptions**: SEO-friendly, 1-2 sentences, key terms for searchability
- **Categories**: "Tech, AI" | "Tech, Development" | "Tech, Tutorial" (Title Case)
- **Tags**: 4-6 tags per set, lowercase, comma-separated (technologies + content type)

See [references/post-patterns.md](references/post-patterns.md) for detailed patterns and examples.

### Step 3: Collect Metadata via AskUserQuestion

Present options for each field:

1. **Title** (required) - Header: "Title"
2. **Description** (required) - Header: "Description"
3. **Categories** (required) - Header: "Categories"
4. **Tags** (required) - Header: "Tags", format: comma-separated, lowercase
5. **Mermaid Diagrams** (default: "Yes (Recommended)") - Header: "Mermaid"
6. **Featured Image** (default: "Yes (Recommended)") - Header: "Image"

User can select from options or choose "Other" to enter custom values.

### Step 4: Execute Script

After collecting ALL inputs:

```bash
source .venv/bin/activate && python3 tools/new-post.py \
  --title "{collected_title}" \
  --description "{collected_description}" \
  --categories "{collected_categories}" \
  --tags "{collected_tags}" \
  {--mermaid if user selected yes} \
  {--image-path "filename.png" --image-alt "generated alt text" if image selected}
```

**Image handling**: If user selected "Yes" for featured image, generate descriptive filename from title slug and appropriate alt text from post description.

### Step 5: Report Results

Show user:
- ✅ Created post file path (e.g., `_posts/2026-02-08-post-slug.md`)
- 📁 Created image directory path (if applicable)
- 🖼️ Image filename and location (if applicable)
- 📝 Next steps for adding content

## Important Notes

- **Virtual Environment**: Always activate with `source .venv/bin/activate`
- **Script Location**: `tools/new-post.py`
- **Categories Format**: Title Case (e.g., "Tech, AI")
- **Tags Format**: lowercase (e.g., "aws, bedrock, tutorial")
- **Smart Defaults**: Mermaid and featured image default to "Yes (Recommended)"
