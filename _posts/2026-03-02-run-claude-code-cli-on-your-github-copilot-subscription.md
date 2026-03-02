---
title: "Run Claude Code CLI on Your GitHub Copilot Subscription"
description: "A quick tip on using Claude Code CLI with your existing GitHub Copilot subscription to access Claude models without a separate Anthropic subscription."
date: 2026-03-02 14:37:09 -0500
categories: [Tech, Ai]
tags: [claude-code, github-copilot, cli, tips, ai, developer-tools]
image:
  path: /assets/img/2026-03-02-run-claude-code-cli-on-your-github-copilot-subscription/claude-code-github-copilot.png
  alt: "Claude Code CLI configured to use GitHub Copilot subscription for AI-powered development"
mermaid: true
---

## The Situation

If you're on a GitHub Copilot subscription — individual, Pro, or through your organization — you already have access to Claude models. GitHub Copilot's Agent HQ brings Claude directly into your IDE (VS Code, JetBrains, etc.) as an in-editor AI agent.

That's great for quick questions and inline edits. But it's not Claude Code CLI.

Claude Code CLI is a different beast. It's a terminal-first AI coding agent with:
- Your own MCP servers, skills, and plugins configured in `~/.claude/`
- Session history and context continuity across conversations
- Access to your project's full file tree and shell environment
- Custom hooks, memory, and project-specific instructions

The question is: can you point Claude Code CLI at your existing Copilot subscription instead of paying for a separate Anthropic API subscription?

Yes. Here's how.

## The Proxy: `copilot-api`

The key tool is [`copilot-api`](https://github.com/ericc-ch/copilot-api) — an open-source reverse-engineered proxy that exposes GitHub Copilot as both an OpenAI-compatible and an Anthropic-compatible API endpoint.

Once running, it listens on `localhost:4141` and forwards requests to GitHub Copilot on your behalf, translating the API format along the way. Claude Code (which talks to Anthropic's API) can then be pointed at this local proxy instead.

> ⚠️ **Note:** `copilot-api` is not officially supported by GitHub and is a community project. Use it responsibly and in accordance with GitHub's [acceptable use policies](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies). Avoid excessive automated use.

## Step 1: Install `copilot-api`

You'll need [Bun](https://bun.sh/) (≥1.2.x) installed first:

```bash
curl -fsSL https://bun.sh/install | bash
```

Then install `copilot-api` globally:

```bash
npm install -g copilot-api
```

Or run it directly without installing:

```bash
npx copilot-api@latest start
```

## Step 2: Authenticate with GitHub

On first run, `copilot-api` will prompt you to authenticate with your GitHub account:

```bash
copilot-api start
```

Follow the device code flow — it opens a browser prompt to authorize the app against your GitHub account. Your Copilot subscription is then used to generate tokens for the proxy.

## Step 3: Set Environment Variables

With the proxy running on port `4141`, tell Claude Code to use it by setting these environment variables before launching:

```bash
export ANTHROPIC_BASE_URL="http://localhost:4141"
export ANTHROPIC_MODEL="claude-sonnet-4.6"
export ANTHROPIC_API_KEY="placeholder"
export ANTHROPIC_DEFAULT_OPUS_MODEL="claude-opus-4.6"
export ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-4.6"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="claude-haiku-4.5"
```

Then launch Claude Code normally:

```bash
claude
```

Claude Code will route all API calls through the local proxy, which forwards them to GitHub Copilot — using your existing subscription.

## Step 4: Make It Convenient with an Alias

Typing all of that manually each time gets old fast. The alias below starts the proxy in the background if it isn't already running, then launches Claude Code with all the necessary environment variables set:

Add this to your `~/.zshrc` (or `~/.bashrc`):

```bash
alias claude-ghc='\
  if ! lsof -ti:4141 > /dev/null 2>&1; then nohup copilot-api start > /dev/null 2>&1 & sleep 2; fi; \
  ANTHROPIC_BASE_URL="http://localhost:4141" \
  ANTHROPIC_MODEL="claude-sonnet-4.6" \
  ANTHROPIC_API_KEY="placeholder" \
  ANTHROPIC_DEFAULT_OPUS_MODEL="claude-opus-4.6" \
  ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-4.6" \
  ANTHROPIC_DEFAULT_HAIKU_MODEL="claude-haiku-4.5" \
  claude'
```

Reload your shell config:

```bash
source ~/.zshrc
```

From now on, just type:

```bash
claude-ghc
```

The alias:
1. Checks if port `4141` is already in use (proxy already running)
2. If not, starts `copilot-api` in the background and waits 2 seconds for it to initialize
3. Launches Claude Code with all the required environment variables inline

Your `~/.claude/` setup — MCP servers, skills, hooks, memory, project instructions — all works exactly as normal. The only difference is where the API calls go.

## Why Not Just Use Agent HQ in the IDE?

Agent HQ (Copilot's Claude integration inside VS Code or JetBrains) is useful for in-editor tasks. But it's isolated to the IDE — it doesn't have access to your MCP servers, custom skills, `~/.claude/` configuration, or session history.

Claude Code CLI is designed for deeper, longer-horizon work: multi-file refactors, shell-integrated workflows, background agents, and project-specific context that builds up over time. If you've invested in setting up your `~/.claude/` environment, using Claude Code CLI means that investment carries over to every project you work on.

With this setup, you get both: the in-IDE convenience of Agent HQ and the full power of Claude Code CLI — all on the same Copilot subscription.

## Tips

**Check which process holds port 4141:**

```bash
lsof -ti:4141
```

**Stop the background proxy manually:**

```bash
kill $(lsof -ti:4141)
```

**Verify the proxy is responding:**

```bash
curl http://localhost:4141/v1/models
```

**Rate limiting:** If you hit usage limits, `copilot-api` supports a `--rate-limit` flag to throttle requests:

```bash
copilot-api start --rate-limit 10
```