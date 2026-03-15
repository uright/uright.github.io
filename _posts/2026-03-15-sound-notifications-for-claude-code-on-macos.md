---
title: "Sound Notifications for Claude Code on macOS"
description: "Quick tip: Add audio alerts to Claude Code using macOS built-in system sounds when it stops or needs attention"
date: 2026-03-15 00:33:03 -0400
categories: [Tech, Quick Tips]
tags: [claude-code, macos, productivity, cli]
image:
  path: /assets/img/2026-03-15-sound-notifications-for-claude-code-on-macos/hero-image.png
  alt: "Claude Code with sound notifications on macOS using built-in system sounds"
---

## The Problem

When you're using Claude Code on macOS and multitasking—maybe you've switched to another app or stepped away—you might miss when Claude finishes a task or needs your attention. Without visual focus on the terminal, you're left checking back repeatedly or risking delays.

## The Solution

If you've seen the [WSL/Windows version of this tip]({% post_url 2026-02-24-sound-notifications-for-claude-code-on-wsl %}), you already know the idea — this is the macOS equivalent, and it's even simpler.

Claude Code supports **hooks** in its settings that trigger commands on specific events. macOS ships with `afplay`, a built-in command-line audio player, plus **14 system sound files** that require zero downloads. Together, they give you audio notifications in a single line of config.

Two key events to catch:
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
            "command": "afplay /System/Library/Sounds/Glass.aiff"
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
            "command": "afplay /System/Library/Sounds/Blow.aiff"
          }
        ]
      }
    ]
  }
}
```

That's it. No PowerShell, no scripts, no downloads.

## How It Works

1. **`afplay`**: macOS's built-in command-line audio player, located at `/usr/bin/afplay` — already in your PATH
2. **System sounds**: `/System/Library/Sounds/` contains `.aiff` files shipped with every Mac
3. **Unique sounds**: `Glass.aiff` for Stop events (task complete), `Blow.aiff` for Notification events (needs attention)
4. **Empty matcher**: `"matcher": ""` means the hook triggers for all events of that type

## Available Built-in Sounds

macOS includes 14 system sounds you can use immediately:

| Sound            | Character                           |
| ---------------- | ----------------------------------- |
| `Basso.aiff`     | Deep, low thud                      |
| `Blow.aiff`      | Wind blow ✓ great for Notification  |
| `Bottle.aiff`    | Hollow bottle tap                   |
| `Frog.aiff`      | Frog croak                          |
| `Funk.aiff`      | Bass guitar pop                     |
| `Glass.aiff`     | Glass clink ✓ great for Stop        |
| `Hero.aiff`      | Triumphant fanfare                  |
| `Morse.aiff`     | Morse code beep                     |
| `Ping.aiff`      | Sonar ping                          |
| `Pop.aiff`       | Cork pop                            |
| `Purr.aiff`      | Mechanical purr                     |
| `Sosumi.aiff`    | Classic Mac alert                   |
| `Submarine.aiff` | Submarine sonar                     |
| `Tink.aiff`      | Small metal tink                    |

Preview any of them from your terminal:

```bash
afplay /System/Library/Sounds/Glass.aiff
```

## Testing

After saving the configuration, run a Claude Code command and switch windows. You should hear:
- `Glass.aiff` when Claude stops/completes
- `Blow.aiff` when Claude needs your input

## Bonus Tips

**Non-blocking playback**: Add `&` to run the sound in the background so it doesn't hold up Claude's next action:
```json
"command": "afplay /System/Library/Sounds/Glass.aiff &"
```

**Customize your sounds**: Swap in any `.aiff` from `/System/Library/Sounds/` — just update the filename in the config.

**Volume control**: `afplay` respects your system volume. Adjust in System Settings → Sound if needed.

**Your own sound files**: `afplay` supports `.aiff`, `.wav`, and `.mp3`. Point it at any file you like:
```json
"command": "afplay ~/Music/my-notification.mp3"
```

## Cross-Platform Note

This specific approach works for **native macOS**. If you're on:
- **WSL on Windows**: Use PowerShell + `Media.SoundPlayer` (see the [WSL post]({% post_url 2026-02-24-sound-notifications-for-claude-code-on-wsl %}))
- **Native Linux**: Use `aplay`, `paplay`, or `ffplay` with your own sound files

## Conclusion

Two lines of JSON and you'll never miss a Claude completion again. The satisfying *clink* of `Glass.aiff` is a small thing that makes long coding sessions noticeably better. 🔔