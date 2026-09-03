---
name: goal:update
description: Update Goal Agent plugin to the latest version
allowed-tools: [Bash, Read, Write, WebFetch]
---

# /goal:update

You are the Goal Agent updater. Update the plugin to the latest version from GitHub.

## Step 1: Detect Current Installation

```bash
PLUGIN_DIR="$HOME/.claude/plugins/data/goal-agent@ishaquehassan"

if [ -d "$PLUGIN_DIR/.git" ]; then
  echo "GIT_INSTALL"
elif [ -d "$PLUGIN_DIR" ]; then
  echo "COPY_INSTALL"
else
  echo "NOT_INSTALLED"
fi
```

## Step 2: Get Current Version

Read `$HOME/.claude/plugins/data/goal-agent@ishaquehassan/version.json` if it exists.
If not, assume version "1.0.0" (pre-update system).

## Step 3: Check Remote Version

Fetch `https://raw.githubusercontent.com/ishaquehassan/goal-agent/main/version.json` and compare.

If already on latest, tell user "Already on latest version X.Y.Z" and stop.

## Step 4: Update Based on Install Type

Check if git is available: `command -v git`

### If git is available:

**GIT_INSTALL (git repo exists):**
```bash
PLUGIN_DIR="$HOME/.claude/plugins/data/goal-agent@ishaquehassan"
cd "$PLUGIN_DIR"
git fetch origin main
git reset --hard origin/main
```

**COPY_INSTALL (old style, no git):**
```bash
PLUGIN_DIR="$HOME/.claude/plugins/data/goal-agent@ishaquehassan"
rm -rf "$PLUGIN_DIR"
mkdir -p "$(dirname "$PLUGIN_DIR")"
git clone https://github.com/ishaquehassan/goal-agent.git "$PLUGIN_DIR"
```

### If git is NOT available (zip fallback):
```bash
PLUGIN_DIR="$HOME/.claude/plugins/data/goal-agent@ishaquehassan"
TEMP_DIR=$(mktemp -d)
curl -sL "https://github.com/ishaquehassan/goal-agent/archive/refs/heads/main.zip" -o "$TEMP_DIR/goal-agent.zip"
unzip -q "$TEMP_DIR/goal-agent.zip" -d "$TEMP_DIR"
rm -rf "$PLUGIN_DIR"
mkdir -p "$(dirname "$PLUGIN_DIR")"
mv "$TEMP_DIR/goal-agent-main" "$PLUGIN_DIR"
rm -rf "$TEMP_DIR"
```

### If NOT_INSTALLED:
Tell user to install first: `curl -sL https://raw.githubusercontent.com/ishaquehassan/goal-agent/main/install.sh | bash`

## Step 5: Sync Commands

After pulling/cloning, re-copy all skill files to commands directory:

```bash
PLUGIN_DIR="$HOME/.claude/plugins/data/goal-agent@ishaquehassan"
COMMANDS_DIR="$HOME/.claude/commands/goal"
AGENTS_DIR="$HOME/.claude/agents"

mkdir -p "$COMMANDS_DIR"
mkdir -p "$AGENTS_DIR"

# Sync skills
for skill_dir in "$PLUGIN_DIR/skills/goal"/*/; do
  if [ -d "$skill_dir" ]; then
    skill_name=$(basename "$skill_dir")
    if [ -f "$skill_dir/SKILL.md" ]; then
      cp "$skill_dir/SKILL.md" "$COMMANDS_DIR/$skill_name.md"
    fi
  fi
done

# Sync agents
cp "$PLUGIN_DIR/agents/"*.md "$AGENTS_DIR/" 2>/dev/null || true
```

## Step 6: Report

Show:
- Previous version
- New version
- Changelog from version.json
- "Update complete! Restart Claude Code to use new commands."

## Platform Detection

Detect OS and use appropriate commands:
- macOS/Linux: bash commands above
- Windows: Use PowerShell equivalents with `$env:USERPROFILE` instead of `$HOME`

## Important
- NEVER ask for confirmation, just update
- If git pull fails due to conflicts, do `git fetch && git reset --hard origin/main`
- If any step fails, show the error and suggest manual reinstall
- If git is not available, always use zip download fallback
