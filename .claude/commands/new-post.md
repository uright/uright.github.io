---
description: Create a new Jekyll blog post with interactive prompts
---

Create a new Jekyll blog post by collecting metadata from the user interactively.

**IMPORTANT**: You MUST use the AskUserQuestion tool to collect EACH piece of information below. Do NOT assume any values - ask the user for everything.

## Step 1: Collect Post Information

Use AskUserQuestion to ask for each of these in order:

1. First, ask for the **post title**:
   - Question: "What's the title of your new blog post?"
   - Header: "Title"
   - This is required - do not proceed without it

2. Then ask for the **description**:
   - Question: "Provide a brief description for SEO and previews:"
   - Header: "Description"
   - This is required

3. Then ask for **categories**:
   - Question: "Which categories should this post be in?"
   - Header: "Categories"
   - Options: "Tech, AI", "Tech, Development", "Tech, Tutorial", plus allow "Other" for custom input
   - Use comma-separated format

4. Then ask for **tags**:
   - Question: "Enter tags for this post (comma-separated, e.g., 'python, tutorial, beginner'):"
   - Header: "Tags"

5. Then ask about **Mermaid diagrams**:
   - Question: "Will this post include Mermaid diagrams?"
   - Header: "Mermaid"
   - Options: "Yes", "No"

6. Finally, ask about **featured image**:
   - Question: "Do you want to add a featured image?"
   - Header: "Image"
   - Options: "Yes", "No"
   - If Yes: Follow up asking for filename and alt text

## Step 2: Execute the Script

After collecting ALL inputs, run the post generator script:

```bash
source .venv/bin/activate && python3 tools/new-post.py \
  --title "{collected_title}" \
  --description "{collected_description}" \
  --categories "{collected_categories}" \
  --tags "{collected_tags}" \
  {--mermaid if user said yes} \
  {--image-path "filename" --image-alt "alt text" if user provided image}
```

## Step 3: Report Results

Show the user:
- The created post file path
- The created image directory path
- Next steps for adding content

## Important Notes

- Always activate the virtual environment before running the script: `source .venv/bin/activate`
- The script is located at `tools/new-post.py`
- Categories should be Title Case (e.g., "Tech, AI")
- Tags should be lowercase (e.g., "python, tutorial")
