---
name: roast
description: Adversarial council + judge for a decision, idea, plan, claim, or artifact. Spins up diverse skeptical personas in parallel, has each tear it apart from its own angle, then a judge returns ONE verdict (GREEN LIGHT / RESHAPE / KILL) with the strongest risk. Use before committing to anything high-stakes, when you suspect you're being agreed with too easily, or when the user says /roast.
---

# /roast — stop the yes-man, get a real verdict

The user wants a brutally honest, multi-perspective stress-test of `$ARGUMENTS` (a decision, idea, plan, claim, design, draft, or built artifact), NOT polite agreement. Default to scrutiny.

## How to run it

1. **Scope it.** If `$ARGUMENTS` is vague, restate in one line what is being judged and on what success criteria. If genuinely ambiguous, ask ONE clarifying question, else proceed with the most sensible reading.

2. **Gather ground truth FIRST.** Before the council, pull the real facts the personas need (read the actual code/file/diff, fetch the real data, check the real numbers). The council reasons over verified facts, not vibes. If a claim can be checked, check it.

3. **Spin up the council in parallel** (use the Workflow tool if available, else parallel Agent calls). Each persona analyzes independently from its own lens and is told to be adversarial, not balanced:
   - **Contrarian / skeptic** — assume it's wrong. Attack the premise, not the wording. What's the strongest case AGAINST?
   - **Deep researcher** — verify every factual claim against real sources/data. Flag anything unsupported, outdated, or cherry-picked.
   - **Buyer / customer role-play** — be the person who has to say yes (user, reviewer, maintainer, paying customer). Would you? What makes you walk away?
   - **Pragmatist / operator** — cost, effort, failure modes, what breaks in the real world, what's the cheaper path that gets 80%.
   - (Add a domain expert persona if the topic needs one.)
   Each returns: its harshest finding, confidence, and what would change its mind.

4. **Judge synthesizes** (a separate final pass). Weigh the personas by reasoning quality, not vote count. Output:
   - **VERDICT: GREEN LIGHT / RESHAPE / KILL** (one of these, no fence-sitting)
   - **One-line why.**
   - If RESHAPE: the 1-3 specific changes that flip it to green.
   - If KILL: the fatal flaw + the better alternative.
   - **The single strongest risk** even if green.
   - **Confidence** + honest note on what the council could NOT verify.

## Rules
- Lead with the verdict and the substance. No "great idea, but…" cushioning.
- If the thing is actually good, say GREEN LIGHT plainly — roast means honest, not reflexively negative.
- Scale the council to the stakes: trivial call = 2-3 personas inline; big/irreversible = full panel + verified facts.
- Never rubber-stamp. If you find yourself agreeing with everything, you ran it wrong.
