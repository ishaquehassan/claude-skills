# Primitives toolkit — API reference

`scenes.js` exports `buildScenes(K)` and calls `K.mkGroup(g => {...})` once per scene
(in the same order as `config.scenes`). Each scene builds bespoke 3D by COMPOSING
`K.prim.*` primitives — never write raw geometry unless a primitive genuinely can't
express it. Compose different primitives / arrangements / animations per topic so
every episode looks distinct.

## The kit `K`
- `K.mkGroup(build)` — register one scene. `build(g)` runs synchronously; add meshes to `g`.
  Set `g.userData.update = (t,dt)=>{}` (per-frame, t = seconds) and `g.userData.enter = ()=>{}` (on scene start).
- `K.prim` — the primitives (below). `K.sc(i)` — scene i's config (`.blocks`, `.chips`, `.swatches`, `.code`...).
- `K.TH` — theme (`.primary .primary2 .accent .warm .ok .ink .muted .swatches[]`). `K.CFG` — full config.
- `K.tw(setter, from, to, durSec, ease, delaySec)` — tween. `K.E` — easings: `outQuart outQuint outExpo outBack outBounce`.
- `K.entrance(obj, {x,y,z}, delay, dur)` — the episode's motion-variant entrance (auto-varies per episode).
- `K.cam` — the THREE camera (move it in `update` for cinematic shots; it resets each scene).
- `K.labelPlaneH(text, worldHeight, {color,weight,size,mono})` / `K.setLabelH(mesh,text,h,opts)` — 3D text.
- Also available: `K.THREE`, `K.RoundedBoxGeometry`, `K.TX_CYAN/GOLD/WHITE` (sprite textures), `K.mkScreen`, `K.M_ALU`, `K.slab`.

## Primitives `P = K.prim`
- `P.node(colorHex, r=.42)` → `{group, core, spin(dt,s), pulse(t,amp), glow(v), decay(dt,floor,rate), setColor(c)}`
  A glowing sphere. Use for concepts/services/entities. Add `.group` to the scene.
- `P.edge(vA, vB, colorHex)` → `{group, pulseAt(p01)}` — glowing line between two points; `pulseAt(p)` moves a pulse (0→1) for data flow.
- `P.stream(colorHex, {count, spread, inward})` → `{group, update(t, speed)}` — particle river out/into center.
- `P.stack([{label,color?}], )` → `{group, update(t), enter()}` — glossy LEGO-like labelled blocks (composition/layers).
- `P.codePanel({file, lines})` → `{mesh, redraw(rows, reload)}` — code editor panel. `lines`/rows = `[[{t,c,chip?}]]` (segments per line; `chip` draws a color swatch).
- `P.deviceRow(['phone','web','desktop'])` → `{group, recolor(hex), enter()}` — device mockups with recolorable screens.
- `P.ring(colorHex, r, arc)` → `{mesh, update(dt,s)}` — spinning arc (loaders/orbits).
- `P.morph([{col,label,val,spin?}])` → `{group, set(i), next(), update(t,dt)}` — a node cycling states (loading/data/error, on/off).
- `P.tree(colorHex, {levels, spread})` → `{group, update(t), enter()}` — branching tree (git branches, dep trees).
- `P.burst(colorsHex[])` → `{group, update(t,dt), enter()}` — celebratory confetti (outro).
- `P.label(text, {h,color,x,y,z,mono,weight})` — quick 3D text plane.
- `P.pop(obj, {x,y,z}, delay, dur)` — entrance shortcut (= `K.entrance`). `P.V(x,y,z)` — a THREE.Vector3.

## Composition tips
- Coordinates: camera looks down -Z; visible area roughly x∈[-2.3,2.3], y∈[-2.5,2.5] at z=0. Keep content y∈[-1.2, 1.4] (title is top ~13%, caption bottom ~24%).
- Give each scene a clear focal object + motion. Use `P.edge` pulses / `P.stream` for "flow", `P.node` graphs for "relationships", `P.stack` for "layers/parts", `P.morph` for "states", `P.tree` for "branching", `P.deviceRow`+`P.codePanel` for "code → output".
- Reuse `K.sc(i).blocks`/`.chips` labels for on-object text so 3D matches the script.
- Vary metaphors by topic: e.g. Kubernetes → pods (nodes) orbiting a control-plane node; Git → `P.tree`; Redis → grid of `P.node` cells; GraphQL → a schema graph with `P.edge`; Kafka → `P.stream` between broker nodes.

## Full example
See `engine/examples/scenes.riverpod.js` (a complete 6-scene bespoke Riverpod video composed from these primitives). Imitate its structure; invent NEW arrangements for the new topic.
