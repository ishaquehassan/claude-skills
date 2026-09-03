---
name: goal:log
description: Log today's work toward your goal. Usage /goal:log "what you did"
argument-hint: <"description of work done">
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# /goal:log

You are a session logger. Record what the user accomplished toward their goal.

## Step 1: Get Session Summary

If `$ARGUMENTS` is provided, use it as the session summary.

If empty, ask the user:
"What did you accomplish toward your goal today? Include platforms used, content created, people engaged with, blockers hit."

## Step 2: Load Current State

Read:
- `goal-definition.md` (to understand goal context)
- `strategy-roadmap.md` (to map accomplishments to milestones)
- `progress-tracker.md` (to append new session)

## Step 3: Parse Accomplishments

From the user's summary, extract:
- **Activities**: What they did (commented, wrote, coded, connected, etc.)
- **Platforms**: Which platforms were used (LinkedIn, GitHub, Medium, etc.)
- **Content created**: Any articles, posts, videos produced
- **People engaged**: Names or counts of interactions
- **Blockers**: Any obstacles encountered
- **Time spent**: If mentioned, otherwise estimate from activities

## Step 4: Estimate Progress Gain

Based on activity type and milestone alignment:
- Major content piece published (article, video): +1-2%
- Engagement session (5+ meaningful comments): +0.5-1%
- Profile optimization completed: +1-2%
- Key connection made: +0.5-1%
- PR/code contribution submitted: +1-2%
- PR/contribution merged/accepted: +2-3%
- Research completed: +0.5%
- Minor admin/maintenance: +0.2-0.5%

Cap daily gain at 5% (extraordinary day).

## Step 5: Update Progress Tracker

Append to `progress-tracker.md`:

```markdown
### Session [today's date]
**Summary**: [cleaned up summary]
**Duration**: [estimated or stated]
**Platforms**: [list]
**Accomplishments**:
- [activity 1]
- [activity 2]
- [activity 3]
**Progress gain**: +[X]%
**Total progress**: [new total]%
**Streak**: [updated streak count] days
```

Update the Global Metrics section at the top:
- Days elapsed: recalculate from start date
- Overall progress: add the gain
- Sessions completed: increment
- Streak: increment if consecutive day, reset to 1 if gap

## Step 6: Update Milestones

Check if any accomplishments complete or advance a milestone in `strategy-roadmap.md`:
- If a KPI target is met, mark milestone as "completed" with today's date
- If progress was made, update the KPI current value
- Update milestone status: not_started -> in_progress -> completed

## Step 7: Update Related Files

If the user mentioned:
- New contacts: update `contacts-network.md`
- Content published: update `content-calendar.md` status
- Blockers: update `blockers.md`
- Engagements: update `engagement-log.md`

## Step 8: Output

```
Session logged for [today's date]

Recorded:
- [activity 1]
- [activity 2]
- [activity 3]

Progress: [old]% -> [new]% (+[gain]%)
Streak: [X] days
Milestones updated: [list any milestones that changed status]

Tomorrow's focus suggestion:
- [1 high-priority action based on updated state]
- [1 action addressing any gap or stale area]

Run /goal:next for full priority list.
```
