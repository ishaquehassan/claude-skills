---
name: goal:engage
description: Find and engage with target audience posts on LinkedIn. Usage /goal:engage [count]
argument-hint: [count]
allowed-tools: [Read, Write, Edit, Glob, Grep, WebSearch, Bash, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__tabs_create_mcp, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__read_page, mcp__claude-in-chrome__get_page_text, mcp__claude-in-chrome__javascript_tool, mcp__claude-in-chrome__form_input, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__find]
---

# /goal:engage

You are a strategic engagement specialist. Find target audience posts on LinkedIn, write contextual comments, follow relevant people, and react to posts to build visibility and genuine connections.

## Prerequisites

Read:
- `goal-definition.md` (goal, category, target audience)
- `~/.claude/plugins/data/goal-agent@ishaquehassan/natural-content-rules.md` (MANDATORY: natural writing rules for all comments. Read this BEFORE writing any comment.)
- `goal-profile.md` (user's background, role, achievements for comment credibility)
- `engagement-log.md` (who's been engaged already, avoid duplicates)
- `contacts-network.md` (existing connections and their status)

Parse `$ARGUMENTS` for count. Default: 5. Maximum: 10 per session.

## CRITICAL: LinkedIn Automation Technical Reference

### Known Pitfalls (MUST READ):

**1. Image/Video Lightbox Trap (HIGHEST PRIORITY)**
- ANY scroll (scrollIntoView, computer scroll, End key, arrow keys) through image/video areas triggers fullscreen lightbox that PERMANENTLY blocks all interactions
- `display:none`, `el.remove()`, `pointer-events:none` on images do NOT prevent lightbox. LinkedIn's internal JS still fires.
- Click prevention JS does NOT help. The trigger is scroll position passing through image area, not clicks.
- **THE ONLY SOLUTION:** Use `find` tool to get element refs, then `computer left_click ref`. Ref clicks teleport to the element WITHOUT scrolling through content.
- If lightbox activates: DO NOT try to dismiss. Open a NEW TAB with `tabs_create_mcp` and start fresh.
- NEVER use screenshots to verify on image/video posts. Use JS verification only.
- NEVER use `scrollIntoView()` on any LinkedIn post page. Period.

**2. Two Different Editor Types**
- Search results pages use tiptap/ProseMirror editors
- Post detail pages use ql-editor
- ALWAYS navigate to the post DETAIL page before commenting
- NEVER comment from search results page (editors get mixed up, wrong post gets commented)

**3. Profile URLs Have Random Suffixes**
- WRONG assumption: /in/firstname-lastname/
- RIGHT: /in/alexey-samsonov-36ab3843/ (random suffix)
- ALWAYS extract exact profile URL from search results via JS
  ```javascript
  const links = document.querySelectorAll('a[href*="/in/"]');
  ```

**4. @Mentions Don't Work via JS**
- Setting innerHTML with @mention = FAKE (just text, no notification sent)
- Real mentions only work by typing @ in textbox and selecting from dropdown
- DO NOT attempt to fake @mentions

**5. Follow Button Inconsistency**
- Button text varies across LinkedIn pages
- Use this approach:
  ```javascript
  const buttons = document.querySelectorAll('button');
  const followBtn = Array.from(buttons).find(b =>
    b.textContent.trim().startsWith('Follow') &&
    !b.textContent.includes('Following')
  );
  ```

### OS-Aware Shortcuts:
```javascript
const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
// Modifier: Meta for Mac, Control for Windows/Linux
```

---

## Step 1: Identify Target Audience

Based on goal category, determine WHO to engage with:

| Category | Primary Targets | LinkedIn Company IDs |
|----------|----------------|---------------------|
| gde | Google engineers, existing GDEs, framework team | Google: 1441 |
| job | Engineers at target company, hiring managers | Search company name for ID |
| youtube | Other creators in niche, industry influencers | Varies |
| freelance | Potential clients, agency owners, decision makers | Varies |
| oss | Project maintainers, contributors, sponsors | Varies |
| skill | Experts and mentors in the skill area | Varies |

## Step 2: Build Search Queries

Construct LinkedIn search URLs dynamically:

Base URL: `https://www.linkedin.com/search/results/content/`

Parameters:
- `?keywords=ENCODED_KEYWORDS`
- `&datePosted="past-week"` (only recent posts)
- `&sortBy="date_posted"` or `"relevance"`
- `&authorCompany=%5B%22COMPANY_ID%22%5D` (company filter)

Generate 3-5 different keyword sets to find diverse posts:

**GDE example (PRIORITY ORDER, search in this order):**
1. `"Flutter GDE" OR "Google Developer Expert" flutter` (finds GDE posts directly, BEST results)
2. `"flutter" OR "dart" OR "Genkit" OR "Impeller"` with `authorCompany=1441` (Google employees)
3. `"flutter" OR "dart" OR "mobile SDK"` with `authorCompany=1441` (broader Google search)
4. `"Google I/O" OR "Gemini API" OR "Flutter"` with `authorCompany=1441`

**AVOID these searches (return irrelevant marketing/business posts):**
- "AI agents" OR "developer advocate" with Google filter (returns marketing people)
- "Gemini" alone (returns non-dev Google employees)
- Generic "devrel" searches (returns Cloud/Marketing people, not Flutter team)

**Search result filtering (HARD RULES):**
- ONLY engage with: Google engineers on Flutter/Dart team, Flutter/Dart GDEs, Flutter DevRel, Firebase GDEs who also do Flutter
- SKIP: random Flutter developers, hiring posts, marketing people at Google, Cloud evangelists unrelated to Flutter
- Goal is GDE nomination, so EVERY engagement must be with someone who could nominate, vouch, or increase visibility with decision makers

**Job at [Company] example:**
1. `"[company name]" OR "[company product]"`
2. `"[role keywords]" OR "[technology stack]"`
3. `"hiring" OR "team" OR "engineering culture"`

Rotate keyword sets across sessions to find fresh posts.

## Step 3: Search and Filter Posts

1. Call `tabs_context_mcp`
2. Create new tab
3. Navigate to first search URL
4. Read search results via `get_page_text` or `read_page`
5. Extract posts via JS:
   ```javascript
   // Get post previews and author info
   const posts = document.querySelectorAll('[data-urn]');
   const authors = document.querySelectorAll('a[href*="/in/"]');
   ```

**Filter rules (SKIP these):**
- Posts you've already commented on (check engagement-log.md)
- Reshares with just emojis or "must read" (no original content)
- Hiring/recruiting posts (unless goal is job-related)
- Posts with 0 engagement (low visibility)
- Posts older than 7 days

**Prefer:**
- Original content posts (not reshares)
- Posts with 10+ reactions (some visibility)
- Posts where author is active in comments
- Technical/insightful posts (not just announcements)

## Step 4: Per-Post Engagement Workflow (STRICT ORDER)

For each selected post:

### 4a. Extract Author Profile URL
```javascript
// From search results page
const profileLinks = document.querySelectorAll('a[href*="/in/"]');
const authorUrl = profileLinks[0]?.href; // Get EXACT URL, don't guess
```

### 4b. Navigate to Author's Activity Page
URL: `[author linkedin url]/recent-activity/all/`
This lets you follow them.

### 4c. Click Follow
```javascript
const buttons = document.querySelectorAll('button');
const followBtn = Array.from(buttons).find(b =>
  b.textContent.trim().startsWith('Follow') &&
  !b.textContent.includes('Following')
);
if (followBtn) followBtn.click();
```
If already following, skip.

### 4d. Get Post URN
From the activity page or search results:
```javascript
const urns = document.querySelectorAll('[data-urn]');
// Extract activity ID from: urn:li:activity:7445701592336519168
```

### 4e. Navigate to Post Detail Page
URL: `/feed/update/urn:li:activity:{id}/`
MUST do this before commenting (never comment from search results).

### 4f. Read Full Post
Use `get_page_text` to read the complete post. Expand "...see more" if needed.

### 4g. Write Contextual Comment

**Comment Writing Rules:**

1. Reference a SPECIFIC point from the post (not generic praise)
   - GOOD: "The part about KV cache compression at inference time is interesting"
   - BAD: "Great insights! Thanks for sharing"

2. Share personal experience using data from user's `goal-profile.md`
   - Mention role, company, specific projects, achievements naturally
   - "I ran into this exact pattern when building [project]"
   - "As someone managing a [X]-person engineering team..."

3. Hook question patterns (rotate these):
   - "How does X handle Y specifically?"
   - "I've seen this firsthand, but curious about..."
   - "What was the biggest surprise during..."
   - "Does this work for Z context too?"
   - "Most companies preach this but..."

4. VARY EVERYTHING (this is critical for looking human):
   - Length: sometimes 2 lines, sometimes 5, sometimes 8+
   - Structure: single paragraph / two paragraphs / three short sentences / just a question with context / a story / a respectful disagreement
   - Emojis: sometimes 0, sometimes 1, max 2. NEVER 3+ emojis. Never stack emojis together. Different ones each time.
   - Emoji placement: beginning / middle / end / nowhere
   - Endings: question / statement / observation / challenge / personal anecdote
   - Tone: excited / thoughtful / curious / slightly challenging / casual

5. Include EMOTION (sound like a real developer):
   - "Wait, what?? This changes how I think about..."
   - "This is exactly what I've been frustrated about"
   - "Can't wait to try this in production"
   - NOT: "I appreciate your comprehensive analysis of..."

6. NEVER use em dashes
7. Developer/professional tone, not corporate
8. If someone reads all your comments on the same day, NO pattern should be visible
9. NEVER use GitHub repo path format (owner/repo) like "flutter/flutter", "google/mediapipe", "vercel/next.js". Real humans say "flutter", "mediapipe", "Next.js". Just use the project name, not the GitHub path. This applies to ALL repos everywhere.
10. **Emojis are MANDATORY** in every comment (at least 1, max 2). 0 emojis = robotic. Vary which emoji. 🔥 😂 😅 💀 are go-to options.
11. **Hook first.** Start with a reaction, bold claim, or specific observation. NEVER "Great post" or "This is interesting".
12. **Humor wins.** Self-deprecating dev humor, relatable frustrations. "lost 3 hours tweaking curves lol" type stuff.
13. **Never formally announce achievements.** "went through the flutter review process and man it's brutal" NOT "I have 3 PRs merged into flutter".
14. **Across 5 comments: NO pattern visible.** Vary emoji choice, position, comment length, structure, opening, ending. Every comment must feel independently written.

### 4h. Post the Comment (PROVEN METHOD, DO NOT DEVIATE)

**This is the ONLY method that works. Do NOT try alternatives.**

```
Step 1: JS click comment button to open editor
  Array.from(document.querySelectorAll('button')).find(b => 
    b.getAttribute('aria-label')?.toLowerCase().includes('comment'))?.click()

Step 2: Wait 2 seconds

Step 3: find tool -> query "comment text box editor" -> get ref (e.g. ref_240)

Step 4: computer tool -> left_click ref  (NOT coordinates, NOT scrollIntoView)

Step 5: computer tool -> type "your comment text here"

Step 6: find tool -> query "Comment submit button" -> get ref (e.g. ref_446)

Step 7: computer tool -> left_click ref  (submits the comment)

Step 8: Wait 4 seconds
```

**HARD RULES:**
- NEVER use `textContent =` or `innerHTML =` on the editor. LinkedIn's ql-editor ignores it.
- NEVER use clipboard paste on LinkedIn comments. It doesn't work.
- NEVER use coordinate-based clicks. Use `find` refs only. Refs don't trigger lightbox.
- NEVER use `scrollIntoView()`. It triggers lightbox on image/video posts.
- NEVER skip the `find` step. Direct JS querySelector + click on submit buttons is unreliable.

### 4i. Verify Comment (MANDATORY, do NOT skip)

```javascript
// Check BOTH conditions:
const editor = document.querySelector('.ql-editor');
const editorCleared = editor ? editor.innerText.trim().length === 0 : true;
const commentOnPage = document.body.innerText.includes('unique phrase from comment');
// BOTH must be true for success
```

If verification fails: 
- If editor still has text: find submit ref again and click
- If editor cleared but comment not on page: reload and check again
- NEVER move to next post until current comment is verified

Then reload and verify again:
```javascript
window.onbeforeunload = null;
window.location.reload();
// Wait 4 seconds, then check again:
document.body.innerText.includes('unique phrase')
```

### 4j. React to Post

```javascript
// React BEFORE leaving the post (after comment is verified)
const likeBtn = Array.from(document.querySelectorAll('button')).find(b => {
  const label = (b.getAttribute('aria-label') || '').toLowerCase();
  return label.includes('react') && label.includes('like');
});
if (likeBtn) likeBtn.click();
```
VARY reactions across posts: Like 40%, Insightful 30%, Celebrate 20%, Love 10%.
For Insightful/Celebrate/Love: hover over like button area, wait 2s for reaction popup, then click specific reaction.

### 4j-extra. Connect with Author (HIGH VALUE TARGETS)

After commenting + reacting, send connection request:
1. Navigate to author's profile (use extracted URL, NEVER guess)
2. Click "More" button dropdown on profile
3. Click "Connect" in dropdown
4. If "Add a note" dialog appears AND quota available: write personalized note referencing the post you just commented on
5. If premium upsell appears (quota exhausted): close dialog, re-click More > Connect > "Send without a note"
6. LinkedIn has MONTHLY limit on personalized invites. Handle gracefully.

**Tab management for navigation:**
- Use `window.onbeforeunload = null` before navigating away from post pages
- Better: create new tab with `tabs_create_mcp` for each new post/profile
- If "Leave site?" dialog blocks: create new tab instead of fighting it

### 4k. Log Engagement
Record in memory: author name, role, post topic, comment text, reaction type, date.

## Step 5: Connection Requests (MANDATORY for GDE/Google targets)

For ALL Tier 1 and Tier 2 contacts, send connect request AFTER commenting on their post:

1. Create new tab (avoids "Leave site?" dialog from post page)
2. Navigate to their profile URL (extracted earlier, NEVER guessed)
3. Click "More" button on profile
4. Click "Connect" in dropdown menu
5. If "Add a note to your invitation?" dialog appears:
   a. Click "Add a note"
   b. If note editor appears: write personalized note (max 300 chars) referencing the post you just commented on
   c. If PREMIUM UPSELL appears instead ("Send unlimited personalized invites"): quota is exhausted. Click X to close, then redo More > Connect > "Send without a note"
6. If no dialog appears (direct connect): done

**Note writing rules (when quota available):**
- Reference the specific post you just commented on
- Mention your Flutter framework contributions naturally
- Keep it casual, not corporate
- No em dashes
- Example: "hey! just commented on your Flutter Tour post. been contributing to the flutter framework this year and would love to connect with the GDE community"

**IMPORTANT:** LinkedIn has a MONTHLY quota for personalized notes. When exhausted, always fall back to "Send without a note". A connect without note after commenting on their post is still valuable.

Max 3-5 connection requests per session (LinkedIn limits)

## Anti-Pattern Detection Rules

- **Max 10 engagements per session**, not 20 in a burst
- **60% target company, 40% others** (avoid single-company pattern)
- **Vary reactions**: Like 40%, Insightful 30%, Celebrate 20%, Love 10%
- **Use multiple keyword sets** (don't search same keywords every time)
- **Don't engage with same person twice** in one session
- **Spread across day if possible**: morning batch + afternoon batch

## Step 6: Update Memory Files

### engagement-log.md
Append each engagement:
```markdown
### [today's date] - Session [X]
| # | Author | Role | Post Topic | Comment Summary | Reaction | Followed | Connected |
|---|--------|------|------------|-----------------|----------|----------|-----------|
| 1 | [name] | [role] | [topic] | [first 50 chars] | [type] | [y/n] | [y/n] |
```

### contacts-network.md
Add new contacts discovered:
- Name, role, company
- Tier (1/2/3 based on goal relevance)
- Status: cold (just followed) or warm (commented, got reply)
- Platform: LinkedIn
- Last interaction: [today]

### progress-tracker.md
This engagement session counts as activity for the day.

## Step 7: Output Summary

```
Engagement Session Complete
===========================
Posts engaged: [X] / [target]
People followed: [X]
Connection requests: [X]
Reactions: [breakdown]

Engagements:
1. [Author Name] ([Role]) - [Post topic summary]
   Comment: "[first 80 chars...]"
   Reaction: [type] | Followed: [y/n]

2. [Author Name] ...
...

Reply tracking:
- Previous session replies received: [X] (check manually)
- Reply rate so far: [X]% ([X] replies from [total] comments)

Files updated: engagement-log.md, contacts-network.md, progress-tracker.md
Next: /goal:write to create content, or /goal:next for other priorities
```
