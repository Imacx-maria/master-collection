#!/bin/bash
# AI_OS Sync Script (macOS/Linux) — copies master template into a project's AI_OS/ folder
# Usage: ./sync-to-project.sh /path/to/your/project
#
# Pulls latest from GitHub first, then rsyncs template files.

if [ -z "$1" ]; then
    echo "Usage: ./sync-to-project.sh <project-path>"
    echo "Example: ./sync-to-project.sh ~/Projects/jocril"
    exit 1
fi

PROJECT="$1"
MASTER="$HOME/AI_OS"
TARGET="$PROJECT/AI_OS"

echo "=== Pulling latest AI_OS from GitHub ==="
cd "$MASTER"
git pull origin main

echo "=== Syncing AI_OS to $TARGET ==="
mkdir -p "$TARGET"

rsync -av --exclude='.git' \
    --exclude='*.js' \
    --exclude='*.json' \
    --exclude='clipboard_*' \
    --exclude='SESSION-PROMPTS/SESSIONS/' \
    --exclude='sync-to-project.*' \
    --exclude='.gitignore' \
    "$MASTER/" "$TARGET/"

echo "=== Syncing .claude/ structural files ==="
CLAUDE_SRC="$(dirname "$MASTER")/.claude"
CLAUDE_DST="$PROJECT/.claude"

mkdir -p "$CLAUDE_DST/rules"
mkdir -p "$CLAUDE_DST/hooks"
mkdir -p "$CLAUDE_DST/commands"

# Copy settings.json (overwrite — template-managed)
[ -f "$CLAUDE_SRC/settings.json" ] && cp "$CLAUDE_SRC/settings.json" "$CLAUDE_DST/settings.json"

# Copy rules (overwrite — template-managed)
[ -d "$CLAUDE_SRC/rules" ] && rsync -av "$CLAUDE_SRC/rules/" "$CLAUDE_DST/rules/"

# Copy hooks (overwrite — template-managed)
[ -d "$CLAUDE_SRC/hooks" ] && rsync -av "$CLAUDE_SRC/hooks/" "$CLAUDE_DST/hooks/"

# Copy commands (overwrite — template-managed)
[ -d "$CLAUDE_SRC/commands" ] && rsync -av "$CLAUDE_SRC/commands/" "$CLAUDE_DST/commands/"

# Copy context-essentials.md if present (overwrite — template-managed, then adapt per project if needed)
[ -f "$CLAUDE_SRC/context-essentials.md" ] && cp "$CLAUDE_SRC/context-essentials.md" "$CLAUDE_DST/context-essentials.md"

# Create CLAUDE.local.md if it doesn't exist (personal, not overwritten)
[ -f "$CLAUDE_DST/CLAUDE.local.md" ] || echo "# Personal Overrides (gitignored)" > "$CLAUDE_DST/CLAUDE.local.md"

# Ensure root .gitignore contains local override entries
if [ -f "$PROJECT/.gitignore" ]; then
    grep -qxF 'CLAUDE.local.md' "$PROJECT/.gitignore" || echo 'CLAUDE.local.md' >> "$PROJECT/.gitignore"
    grep -qxF 'settings.local.json' "$PROJECT/.gitignore" || echo 'settings.local.json' >> "$PROJECT/.gitignore"
else
    printf "CLAUDE.local.md\nsettings.local.json\n" > "$PROJECT/.gitignore"
fi

echo "=== Done! AI_OS + .claude/ synced to $PROJECT ==="
