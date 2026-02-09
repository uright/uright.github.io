# Blog Post Patterns Reference

This document provides reference patterns from existing blog posts to help generate consistent metadata.

## Common Title Patterns

1. **Tutorial Style**: "How to [Action] [Technology]"
   - Example: "How to Deploy Docker Applications on AWS ECS"

2. **Quick Tip Style**: "Quick Tip: [Action] [Technology]"
   - Example: "Quick Tip: Installing AWS CLI v2 with uv Tool"

3. **Integration Style**: "Using [Technology A] from [Technology B]"
   - Example: "Using AWS Bedrock Models from OpenWebUI"

4. **Problem/Solution Style**: "[Problem] Solved in [Technology]"
   - Example: "Shift+Enter Shortcut Key Solved in Claude Code + Antigravity"

5. **Guide Style**: "[Action]: A Complete Guide"
   - Example: "Deploying Docker Containers: A Complete Guide"

## Common Category Combinations

Based on existing posts, these are the standard categories:

- **"Tech, AI"**: For AI/ML-related content, cloud AI services
  - AWS Bedrock, OpenAI, LLMs, model deployment

- **"Tech, Development"**: For development tools, programming, tooling
  - Claude Code, keyboard shortcuts, developer tools, IDEs

- **"Tech, Tutorial"**: For step-by-step guides and how-to content
  - Installation guides, configuration tutorials, deployment guides

## Tag Patterns by Topic

### Cloud & Infrastructure
- **AWS**: aws, bedrock, ecs, cloud, deployment
- **Docker**: docker, containers, deployment, devops
- **Azure**: azure, openai, cloud

### Development Tools
- **CLI Tools**: cli, tools, terminal, bash
- **IDE/Editors**: claude-code, vscode, antigravity, keyboard-shortcuts
- **Package Managers**: uv, pip, npm, homebrew

### AI & ML
- **LLM Platforms**: llm, openai, bedrock, ai
- **Specific Models**: claude, gpt, llama
- **ML Tools**: openwebui, litellm

### Content Types
- **Tutorial**: tutorial, guide, how-to, step-by-step
- **Tips**: tips, quick-tip, tricks
- **Configuration**: config, setup, installation

## Description Patterns

### Tutorial Descriptions
- "Step-by-step guide for [action] [technology]"
- "Learn how to [action] with [technology]"
- "Complete guide to [action] on [platform]"

### Quick Tip Descriptions
- "A quick tip on [action] to [benefit]"
- "Quick guide to [action] making [benefit]"

### Integration Descriptions
- "Guide of configuring [tool A] to connect to [tool B]"
- "How to integrate [tool A] with [tool B] for [benefit]"

### Problem/Solution Descriptions
- "Resolving the [problem] when using [technology]"
- "Fix for [issue] in [technology]"

## Metadata Examples from Real Posts

### Example 1: AI Integration Tutorial
```yaml
title: "Using AWS Bedrock Models from OpenWebUI"
description: "Guide of configuring OpenWebUI to connect to Bedrock models for inference"
categories: [Tech, AI]
tags: [aws, bedrock, openwebui, llm]
mermaid: true
image: yes
```

### Example 2: Development Tool Tip
```yaml
title: "Shift+Enter Shortcut Key Solved in Claude Code + Antigravity"
description: "Resolving the Shift+Enter keyboard shortcut issue when using Claude Code with Antigravity"
categories: [Tech, Development]
tags: [claude-code, antigravity, keyboard-shortcuts, tips]
image: yes
```

### Example 3: Installation Tutorial
```yaml
title: "Quick Tip: Installing AWS CLI v2 with uv Tool"
description: "A quick tip on using uv tool to install and manage AWS CLI v2, making Python-based CLI tool installation easier."
categories: [Tech, Tutorial]
tags: [aws, cli, uv, python, tools, quick-tip]
image: yes
```

### Example 4: Docker Tutorial
```yaml
title: "Docker Desktop Volume Backup and Restore"
description: "Step-by-step guide for backing up and restoring Docker Desktop volumes"
categories: [Tech, Tutorial]
tags: [docker, backup, volumes, containers, devops]
image: yes
```

## Generation Guidelines

### When Analyzing User Input

1. **Identify the main technology/tool** mentioned
2. **Determine the content type** (tutorial, tip, guide, integration)
3. **Extract key concepts and technologies**
4. **Match to existing patterns** above
5. **Generate 3-4 variations** of each metadata field

### Title Generation Strategy

1. Start with the most common pattern for the content type
2. Create variations with different phrasings
3. Keep titles under 70 characters
4. Use title case
5. Be specific and descriptive

### Tag Generation Strategy

1. Include the primary technology (lowercase)
2. Add related technologies and tools
3. Include content type tags (tutorial, tips, guide)
4. Add 1-2 general domain tags (cloud, devops, ai)
5. Keep total tags between 4-6

### Category Selection Logic

- **AI/ML content** → "Tech, AI"
- **Development tools/IDE** → "Tech, Development"
- **Step-by-step guides** → "Tech, Tutorial"
- **Multi-topic** → Choose the most dominant focus

## Image Filename Format

Generated image filenames should follow this pattern:
```
YYYY-MM-DD-{slug}/{descriptive-name}.png
```

Examples:
- `2026-02-08-aws-bedrock-openwebui/integration-diagram.png`
- `2026-02-08-docker-volume-backup/backup-process.png`
- `2026-02-08-quick-uv-install/uv-aws-cli-install.png`
