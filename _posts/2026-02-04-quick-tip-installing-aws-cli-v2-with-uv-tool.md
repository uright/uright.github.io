---
title: "Quick Tip: Installing AWS CLI v2 with uv Tool"
description: "A quick tip on using uv tool to install and manage AWS CLI v2, making Python-based CLI tool installation easier."
date: 2026-02-04 21:55:21 -0500
categories: [Tech, Tutorial]
tags: [aws, cli, uv, python, tools, quick-tip]
image:
  path: /assets/img/2026-02-04-quick-tip-installing-aws-cli-v2-with-uv-tool/uv-aws-cli-install.png
  alt: "Installing AWS CLI v2 using uv tool"
---

## The Problem with Traditional Installation Methods

If you're managing your Python environments with [uv](https://github.com/astral-sh/uv), you might have encountered these issues:

**Using Homebrew:**
```bash
brew install awscli
```
While this works, Homebrew installs AWS CLI with its own Python version, managed by brew rather than uv. This creates a separate Python ecosystem outside of uv's control.

**Using uv tool install:**
```bash
uv tool install awscli
```
This command only installs AWS CLI **v1**, not the newer v2 that most users want.

## The Solution: Install AWS CLI v2 with uv

Here's how to install AWS CLI v2 while keeping everything managed by uv:

```bash
uv tool install git+https://github.com/aws/aws-cli.git@v2
```

This command:
- Installs AWS CLI v2 directly from the official GitHub repository
- Uses uv's Python environment management
- Keeps all your Python tools in one unified ecosystem

## Verify Installation

After installation, verify that AWS CLI v2 is installed:

```bash
aws --version
```

You should see output confirming v2 is being used:
```
aws-cli/2.x.x Python/3.x.x ...
```

Notice the version starts with **2.x.x**, confirming you have AWS CLI v2 installed via uv!

