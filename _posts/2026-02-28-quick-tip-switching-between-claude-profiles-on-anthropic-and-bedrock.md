---
title: "Quick Tip: Switching Between Claude Profiles on Anthropic and Bedrock"
description: "Tips for managing multiple Claude profiles when switching between Anthropic and AWS Bedrock."
date: 2026-02-28 16:41:56 -0500
categories: [Tech, Ai]
tags: [claude, anthropic, bedrock, aws, tips, profiles]
image:
  path: /assets/img/2026-02-28-quick-tip-switching-between-claude-profiles-on-anthropic-and-bedrock/claude-profiles-anthropic-bedrock.png
  alt: "Switching between Claude profiles on Anthropic API and AWS Bedrock"
mermaid: true
---

## The Problem

If you use Claude Code across multiple environments — an Anthropic subscription, a work AWS Bedrock account, a personal one — switching between them means:

- Editing `~/.claude/settings.json` each time, or
- Manually `export`-ing environment variables before launching, or
- Juggling multiple terminal windows with different environments

None of these are great. Shell aliases solve this in 5 minutes.

## What is a Shell Alias?

A shell alias is a custom shortcut command that expands into a longer command automatically. Instead of typing:

```bash
CLAUDE_CODE_USE_BEDROCK=1 AWS_PROFILE=my-work-account AWS_REGION=us-east-1 claude
```

You define a nickname once, and just type `claude-work` from then on. That's it.

## Setup (5 minutes)

### Step 1: Open your shell config file

```bash
# If you're on a modern Mac (zsh):
nano ~/.zshrc

# If you're on Linux or an older Mac (bash):
nano ~/.bashrc
```

### Step 2: Add your aliases

Paste the following at the bottom of the file, replacing profile names and regions with your own:

```bash
# Claude Code profile aliases
alias claude-anthropic='unset CLAUDE_CODE_USE_BEDROCK && claude'
alias claude-bedrock1='CLAUDE_CODE_USE_BEDROCK=1 AWS_PROFILE=account1 AWS_REGION=us-east-1 claude'
alias claude-bedrock2='CLAUDE_CODE_USE_BEDROCK=1 AWS_PROFILE=account2 AWS_REGION=eu-west-1 claude'
alias claude-bedrock3='CLAUDE_CODE_USE_BEDROCK=1 AWS_PROFILE=account3 AWS_REGION=ap-southeast-1 claude'
```

> **Note:** The `AWS_PROFILE` values here should match the profile names in your `~/.aws/credentials` or `~/.aws/config` file.

### Step 3: Reload your shell

```bash
source ~/.zshrc   # or source ~/.bashrc
```

That's it. You're done.

## Using Your Aliases

From now on, launching Claude Code with a specific profile is just one short command:

```bash
claude-anthropic   # Anthropic subscription
claude-bedrock1    # Bedrock Account #1
claude-bedrock2    # Bedrock Account #2
claude-bedrock3    # Bedrock Account #3
```

The environment variables are only set for that Claude session — they won't bleed into other terminal windows or background processes.

## Tips

**Use descriptive alias names.** Names like `claude-personal`, `claude-work`, or `claude-prod` are easier to remember than `claude-bedrock1`.

```bash
alias claude-personal='CLAUDE_CODE_USE_BEDROCK=1 AWS_PROFILE=personal AWS_REGION=us-west-2 claude'
alias claude-work='CLAUDE_CODE_USE_BEDROCK=1 AWS_PROFILE=corp-sso AWS_REGION=eu-west-1 claude'
```

**Combine with SSO login.** If your Bedrock accounts use AWS SSO, you can chain the login command so it refreshes credentials automatically before launching:

```bash
alias claude-work='aws sso login --profile corp-sso && CLAUDE_CODE_USE_BEDROCK=1 AWS_PROFILE=corp-sso AWS_REGION=eu-west-1 claude'
```

**Check which aliases you have at any time:**

```bash
alias | grep claude
```

## Why Not Just Use `~/.claude/settings.json`?

The `settings.json` file is great for setting a *default* configuration, but it only supports one active profile at a time. There's currently no native multi-profile switcher built into Claude Code. Aliases fill that gap — no extra tooling required, just your shell.