---
title: "Shift+Enter Shortcut Key Solved in Claude Code + Antigravity"
description: "Resolving the Shift+Enter keyboard shortcut issue when using Claude Code with Antigravity"
date: 2026-02-05 22:53:37 -0500
categories: [Tech, Development]
tags: [claude-code, antigravity, keyboard-shortcuts, tips]
image:
  path: /assets/img/2026-02-05-shiftenter-shortcut-key-solved-in-claude-code-antigravity/shift-enter-fix.png
  alt: "Shift+Enter shortcut fix in Claude Code and Antigravity"
---

If you use Claude Code inside [Antigravity](http://antigravity.google/), you may have noticed that `Shift+Enter` doesn't work in the terminal. This is because Claude Code's `/terminal-setup` command only updates VSCode's `keybindings.json`, which Antigravity does not read. Here's how to fix it.

## The Problem

Running `/terminal-setup` in Claude Code configures the `Shift+Enter` keybinding for VSCode. However, Antigravity maintains its own separate keyboard shortcuts configuration, so the binding never takes effect.

## The Fix

### 1. Run `/terminal-setup` in Claude Code

This generates the required keybinding in VSCode's `keybindings.json`. On macOS, the entry looks like this:

```json
[
    {
        "key": "shift+enter",
        "command": "workbench.action.terminal.sendSequence",
        "args": {
            "text": "\u001b\r"
        },
        "when": "terminalFocus"
    }
]
```

### 2. Add the keybinding to Antigravity

1. Open the Command Palette with `Cmd + Shift + P`
2. Search for **Keyboard Shortcuts**
3. Click the file icon in the top-right corner to open the JSON config
4. Paste the same keybinding configuration into the file and save

`Shift+Enter` should now work as expected in Claude Code within Antigravity.