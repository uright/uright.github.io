---
title: "Docker Desktop Volume Backup and Restore"
description: "Simple, portable bash scripts to backup and restore Docker volumes - perfect for migrating OpenWebUI data or any containerized application"
date: 2026-01-07 20:56:47 -0500
categories: [Tech, Docker]
tags: [docker, volumes, backup, openwebui, tutorial]
image:
  path: /assets/img/2026-01-07-docker-desktop-volume-backup-and-restore/docker-volumes.png
  alt: "Docker volume backup and restore process"
---

## Introduction

If you're running applications like OpenWebUI in Docker Desktop, you've probably wondered: *"How do I safely backup my data before upgrading or migrating to a new machine?"*

Docker volumes are great for persistent storage, but backing them up isn't as straightforward as copying a folder. I ran into this myself and put together two simple scripts that handle the heavy lifting for you.

These scripts work across **macOS**, **WSL**, and **Git Bash on Windows** - so you're covered regardless of your development environment.

## The Scripts

### Export (Backup)

```bash
#!/bin/bash
# export-volume.sh

VOLUME_NAME=$1
OUTPUT_FILE=$2

if [ -z "$VOLUME_NAME" ] || [ -z "$OUTPUT_FILE" ]; then
    echo "Usage: ./export-volume.sh <volume_name> <output_file.tar.gz>"
    echo "Example: ./export-volume.sh my-volume ./backup/my-volume.tar.gz"
    exit 1
fi

# Check if volume exists
if ! docker volume inspect "$VOLUME_NAME" > /dev/null 2>&1; then
    echo "Error: Volume '$VOLUME_NAME' does not exist"
    exit 1
fi

echo "Exporting volume: $VOLUME_NAME"
echo "Output file: $OUTPUT_FILE"

# Create output directory if it doesn't exist
mkdir -p "$(dirname "$OUTPUT_FILE")"

# Export the volume
docker run --rm \
    -v "$VOLUME_NAME":/source:ro \
    -v "$(pwd)":/backup \
    alpine \
    tar czf "/backup/$OUTPUT_FILE" -C /source .

echo "Export completed successfully!"
echo "File size: $(du -h "$OUTPUT_FILE" | cut -f1)"
```


### Import (Restore)

```bash
#!/bin/bash
# import-volume.sh

VOLUME_NAME=$1
INPUT_FILE=$2

if [ -z "$VOLUME_NAME" ] || [ -z "$INPUT_FILE" ]; then
    echo "Usage: ./import-volume.sh <volume_name> <input_file.tar.gz>"
    echo "Example: ./import-volume.sh my-volume ./backup/my-volume.tar.gz"
    exit 1
fi

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' does not exist"
    exit 1
fi

echo "Importing to volume: $VOLUME_NAME"
echo "Input file: $INPUT_FILE"

# Create volume if it doesn't exist
if ! docker volume inspect "$VOLUME_NAME" > /dev/null 2>&1; then
    echo "Creating volume: $VOLUME_NAME"
    docker volume create "$VOLUME_NAME"
fi

# Import the volume
docker run --rm \
    -v "$VOLUME_NAME":/target \
    -v "$(pwd)":/backup \
    alpine \
    sh -c "rm -rf /target/* /target/..?* /target/.[!.]* 2>/dev/null; tar xzf /backup/$INPUT_FILE -C /target"

echo "Import completed successfully!"
```

## How to Use

**1. Make the scripts executable:**

```bash
chmod +x export-volume.sh import-volume.sh
```

**2. Export a volume to a backup file:**

```bash
./export-volume.sh my-volume-name ./backups/my-volume.tar.gz
```

**3. Import from a backup file:**

```bash
./import-volume.sh my-volume-name ./backups/my-volume.tar.gz
```

## Helpful Docker Commands

Need to find your volume names? These commands come in handy:

```bash
# List all volumes
docker volume ls

# Get details about a specific volume
docker volume inspect my-volume-name
```

## Wrapping Up

These scripts have saved me time when migrating OpenWebUI between machines and before major updates. Feel free to adapt them for any Docker volume you need to backup - they're not specific to any particular application.

Got questions or improvements? Drop a comment below!
