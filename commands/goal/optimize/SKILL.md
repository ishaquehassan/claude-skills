---
name: goal:optimize
description: Optimize your social profiles for your goal. Usage /goal:optimize [linkedin|github|twitter|all]
argument-hint: [platform]
allowed-tools: [Read, Write, Edit, Glob, Grep, WebSearch, Bash, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__tabs_create_mcp, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__read_page, mcp__claude-in-chrome__get_page_text, mcp__claude-in-chrome__javascript_tool, mcp__claude-in-chrome__form_input, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__find]
---

# /goal:optimize

You are a profile optimization specialist. Audit and optimize the user's social profiles to align with their goal.

## Prerequisites

Read:
- `goal-definition.md` (goal, category, target audience)
- `~/.claude/plugins/data/goal-agent@ishaquehassan/natural-content-rules.md` (MANDATORY: natural writing rules for all profile text. Read this BEFORE writing any profile copy.)
- `goal-profile.md` (social URLs, skills, achievements)
- `profile-audit.md` (previous audit results)

Parse `$ARGUMENTS` for platform. Default to "linkedin" if empty. Options: linkedin, github, twitter, all.

## CRITICAL: Browser Automation Technical Reference

### Before ANY browser action:
1. Call `tabs_context_mcp` to get current browser state
2. Create a new tab for the work (don't reuse existing tabs)
3. Never reuse tab IDs from previous sessions

### OS-Aware Keyboard Shortcuts:
For clipboard operations, detect OS first:
```javascript
const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
// Use Meta (Cmd) for Mac, Control (Ctrl) for Windows/Linux
```
- Paste: Cmd+V (Mac) / Ctrl+V (Windows/Linux)
- Select All: Cmd+A (Mac) / Ctrl+A (Windows/Linux)
- Copy: Cmd+C (Mac) / Ctrl+C (Windows/Linux)

### LinkedIn Profile Editing Workarounds:
- contenteditable fields are often NOT directly accessible via JS
- ALWAYS use clipboard approach: navigator.clipboard.writeText("text") then Cmd/Ctrl+V
- Skills drag-and-drop reorder does NOT work via automation
- Top 5 skills: edit via About section edit dialog, NOT Skills page
- Featured section: "Add a link" then paste URL, LinkedIn auto-fetches preview
- Image/video areas: NEVER scroll through them (triggers fullscreen lightbox)

---

## LinkedIn Optimization

### Step 1: Navigate and Read Current Profile

Navigate to the user's LinkedIn profile URL from `goal-profile.md`.
Use `get_page_text` to read the full profile content.

### Step 2: Audit Against Goal

Score each section 0-10 based on goal alignment:

**Headline (weight: 25%)**
- Does it mention the goal-relevant skill/role FIRST?
- Is the most impressive credential prominent?
- Is it under 120 characters?
- Developer Expert goal: lead with framework/technology contribution
- Job goal: Target role title + key skill
- YouTube goal: Channel identity + niche
- Scoring: 10 = perfectly aligned, 0 = completely irrelevant to goal

**About Section (weight: 25%)**
- Does the FIRST LINE mention goal-relevant achievements?
- Are specific accomplishments listed (not vague claims)?
- Does it include relevant keywords for the goal niche?
- Is it between 1000-2600 characters?
- Scoring: 10 = leads with goal achievements, 0 = no mention of goal area

**Top 5 Skills (weight: 15%)**
- Are all 5 skills relevant to the goal niche?
- Remove irrelevant skills (e.g., Java/Python if your goal is in a different stack)
- Add missing niche skills
- Scoring: 10 = all 5 perfectly aligned, 0 = none relevant

**Featured Section (weight: 15%)**
- Are the best goal-relevant content pieces pinned?
- Articles, posts, or projects that demonstrate expertise
- Scoring: 10 = strong portfolio, 0 = empty or irrelevant

**Banner Image (weight: 10%)**
- Does it reflect professional identity for this goal?
- Custom > generic company banner > default LinkedIn banner
- Scoring: 10 = custom goal-aligned banner, 0 = default

**Open to Work Badge (weight: 5%)**
- Networking/expert goals: should be OFF (looks desperate)
- Job hunting: can be ON but "visible to recruiters only"
- Scoring: 10 = appropriate for goal, 0 = counterproductive

**Experience Descriptions (weight: 5%)**
- Do current role descriptions highlight goal-relevant work?

### Step 3: Generate Recommendations

For each section scoring below 7/10, generate specific changes:

```
LinkedIn Profile Audit Results
==============================
Overall Score: [X]/10

Headline: [X]/10
  Current: "[current headline]"
  Suggested: "[optimized headline]"
  Why: [reason]

About: [X]/10
  Issue: [what's wrong]
  Suggested first line: "[new opening]"
  Full suggested about: [complete text]

Skills: [X]/10
  Remove: [skill1], [skill2]
  Add: [skill1], [skill2]
  New top 5: [ordered list]

Featured: [X]/10
  Add: [content piece 1 URL]
  Add: [content piece 2 URL]

Banner: [X]/10
  Suggestion: [what kind of banner to create/upload]

Open to Work: [X]/10
  Current: [on/off]
  Suggested: [on/off and why]
```

### Step 4: Ask for Approval

Show all changes and ask: "Should I apply these changes? You can say 'all', list specific sections, or 'skip'."

### Step 5: Execute Approved Changes

**Headline/About editing:**
1. Navigate to profile page
2. Click the pencil/edit icon on the intro/about section
3. Wait for edit dialog to load
4. For text fields, use clipboard approach:
   - Run JS: `navigator.clipboard.writeText("new text here")`
   - Click on the field to focus it
   - Select all: Cmd+A (Mac) or Ctrl+A (Windows)
   - Paste: Cmd+V (Mac) or Ctrl+V (Windows)
5. Click Save button
6. Verify change by reading the profile again

**Skills editing:**
1. Navigate to About section edit
2. In the edit dialog, find the skills section
3. Remove irrelevant skills (click X next to skill name)
4. Add new skills (type in search field, select from suggestions)
5. Save

**Featured section:**
1. Scroll to Featured section
2. Click "+" or "Add" button
3. Select "Add a link"
4. Paste the URL
5. Wait for LinkedIn to fetch preview
6. Click Save/Done

### Step 6: Update Profile Audit

Update `profile-audit.md` with new scores and changes made:

```markdown
## LinkedIn
- Score: [new score]/10 (was [old score]/10)
- Last audited: [today]
- Changes made:
  - Headline: updated to "[new headline]"
  - About: rewritten with [goal] focus
  - Skills: removed [X], added [Y]
```

---

## GitHub Optimization

### Step 1: Read Current State

Use `gh` CLI commands:
```bash
gh api user --jq '.bio, .blog, .company, .location'
gh api users/USERNAME/repos --jq 'sort_by(-.stargazers_count) | .[0:10] | .[] | {name, stars: .stargazers_count, description}'
```

### Step 2: Audit

- **Bio**: Does it mention goal-relevant expertise? Max 160 chars
- **Pinned repos**: Are the most goal-relevant repos pinned?
- **Profile README**: Does it exist? Does it highlight goal achievements?
- **Contribution graph**: Is it active?

### Step 3: Suggest and Execute

Bio update via gh CLI:
```bash
gh api -X PATCH /user -f bio="new bio text"
```

For pinned repos and README, suggest changes and let user approve.

---

## Twitter/X Optimization

### Step 1: Read via Browser

Navigate to user's Twitter profile, read bio, pinned tweet, header.

### Step 2: Audit

- Bio alignment with goal
- Pinned tweet relevance
- Header image

### Step 3: Execute via Browser

Similar clipboard approach for bio editing.

---

## Output

After all optimizations:

```
Profile Optimization Complete
=============================
Platform: [platform]

Before: [X]/10
After: [Y]/10

Changes applied:
1. [change 1]
2. [change 2]
3. [change 3]

Files updated: profile-audit.md
Next: /goal:write to create content for your optimized profile
```
