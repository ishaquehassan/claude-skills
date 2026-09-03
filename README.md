# claude-skills

My Claude Code skills, kept here so a new machine can be set up in one step
instead of copying folders around by hand.

Private on purpose. Some of these were written by other people and are here
because I use them, not because they are mine to redistribute.

## Install

```bash
git clone git@github.com:ishaquehassan/claude-skills.git /tmp/cs
mkdir -p ~/.claude/skills
cp -R /tmp/cs/skills/* ~/.claude/skills/
rm -rf /tmp/cs
```

Restart Claude Code afterwards. Skills are picked up from `~/.claude/skills`
at startup, so a running session will not see them.

## What is here

23 skills. The design ones are the reason this repo exists: `impeccable` is the
engine for writing real UI code, and the aesthetic ones (`taste-skill`,
`brutalist-skill`, `minimalist-skill`, `soft-skill`, `gpt-tasteskill`,
`stitch-skill`, `redesign-skill`, `brandkit`) are picked one at a time to suit
the brief, never stacked together.

Also here: `roast` (adversarial review council), `handoff` (session summary for
a clean context window), `output-skill` (full code, no truncation),
`review-animations` and `emil-design-eng` (motion craft), the `imagegen-*`
pair, `image-to-code-skill`, `explainer-visuals`, `banana`, `make-video`,
`whatsapp-read`, `voice-transcribe`.

## Not here

**The Flutter 3D and Three.js skills** live in their own public repo, because
they were written to be shared:

```bash
git clone https://github.com/ishaquehassan/fscene-skills.git /tmp/fs
cp -R /tmp/fs/skills/* ~/.claude/skills/
rm -rf /tmp/fs
```

That covers `fscene`, `3d-router`, `3d-crossmap` and the ten `threejs-*` skills.

**`voice-transcribe`'s model.** Only `SKILL.md` and `bin/` are committed. The
model directory is 465 MB, which has no business in a git repo. Follow the
skill's own README to fetch it, or leave it out; the rest of the skills do not
depend on it.
