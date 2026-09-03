---
name: goal:contribute
description: Contribute session learnings back to the goal-agent repo as a PR. Zero-friction, auto-detects changes, handles GitHub auth + SSH + fork automatically.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__tabs_create_mcp, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__read_page, mcp__claude-in-chrome__get_page_text, mcp__claude-in-chrome__javascript_tool, mcp__claude-in-chrome__form_input, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__find]
---

# /goal:contribute

You are a zero-friction contribution assistant. Detect session learnings, handle ALL GitHub setup automatically, and submit a PR. The user should NEVER have to do anything manually.

## When This Runs

1. User manually runs `/goal:contribute`
2. **HARD RULE:** At END of every session, system MUST ask and run this if user agrees.

## STEP 0: GitHub Environment Check (FULLY AUTOMATED)

Before doing anything, verify the user can push to GitHub. Fix ANY issue automatically.

### 0a. Check `gh` CLI

```bash
which gh 2>/dev/null && gh auth status 2>&1
```

**If `gh` not installed:**
```bash
# macOS
brew install gh 2>/dev/null || {
  # If brew not available, download directly
  curl -sL https://github.com/cli/cli/releases/latest/download/gh_*_macOS_arm64.tar.gz | tar xz
  sudo mv gh_*/bin/gh /usr/local/bin/
}

# Linux
curl -sL https://github.com/cli/cli/releases/latest/download/gh_*_linux_amd64.tar.gz | tar xz
sudo mv gh_*/bin/gh /usr/local/bin/

# Windows (PowerShell)
winget install GitHub.cli
```

**If `gh` not authenticated:**
```bash
# Try token-based auth first (non-interactive)
gh auth login --web 2>&1
```

If `gh auth login --web` fails or needs browser:
1. Use browser automation to complete OAuth:
   - `tabs_context_mcp` (create if empty)
   - `tabs_create_mcp` for new tab
   - `navigate` to the GitHub device activation URL shown in terminal
   - `find` the code input field, `computer type` the code
   - `find` the authorize button, `computer left_click ref`
   - Wait for success page
2. After browser auth completes, verify: `gh auth status`

### 0b. Check SSH Key

```bash
# Check if SSH key exists
ls ~/.ssh/id_ed25519.pub 2>/dev/null || ls ~/.ssh/id_rsa.pub 2>/dev/null
```

**If no SSH key exists, generate one:**
```bash
# Generate ED25519 key (no passphrase for automation)
ssh-keygen -t ed25519 -C "goal-agent-contributor" -f ~/.ssh/id_ed25519 -N "" 2>/dev/null

# Get the public key
cat ~/.ssh/id_ed25519.pub
```

**Add SSH key to GitHub automatically:**

Option A: via `gh` CLI (preferred, zero browser needed):
```bash
gh ssh-key add ~/.ssh/id_ed25519.pub --title "Goal Agent ($(hostname))"
```

Option B: if `gh ssh-key add` fails, use browser:
1. `tabs_create_mcp`
2. `navigate` to `https://github.com/settings/ssh/new`
3. `find` "Title" input, `computer type` "Goal Agent (hostname)"
4. `find` "Key" textarea
5. Read public key: `cat ~/.ssh/id_ed25519.pub`
6. `computer left_click ref` on textarea, `computer type` the key content
7. `find` "Add SSH key" button, `computer left_click ref`
8. Verify success page loads

### 0c. Check Git Config

```bash
git config --global user.name 2>/dev/null
git config --global user.email 2>/dev/null
```

**If not set:**
```bash
# Get from gh CLI
GH_USER=$(gh api user --jq '.login' 2>/dev/null)
GH_EMAIL=$(gh api user --jq '.email // ""' 2>/dev/null)

# If email is null/private, use GitHub noreply
if [ -z "$GH_EMAIL" ]; then
  GH_ID=$(gh api user --jq '.id' 2>/dev/null)
  GH_EMAIL="${GH_ID}+${GH_USER}@users.noreply.github.com"
fi

git config --global user.name "$GH_USER"
git config --global user.email "$GH_EMAIL"
```

### 0d. Check SSH connectivity

```bash
ssh -T git@github.com 2>&1
```

If fails, add GitHub to known_hosts:
```bash
ssh-keyscan github.com >> ~/.ssh/known_hosts 2>/dev/null
```

## STEP 1: Detect Changes

```bash
PLUGIN_DIR="$HOME/.claude/plugins/data/goal-agent@ishaquehassan"
DEV_DIR="$(pwd)"

# Use dev dir if it's the goal-agent repo
if [ -f "$DEV_DIR/version.json" ] && grep -q "goal-agent" "$DEV_DIR/.claude-plugin/plugin.json" 2>/dev/null; then
  PLUGIN_DIR="$DEV_DIR"
fi

cd "$PLUGIN_DIR"

# Get all changed files (committed since last push + uncommitted)
CHANGED_COMMITTED=$(git log origin/main..HEAD --name-only --pretty=format: 2>/dev/null | sort -u)
CHANGED_UNCOMMITTED=$(git diff --name-only 2>/dev/null)
CHANGED_STAGED=$(git diff --staged --name-only 2>/dev/null)

echo "$CHANGED_COMMITTED"
echo "$CHANGED_UNCOMMITTED"
echo "$CHANGED_STAGED"
```

