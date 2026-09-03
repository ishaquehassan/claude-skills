---
name: handoff
description: Write a complete session handoff summary so the user can /clear (or start a fresh session) and paste it back with zero lost progress. Captures state, decisions, what's done+verified vs pending, and the exact next step. Use when the context is getting long/degraded, before a /clear, or when the user says /handoff.
---

# /handoff — clean context window, zero lost progress

Models degrade well before the context window is full. The user wants a tight, paste-back summary so they can clear and resume on a clean window. Write the handoff as a single self-contained block the user can paste into a fresh session.

## Produce exactly this (fill from the real session, no fluff)

**HANDOFF — <one-line what this session is about>**

1. **Goal / definition of done** — what we're trying to achieve and how we'll know it's finished.
2. **Current state** — where things actually stand right now (be precise: branch, version, what's deployed/running).
3. **Done + VERIFIED** — what's complete AND how it was proven (test/screenshot/curl/logcat). Mark anything "done but unverified" separately.
4. **In progress / pending** — what's half-done, the exact next step, and any blockers.
5. **Key facts to carry** — file paths, function/symbol names, IDs (PR#, commit, doc id), commands, credentials-location (not the secret), URLs, gotchas discovered.
6. **Decisions made (and why)** — so the fresh session doesn't relitigate them.
7. **Open questions / risks** — anything unresolved or that could bite.
8. **First action on resume** — the single concrete thing to do next.

## Rules
- Pull from what ACTUALLY happened this session, not a generic template. Quote real paths/IDs/commands.
- Be honest about what's unverified or uncertain (don't claim "done" for things not tested).
- Keep it dense but complete: enough that a fresh session needs zero re-discovery.
- After writing it, remind the user they can /clear and paste this block to continue.
- If this project keeps a memory file, also offer to persist the durable parts there.
