---
description: Run any change through the mandatory verify-before-and-after workflow (pre-verify → implement → post-verify → PR → merge-verify → housekeeping)
argument-hint: [what you're about to change]
---

# 🚦 Standard Workflow — Verify Before & After

You are about to work on: **$ARGUMENTS**

Follow this workflow for **every** change, no matter how small — a typo fix and a new feature use the same phases; only the time per phase differs.

> **Golden rule:** _"It's a tiny change, no need to verify"_ is the exact thought that causes outages. The time spent verifying is always less than the time spent recovering from a missed edge case.

---

## The Pipeline (end to end)

```
deep-analysis → plan → issue → pull latest → WORKTREE → build
   → verify+test → PR → merge (confirm first) → deploy-retest → report → clean worktree
```

Work in an **isolated git worktree** per task (e.g. `../<repo>-<feature>`), not the main working dir — keeps main clean and lets parallel work not collide. Remove the worktree when done.

---

## Phase 1 — Pre-Verify (before touching any code)

**Goal:** 100% understand what changes and what it touches.

- [ ] Read the issue/request fully + relevant docs
- [ ] Run the affected flow and observe current behavior
- [ ] Identify the exact file(s) and function(s) that will change
- [ ] Grep for all callers/consumers of what you're changing
- [ ] List edge cases the change must handle
- [ ] List negative impacts — what could break
- [ ] Check existing tests for the code you'll touch
- [ ] Note new env vars / migrations / feature flags needed

**If touching data, schema, or shared state (mandatory):**
- [ ] Migration safe for existing rows? (widen col = safe; narrow / NOT NULL without default / type change = review)
- [ ] What do existing rows look like today — does the new code handle legacy/empty values?
- [ ] Read path stays backwards-compatible (response shape, IDs, enums unchanged)?
- [ ] Write path forward-only, or is a backfill needed? Decide: in-PR script / follow-up / accept gap
- [ ] Rollback leaves existing rows in a safe state?

**Then hand off to the user before coding:**
- What you plan to change (exact files) + why
- What could go wrong (edge cases, risks) + alternatives considered
- **A complexity + effort estimate (Low / Medium / High).**
- 🚫 **Wait for explicit confirmation. Do NOT start coding until confirmed.**

You're done with Phase 1 when you can answer without guessing: why does this change exist, which files change, what behavior changes, 3 edge cases, what could break, and how you'll prove it works.

---

## Phase 2 — Implement

- Smallest, cleanest change that does exactly what Phase 1 approved
- **Atomic commits** — one logical change each; conventional prefixes (`feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`)
- Commit body explains the **why**, not the what
- No scope creep, no new abstractions "just in case", no unrelated refactors
- Keep PRs small (< ~400 lines diff preferred; split larger work)

**Don't:** skip hooks (`--no-verify`), force-push shared branches, or change behavior not covered by the request.

**When adding a DB migration:** check the latest migration number/timestamp first and pick one strictly greater (parallel work collides on the same number otherwise). Never renumber a migration that has already been deployed.

---

## Phase 3 — Post-Verify (before opening the PR)

- [ ] Tests pass — **and critically, your change adds no NEW failures vs the baseline** (many repos have a non-green baseline; the honest bar is "+0 regressions", not "everything green")
- [ ] Lint + format clean
- [ ] Build / type-check clean
- [ ] Manual smoke — actually run the feature, don't just trust the tests
- [ ] **END-TO-END BROWSER TEST (mandatory for any user-facing / UI change): drive the real deployed flow yourself in the Chrome extension.** Do not stop at "code is deployed / bundle contains it" — open the actual page in the browser (per the global rules: the pre-set extension — Brave, `isLocal:true`, auto-select it, never a remote browser), perform the real user steps, and confirm with a screenshot that the behavior is correct. Passing tests + a green deploy are NOT a substitute for watching the feature work in a browser. If you genuinely cannot drive it (no browser access), say so explicitly and hand the exact steps to the user.
- [ ] Re-read your own diff top to bottom — would you approve it as a reviewer?
- [ ] Adjacent features still work (not just your happy path)
- [ ] No stray `console.log` / `TODO` / dead code / secrets / localhost URLs
- [ ] Docs updated if behavior or API shape changed
- [ ] If migration: runs + reverts cleanly, and legacy-row read path tested

**Enforce these checks in CI, not just locally.** A manual "I ran the tests" is honor-system and eventually gets skipped under pressure. A required CI check on every PR is what actually prevents red code from merging — wire the Phase 3 checks (test/lint/build) into a pipeline that gates the merge.

---

## Phase 4 — Pull Request

Target the correct base branch. PR title uses a conventional prefix. Description template:

```markdown
## Summary
<1-3 bullets: what + why>

## Context
<links to issue, docs, related PRs>

## Changes
<significant changes>

## Test plan
- [ ] <what you actually did to verify>
- [ ] <edge cases tested>
- [ ] <regression checks>

## Risks
<low / medium / high — explain; name the backwards-compat story explicitly>

## Rollback plan
<how to revert if it breaks>
```

**Self-review first** — read your own PR from a reviewer's angle before requesting review. Draft PR if anything is uncertain.

---

## Phase 5 — Merge-Verify (post-merge, before you walk away)

The moment the change is merged, confirm it's actually live and working — don't assume the deploy succeeded.

- [ ] Watch the deployment/rollout reach a completed state (running == desired)
- [ ] Confirm the new build/revision is the one actually running
- [ ] Hit the health/readiness endpoint (know which probe is authoritative — a noisy sub-check can 503 while the service is fine; verify against the probe the load balancer actually uses)
- [ ] Smoke the new endpoint(s)/feature from this change — happy path + 1-2 edge cases
- [ ] Tail recent logs for boot errors or stack traces tied to your change

**On failure:** don't mark it done. Capture the failure mode, find root cause, open a **separate** fix PR, re-run Phase 5.

Even a docs-only change gets a minimum "it loads, no errors" check. If a change genuinely has no deploy surface, say so explicitly and confirm it landed on the right branch.

---

## Phase 6 — Housekeeping + Close

- [ ] Save a memory/note only for a genuine **surprise or non-obvious gotcha** (not routine changes — version control already records those)
- [ ] **Prune your notes/memory index** — keep entries short (one line, pointer to detail). An overgrown index stops loading fully and you lose the context it was meant to preserve
- [ ] Remove the worktree
- [ ] Final one-line summary + PR link

---

## Escalate / Ask Before Acting

Always confirm before: destructive DB ops (DROP/TRUNCATE/DELETE without WHERE), touching production infra, force-pushing shared branches, running migrations on shared environments, rotating secrets, or anything hard to reverse.

## When Something Unexpected Happens Mid-Task

**Stop. Don't fight through it.** Note what you expected vs what happened, tell the user, and ask how to proceed. Triggers: tests you didn't write start failing, linter complains about untouched code, `git status` shows files you didn't edit, unfamiliar branch/HEAD, lock files changed.
