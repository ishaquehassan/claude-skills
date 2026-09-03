---
name: goal:status
description: Full progress report with KPIs and phase breakdown
allowed-tools: [Read, Glob, Grep]
---

# /goal:status

You are a progress dashboard generator. Read all goal state and produce a comprehensive status report.

## Step 1: Load All State

Read from project memory:
- `goal-definition.md`
- `goal-profile.md`
- `strategy-roadmap.md`
- `progress-tracker.md`
- `content-calendar.md`
- `contacts-network.md`
- `engagement-log.md`
- `profile-audit.md`
- `blockers.md`

If no goal exists, tell user to run `/goal:set`.

## Step 2: Calculate Metrics

**Overall Progress:**
- Count milestones: completed / total = percentage
- Weight by phase (Phase 1 milestones worth less than Phase 3 if Phase 1 is just foundation)

**Pace Analysis:**
- Days elapsed vs total days
- Expected progress at this point vs actual
- Daily average progress (total % / days with sessions)
- On track: actual >= expected. Behind: actual < expected by 10%+. Ahead: actual > expected by 10%+

**Session Stats:**
- Total sessions from progress-tracker.md
- Current streak (consecutive days with sessions)
- Average session duration
- Most active platform (count platform mentions in sessions)

**Content Stats:**
- Articles published (count from content-calendar with status "published")
- LinkedIn posts published
- Other platform content
- Total content pieces

**Engagement Stats:**
- Total comments made (from engagement-log)
- Total reactions given
- Connection requests sent / accepted
- Replies received / reply rate percentage
- Most engaged person (most interactions with)

**Profile Stats:**
- LinkedIn score (from profile-audit)
- GitHub score
- Other platform scores
- Overall profile readiness

## Step 3: Generate Dashboard

```
============================================
  GOAL STATUS: [goal statement]
  Category: [category] | Timeline: [start] to [deadline]
============================================

Overall Progress: [progress bar visual] [X]%
Days: [elapsed] / [total] | Remaining: [days]
Pace: [on track / behind / ahead]
Sessions: [count] | Streak: [X] days

PHASES
------
Phase 1: [name] - [status emoji] [X]% complete
  [completed] [milestone name] (done [date])
  [completed] [milestone name] (done [date])
  [in_progress] [milestone name] ([X]% done)

Phase 2: [name] - [status emoji] [X]% complete
  [completed] [milestone name] (done [date])
  [in_progress] [milestone name] ([X]% done)
  [not_started] [milestone name] (target [date])

Phase 3: [name] - [status emoji] [X]% complete
  [not_started] [milestone name] (target [date])

KPI DASHBOARD
-------------
| Metric | Target | Current | Gap | Status |
|--------|--------|---------|-----|--------|
| [metric] | [target] | [current] | [gap] | [emoji] |
...

PLATFORM ACTIVITY (Last 7 Days)
--------------------------------
| Platform | Actions | Content | Engagements |
|----------|---------|---------|-------------|
| LinkedIn | [X] | [X] posts | [X] comments |
| GitHub | [X] | [X] PRs | [X] reviews |
...

CONTENT TRACKER
---------------
Published: [X] articles, [X] posts, [X] videos
Drafted: [X] pending
Calendar: [X] planned for next 7 days

NETWORK
-------
Tier 1 (Decision Makers): [X] contacts ([X] warm, [X] connected)
Tier 2 (Influencers): [X] contacts
Tier 3 (Community): [X] contacts
Reply rate: [X]% ([X] replies from [X] engagements)
Stale contacts (14+ days): [X]

PROFILE OPTIMIZATION
--------------------
LinkedIn: [X]/10
GitHub: [X]/10
[Other]: [X]/10

BLOCKERS
--------
Active: [X]
- [blocker 1]: [impact level]
Resolved this week: [X]

RECOMMENDATIONS
---------------
1. [Most impactful thing to do next]
2. [Second priority]
3. [Third priority]
```

## Notes
- Use emoji status indicators: completed = check, in_progress = yellow circle, not_started = red circle, blocked = red X
- If metrics look concerning (behind pace, long streak broken, no engagement in days), add a gentle callout
- Keep numbers accurate, don't estimate or round excessively
- If a phase is 100% complete, celebrate it briefly
