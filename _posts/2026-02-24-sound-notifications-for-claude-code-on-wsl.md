---
title: "Sound Notifications for Claude Code on WSL/Windows 11"
description: "Quick tip: Add audio alerts to Claude Code using Windows built-in sounds when it stops or needs attention"
date: 2026-02-24 00:42:00 -0500
categories: [Tech, Quick Tips]
tags: [claude-code, wsl, windows11, productivity, cli]
image:
  path: /assets/img/2026-02-24-sound-notifications-for-claude-code-on-wsl/hero-image.png
  alt: "Claude Code with sound notifications on WSL and Windows 11"
---

## The Problem

When you're using Claude Code in WSL (Windows Subsystem for Linux) and multitasking—maybe you've switched to another window or stepped away—you might miss when Claude finishes a task or needs your attention. Without visual focus on the terminal, you're left checking back repeatedly or risking delays.

## The Solution

Claude Code supports **hooks** in its settings that can trigger commands on specific events. By combining WSL's ability to call Windows PowerShell with Windows 11's built-in sound files, you can get audio notifications that cut through the noise.

Two key events we want to catch:
- **Stop**: When Claude Code finishes running or stops
- **Notification**: When Claude Code needs user input or attention

## The Configuration

Edit your `~/.claude/settings.json` file and add a `hooks` section:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -NonInteractive -c \"(New-Object Media.SoundPlayer 'C:\\\\Windows\\\\Media\\\\Ring02.wav').PlaySync()\""
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -NonInteractive -c \"(New-Object Media.SoundPlayer 'C:\\\\Windows\\\\Media\\\\Ring06.wav').PlaySync()\""
          }
        ]
      }
    ]
  }
}
```

## How It Works

1. **WSL Path Translation**: `/mnt/c/Windows/...` accesses the Windows C: drive from WSL
2. **PowerShell from WSL**: We invoke PowerShell directly to play system sounds
3. **Media.SoundPlayer**: A .NET class that can play `.wav` files synchronously
4. **Unique Sounds**: 
   - `Ring02.wav` for Stop events (task complete)
   - `Ring06.wav` for Notification events (needs attention)
5. **Empty Matcher**: `"matcher": ""` means the hook triggers for all events of that type

## Why These Sounds?

Windows 11 ships with dozens of built-in sound files in `C:\Windows\Media\`. I chose `Ring02.wav` and `Ring06.wav` because they're:
- **Distinct**: You can instantly tell which event occurred
- **Pleasant**: Not jarring or annoying during long coding sessions
- **Short**: Quick audio cue without disrupting focus

## Testing

After saving the configuration, try running a Claude Code command and switch windows. You should hear:
- `Ring02.wav` when Claude stops/completes
- `Ring06.wav` when Claude needs your input

## Bonus Tips

**Customize Your Sounds**: Browse `C:\Windows\Media\` and pick sounds that work for you. Just update the file paths in the config.

**Volume Control**: Windows notification sounds respect your system volume. If they're too loud/quiet, adjust your system volume or choose different sound files.

**Other Hooks**: Claude Code supports other hook events. Check the documentation to extend this pattern for error notifications, warnings, or other events.

## Why This Matters

This small tweak significantly improves the developer experience:
- **No More Checking Back**: You'll know immediately when Claude needs you
- **Better Multitasking**: Work on other tasks without losing track of Claude's progress
- **Reduced Context Switching**: Audio cues are less disruptive than visual polling

## Cross-Platform Note

This specific approach works for **WSL on Windows 11**. If you're on:
- **Native Linux**: Use `aplay`, `paplay`, or `ffplay` with your own sound files
- **macOS**: Use `afplay` with macOS system sounds
- **Native Windows**: Call PowerShell directly without the `/mnt/c/` path prefix

## Conclusion

Sound notifications bridge the gap between Claude Code's powerful CLI and the realities of multitasking. With just a few lines in your settings file, you can stay informed without staying glued to your terminal.

Give it a try and enjoy the satisfying *ding* when Claude's got something for you! 🔔