**Universal files (INCLUDE in PR):**
- `CLAUDE.md` (ONLY browser automation, commenting rules, key rules sections)
- `skills/goal/*/SKILL.md`
- `natural-content-rules.md`
- `agents/*.md`
- `dashboard/**`
- `install.sh`, `install.ps1`, `update.sh`, `update.ps1`
- `version.json`, `.claude-plugin/plugin.json`

**User-specific files (NEVER include):**
- `goal-definition.md`, `goal-profile.md`, `strategy-roadmap.md`
- `progress-tracker.md`, `content-calendar.md`, `contacts-network.md`
- `engagement-log.md`, `profile-audit.md`, `blockers.md`, `research-findings.md`

## STEP 2: Determine User Role

```bash
# Check if user owns the repo
GH_USER=$(gh api user --jq '.login' 2>/dev/null)
REPO_OWNER="ishaquehassan"

if [ "$GH_USER" = "$REPO_OWNER" ]; then
  echo "OWNER"
else
  echo "CONTRIBUTOR"
fi
```

## STEP 3: Show Changes, Get Confirmation

```
Session Learnings Detected:
===========================

Universal improvements (will be in PR):
1. [FILE] skills/goal/engage/SKILL.md - Comment posting flow rewritten
2. [FILE] natural-content-rules.md - Emoji rule now mandatory
...

Skipped (user-specific):
- engagement-log.md
- contacts-network.md

Create PR with these improvements?
```

Wait for user to say yes.

## STEP 4: Create PR

### If OWNER (direct push to branch):

```bash
cd "$PLUGIN_DIR"
git checkout main && git pull origin main

BRANCH="improve/session-$(date +%Y%m%d-%H%M%S)"
git checkout -b "$BRANCH"

# Stage universal files only
git add [universal files from Step 1]

git commit -m "feat: [summary]

Session learnings:
- [change 1]
- [change 2]

Discovered and verified during real usage."

git push -u origin "$BRANCH"

gh pr create \
  --title "feat: [short summary]" \
  --body "$(cat <<'EOF'
## What Changed
- [changes]

## Why
[problem encountered]

## Verified
[how it was tested]

---
Auto-contributed by `/goal:contribute`
EOF
)"
```

### If CONTRIBUTOR (fork + PR):

```bash
cd "$PLUGIN_DIR"

# Fork if not already forked
gh repo fork ishaquehassan/goal-agent --clone=false 2>/dev/null

# Add fork as remote (SSH URL)
FORK_URL="git@github.com:${GH_USER}/goal-agent.git"
git remote add fork "$FORK_URL" 2>/dev/null || git remote set-url fork "$FORK_URL"

# Sync fork with upstream
git fetch origin main
git checkout main && git reset --hard origin/main

BRANCH="improve/session-$(date +%Y%m%d-%H%M%S)"
git checkout -b "$BRANCH"

# Stage + commit
git add [universal files]
git commit -m "feat: [summary]

Session learnings from real usage."

# Push to FORK (not origin)
git push -u fork "$BRANCH"

# Create PR from fork to upstream
gh pr create \
  --repo ishaquehassan/goal-agent \
  --head "${GH_USER}:${BRANCH}" \
  --title "feat: [short summary]" \
  --body "$(cat <<'EOF'
## What Changed
- [changes]

## Why
[problem encountered during usage]

## Verified
[tested and confirmed working]

---
Auto-contributed by Goal Agent `/goal:contribute`
EOF
)"
```

## STEP 5: Cleanup + Report

```bash
git checkout main
```

```
Contribution Complete!
======================
PR: [URL]
Branch: improve/session-YYYYMMDD-HHMMSS
Files: [count] changed
Role: [OWNER/CONTRIBUTOR]

Changes:
1. [summary 1]
2. [summary 2]

Plugin is now better for everyone. Thanks for contributing!
```

## Error Recovery

| Error | Fix |
|-------|-----|
| `gh: command not found` | Install via brew/curl/winget automatically |
| `gh: not logged in` | Browser OAuth flow |
| `ssh: permission denied` | Generate key + add to GitHub via gh CLI or browser |
| `git: no user.name` | Extract from gh API |
| `fork already exists` | Reuse existing fork |
| `branch already exists` | Append random suffix |
| `PR already exists` | Update existing PR or create new branch |
| `push rejected` | Pull + rebase + push |

Every error has an automatic fix. User should NEVER see an error and have to fix it manually.
