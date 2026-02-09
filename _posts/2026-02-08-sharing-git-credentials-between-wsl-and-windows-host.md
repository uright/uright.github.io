---
title: "Sharing Git Credentials Between WSL and Windows Host"
description: "Configure git credential management to seamlessly bridge WSL and Windows host systems. Discover quick setup tricks that allow WSL to access your host's stored credentials without duplication."
date: 2026-02-08 21:33:20 -0500
categories: [Tech, Development]
tags: [wsl, git, credentials, windows, development, quick-tip]
image:
  path: /assets/img/2026-02-08-sharing-git-credentials-between-wsl-and-windows-host/wsl-git-credentials.png
  alt: "WSL and Windows host sharing git credentials"
---

## Introduction

If you're using Windows Subsystem for Linux (WSL), you've probably noticed that git credentials aren't automatically shared with your Windows host. This means you either need to generate separate SSH keys for WSL or manually configure credentials each time. There's a better way: configure WSL to use your Windows Git Credential Manager directly.

This quick tip shows you exactly how to set it up with just two commands.

## Prerequisites

Before you proceed, make sure you have:
- **Git for Windows** installed on your Windows host machine
- WSL2 installed and running
- Access to a terminal within your WSL environment

## The Two Commands

### 1. Configure the Credential Helper

```bash
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"
```

**What it does:**
- Points git to use Windows' Git Credential Manager for storing and retrieving credentials
- `/mnt/c/` is how WSL maps to your Windows C: drive
- This path is the default location where Git for Windows installs the credential manager

**Breaking down the path:**
- `Program\ Files/Git/` → Where Git for Windows installs (the backslash escapes the space)
- `mingw64/bin/` → Contains the executable binaries
- `git-credential-manager.exe` → The credential manager application


## Step-by-Step Setup

**Step 1:** Open your WSL terminal

**Step 2:** Run the credential helper command:
```bash
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"
```

**Step 3:** Verify it worked by checking your git config:
```bash
git config --global --list | grep credential
```

You should see:
```
credential.helper=/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe
```

## Testing Your Setup

1. **Try cloning a private repository:**
   ```bash
   git clone https://github.com/your-username/private-repo.git
   ```

2. **First attempt:** You'll get a Windows dialog prompting you to authenticate

3. **Subsequent attempts:** Your credentials will be cached and used automatically

## Troubleshooting

**"Command not found" error:**
- Verify Git for Windows is installed: `ls /mnt/c/Program\ Files/Git/`
- Make sure the path matches your installation

**"Permission denied" error:**
- Try making the executable runnable:
  ```bash
  chmod +x "/mnt/c/Program Files/Git/mingw64/bin/git-credential-manager.exe"
  ```

**Credentials aren't being saved:**
- Check that Windows Credential Manager is enabled: Settings → Credential Manager → Windows Credentials
- Verify Git for Windows has credential storage configured

**Different Git installation path:**
- If you installed Git to a custom location, adjust the path:
  ```bash
  git config --global credential.helper "your/custom/path/git-credential-manager.exe"
  ```

## Why This Works

- **Single credential store:** Manage credentials from Windows, access them in WSL
- **Better security:** Uses Windows Credential Manager's encryption
- **No duplication:** One set of credentials for all your tools
- **Seamless:** Works across Git Bash, PowerShell, WSL, and IDE integrations

## Reverting if Needed

If you want to remove this configuration:

```bash
git config --global --unset credential.helper
```

## Conclusion

That's it! Two quick commands and you've eliminated the credential management headache between WSL and Windows. Your git workflow becomes seamless, and you only have to manage credentials in one place—Windows Credential Manager. No more separate SSH keys, no more duplicate setup, just smooth development across both environments.