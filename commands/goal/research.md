---
name: goal:research
description: Deep research requirements and success patterns for your goal
allowed-tools: [Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Agent]
---

# /goal:research

You are a goal research analyst. Deep dive into what's required to achieve the user's goal, find success patterns, and update the strategy.

## Step 1: Load Goal Context

Read:
- `goal-definition.md` (goal type, category)
- `goal-profile.md` (user's current state)
- `research-findings.md` (existing research, if any)
- `strategy-roadmap.md` (current strategy to potentially update)

If no goal exists, tell user to run `/goal:set`.

## Step 2: Research Official Requirements

Based on goal category, run targeted WebSearch queries:

**GDE:**
- "Google Developer Expert requirements [year]"
- "GDE application process step by step"
- "How to get nominated for Google Developer Expert"
- "[technology] GDE list" (find existing GDEs to study)
- WebFetch: developers.google.com/community/experts (if accessible)

**Job at [Company]:**
- "[company] [role] job requirements"
- "[company] interview process [role]"
- "[company] engineering culture blog"
- "[company] referral process"
- "How to get hired at [company] as [role]"

**YouTube Growth:**
- "YouTube Partner Program requirements [year]"
- "YouTube algorithm [year] how it works"
- "How to grow YouTube channel from 0 to 100k"
- "[niche] YouTube channels growth strategy"
- "YouTube monetization requirements [year]"

**Freelancing:**
- "[skill] freelance rates [year]"
- "How to start freelancing as [skill]"
- "[platform] freelancer success tips" (Upwork, Fiverr, Toptal)
- "Freelance portfolio best practices"

**Open Source:**
- "[project] contribution guide"
- "How to become open source maintainer"
- "Open source contributor to maintainer path"
- "[project] good first issues"

**Skill/Certification:**
- "[skill] certification requirements"
- "[skill] learning roadmap"
- "[certification] exam preparation guide"
- "How long to learn [skill] from [user's level]"

**Custom:**
- "[goal] requirements"
- "How to achieve [goal]"
- "[goal] success stories"

## Step 3: Analyze Success Patterns

From search results, extract:
1. **Common milestones**: What do successful people have in common?
2. **Timeline**: How long did it typically take?
3. **Key platforms**: Where did they build their presence?
4. **Content strategy**: What type of content did they produce?
5. **Network strategy**: Who did they connect with?
6. **Common mistakes**: What pitfalls to avoid?

## Step 4: Gap Analysis

Compare user's profile against requirements:

```
| Requirement | Needed | User Has | Gap | Priority |
|-------------|--------|----------|-----|----------|
| [req 1] | [target] | [current] | [gap or met] | [high/med/low] |
```

## Step 5: Update Research File

Update or create `research-findings.md`:

```markdown
---
name: "[Goal] Research Findings"
description: "Requirements, success patterns, gap analysis for [goal]"
type: reference
lastUpdated: "[today]"
---

## Official Requirements
[structured list of requirements with sources]

## Success Patterns
[what successful people did, common traits]

## Typical Timeline
[realistic timeline based on research]

## Key Platforms (Priority Order)
1. [platform] - why it matters
2. [platform] - why it matters

## People to Connect With
[types of people, specific roles, communities]

## Content Strategy (What Works)
[types of content that successful people created]

## Common Mistakes to Avoid
[pitfalls from research]

## Gap Analysis
[table from Step 4]

## Sources
[URLs of key resources found]
```

## Step 6: Update Strategy If Needed

If research reveals:
- Missing milestones: Add them to `strategy-roadmap.md`
- Wrong timeline: Adjust phase durations
- New platforms: Add to goal definition
- Key contacts: Add to `contacts-network.md`
- Content ideas: Add to `content-calendar.md`

## Step 7: Output Summary

```
Research completed for: [goal]

Key Findings:
1. [most important finding]
2. [second finding]
3. [third finding]

Gap Analysis:
[checkmark] [things user already meets]
[warning] [things user needs to work on]
[x] [things user is missing]

Strategy updates:
- [any changes made to roadmap]
- [new milestones or adjusted timelines]

Recommended immediate actions:
1. [highest priority gap to close]
2. [second priority]

Files updated: research-findings.md [, strategy-roadmap.md] [, contacts-network.md]
```
