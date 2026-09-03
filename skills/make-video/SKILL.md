---
name: make-video
description: >-
  Generate a bespoke 3D 4K vertical (9:16) explainer video for any tech/topic —
  each episode gets its OWN theme, mascot, 3D objects, animations, explaining
  style and ending, composed from a tested primitives toolkit. Use when the user
  says "make a video about X", "/make-video X", "explainer video for X", or wants
  a new episode for their video course. Produces a ready-to-post 4K MP4.
argument-hint: "<topic>  (e.g. Kubernetes, GraphQL, Rust, Redis)"
---

# make-video — bespoke 3D explainer generator

Turn a topic into a unique, on-brand, 4K 9:16 explainer video. Every episode
looks DIFFERENT (its own colors, mascot, 3D metaphors, motion, ending) because
you design the scenes per topic and COMPOSE them from a tested primitives
toolkit (so they render reliably).

**Engine:** `~/Desktop/personal/tech-explainer/engine`  (`E` below). Work from the repo root `~/Desktop/personal/tech-explainer`.

## Before anything
1. Read `E/reference` note here: **read `~/.claude/skills/make-video/reference/primitives-api.md`** (the toolkit API) and **`E/examples/scenes.riverpod.js`** (a full worked example). You compose these primitives — do not hand-write raw Three.js.
2. Voice needs a key: ensure `CARTESIA_API_KEY` is exported (or `ELEVEN_API_KEY`). If neither is set, ask the user for it before the render step (steps 1–4 don't need it).

## Flow (topic → video)
Let `TOPIC` = the argument, `SLUG` = kebab-case + `-what-is` (e.g. `kubernetes-what-is`), `EP = episodes/$SLUG`.

> **AESTHETIC = CLEAN LIGHT** (locked). Every video is a bright, airy, Apple/Linear-tier design on a light background — NOT a dark "space" theme. Light paper bg, dark bold type, the topic's brand color as accent, real soft shadows under solid 3D objects, no starfields/glow-orbs. The engine handles the light bg/text automatically; you only supply the brand accent colors + readable content.

### 1. Design (research + art direction)
Research the topic's real concepts + brand. Decide:
- **Theme** — supply the topic's brand palette for ACCENTS only (the engine forces a light bg + dark text): `primary` = its recognisable brand color; `primary2` lighter; `primary3` darker (used for the title gradient + accents — make sure it reads on white); `accent` complementary; `swatches` = 4 vivid colors for 3D objects/blocks; `aura1/aura2` = translucent brand rgba (subtle top-glow tint on the light bg, alpha .06–.14). `bg0/bg1/bg2/ink/muted` are ignored now (light is automatic) but harmless to include.
- **Mascot / logo** — ALWAYS prefer the topic's REAL brand logo: set `mascot.logo` to the topic's [devicon](https://devicon.dev) slug (e.g. `dart, flutter, docker, react, python, go, rust, kubernetes, redis, nodejs, typescript, graphql, postgresql`). The build auto-downloads the official full-color SVG from devicon and shows it as the mascot. Also set `mascot.type` (from `bird, atom, snake, gopher, cube, spark, whale, gear, crab, hexagon`) + `colors {a,b,c,d}` as a fallback for topics with no devicon logo. Verify the logo actually renders in the s0/s5 frames; if the slug 404s, drop `logo` and rely on the drawn mascot.
- **6 scene beats** (the script) — one short spoken `line` each, plus `kicker` + two-part `title:[normal,highlight]`. Beats are usually: intro · where-it-runs/surfaces · core-parts · fast-iteration/how-it-works · a contrast (light-vs-deep / before-vs-after) · outro+CTA. Adapt wording to the topic; keep facts correct.

Write `EP/config.json`:
```json
{ "slug":"$SLUG",
  "meta":{"series":"Ishaq Explains","episode":"Ep 01 · What is $TOPIC?","title":"What is $TOPIC?","narrator":"Ishaq"},
  "theme":{ ...full palette... },
  "mascot":{"logo":"<devicon-slug>","type":"<fallback>","colors":{"a":"#..","b":"#..","c":"#..","d":"#.."}},
  "voice":{"provider":"cartesia","voiceId":"630ed21c-2c5c-41cf-9d82-10a7fd668370","model":"sonic-2"},
  "bgm":true,
  "scenes":[ {"type":"intro","line":"..","title":["Meet ","$TOPIC"],"lede":".."},
             {"type":"chips","line":"..","kicker":"..","title":["..",".."],"chips":["","","",""]},
             {"type":"stack","line":"..","kicker":"..","title":["..",".."],"blocks":[{"label":".."},{"label":".."},{"label":".."},{"label":".."}]},
             {"type":"flow","line":"..","kicker":"..","title":["..",".."]},
             {"type":"contrast","line":"..","kicker":"..","title":["..",".."]},
             {"type":"outro","line":"..","title":["Build something ",".."],"cta":"Try it at ...→"} ] }
```
(scene `type` is just a hint; the Nth scene in `scenes.js` renders regardless. Include `blocks`/`chips` labels you'll show on 3D objects.)

### 2. Bespoke scenes — FLAT 2D (no 3D)
The visuals are **flat 2D DOM/SVG** (Apple-keynote minimal), NOT 3D. The WebGL canvas is hidden. Write `EP/scenes.js`:
```js
export function buildScenes(K){
  const TH=K.TH, PRI=TH.primary, ACC=TH.accent, SW=TH.swatches, INK='#0d1526', MUT='#5b6b82';
  for(let i=0;i<6;i++) K.mkGroup(()=>{});          // harness needs 6 (empty) scene groups
  const vis=(i)=>{const s=document.querySelector('[data-scene="'+i+'"]');const v=document.createElement('div');v.className='vis';s.appendChild(v);return v;};
  vis(1).innerHTML = `... flat SVG/HTML ...`;        // build a distinct flat illustration per scene (1..4)
}
```
- Scene 0 (intro) and 5 (outro) already show the real logo — leave them (optionally add flat confetti to 5). Build flat visuals for the CONTENT scenes (1–4).
- **Ready CSS classes** (use these, already styled for the light theme): `.f-chip` (pill with a `.ic` colored square), `.f-row` (wrapping row of chips), `.f-card` (row card with a `.dot`), `.f-stack` (staggered-reveal column of `.f-card`s), `.f-codecard` (dark code card with a `.bar` of dots), `.f-metric` (big mono number). Colored progress bars: a track `div` + inner `div` with a width %.
- Pick a fitting flat metaphor per beat: connector diagram (chip + SVG lines + chips) for "runs on X"; `.f-stack` of cards for parts/features; `.f-codecard` + `→` + chips for code→output; two labelled progress bars for a speed/before-after compare.
- **Readability:** labels/text dark (`#0d1526` / `#5b6b82`); deepen pale swatch colors for dots/fills (see `deep()` in the example). Everything flat — soft shadows only, no gradients-as-fills, no glow.
- Keep it inside the middle band (below the title, above the caption). See `episodes/dart-what-is/scenes.js` for a complete worked example — imitate its structure, invent fresh flat visuals for the new topic.

### 3. Verify (self-check — do NOT skip)
```
cd ~/Desktop/personal/tech-explainer
python3 engine/verify.py episodes/$SLUG
```
It prints `ERRORS:...` and writes `episodes/$SLUG/.build/verify/s0.png … s5.png`. **Read every frame.** If `ERRORS` is not `none`, or any scene is empty / broken / text unreadable / objects off-screen or overlapping the caption → fix `scenes.js` and re-run. Loop until all scenes look clean and distinct.

### 4. Render
```
cd ~/Desktop/personal/tech-explainer
export CARTESIA_API_KEY=...            # if not already set
python3 engine/build.py episodes/$SLUG
```
~7–8 min. Output: `episodes/$SLUG/$SLUG-4k.mp4` (2160×3840, voice + music). Grab a couple frames with ffmpeg to confirm, then `open episodes/$SLUG/` and report the path.

## Rules
- Facts must be correct for the topic; labels (`blocks`, `chips`) are real concepts.
- Never reuse another episode's exact scene set — design fresh metaphors each time.
- Prefer composing primitives; only drop to raw `K.THREE` for something the toolkit can't express, and keep it in the safe area.
- Always run verify (step 3) before the expensive render (step 4).
