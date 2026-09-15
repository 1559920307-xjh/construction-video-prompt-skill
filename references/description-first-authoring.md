# Description-First Authoring

This is the default mode for ordinary prompt requests.

## Input Contract

The user may provide only a natural-language description. Extract the following facts when available:

- construction stage or operation;
- one primary action;
- intended visual effect;
- objects that must remain fixed;
- camera behavior;
- action direction and bounded area;
- appearance or operation order;
- content that belongs to a later stage and must not appear early;
- target model or platform, if known;
- optional duration, aspect ratio, resolution, or fps;
- optional observed failure from an earlier result.

First and last frames are not required inputs to the skill. They are usually uploaded later to the video model as downstream visual conditions. Never claim to have inspected a frame that was not supplied.

## Default Assumptions

Use these assumptions only when the description does not contradict them:

- If the construction state changes and no camera move is requested, use a fixed camera.
- If the user names a machine or component, preserve its identity, count, silhouette, scale, and contact relationships unless a change is explicitly requested.
- If the user describes one operation, keep the clip centered on that operation.
- If the user does not provide exact counts, dimensions, model IDs, or settings, do not invent them.
- Keep labels, arrows, subtitles, and watermarks out of the generated video when they can be added in post-production.

State only material assumptions in a short note after the prompts. Do not invent missing engineering facts.

## Default Output

For a description-first request, return the following sections in this order:

1. **Copy-ready English prompt**
2. **English negative prompt**
3. **Chinese review prompt**
4. **Chinese negative prompt**
5. **Assumptions or adapter note**, only when needed

Use endpoint wording in the positive prompt by default for a construction-video request:

```text
Use the uploaded first frame as the exact starting state and the uploaded last frame as the exact target state.
Only the described construction action may change between the two endpoint states.
```

Omit that wording only when the user explicitly asks for a pure text-to-video prompt or says that no first/last-frame workflow will be used. Do not ask the user to upload frames to this skill merely to draft the prompt.

## When to Ask a Question

Do not block prompt generation merely because frames are absent. Ask at most one focused question only when two plausible interpretations would produce materially different prompts, such as:

- hammer strike versus camera-only inspection;
- pile sinking versus hammer lifting;
- fixed camera versus a deliberate pullback;
- one pile versus a multi-pile sequence.

Otherwise, make the narrowest reasonable assumption, state it, and produce the prompt.

## Endpoint Wording

For the default construction-video workflow, put the endpoint relationship directly inside the positive prompt:

- the first uploaded frame is the exact starting state;
- the last uploaded frame is the exact target state;
- the camera, site boundary, recurring machinery, component identity, scale, and other fixed references remain consistent;
- only the named construction action and its direct visible consequence may change;
- later-stage objects, unrelated machinery, workers, labels, or unrequested effects must not appear early.

If the user explicitly requests pure text-to-video, omit the endpoint wording but retain the construction constraints. Do not expose these points as a separate alignment report during ordinary prompt writing unless the user explicitly asks for an explanation. Do not invent visual details for frames that were not supplied.

## Example: Hammer-Driven Pile

User description:

```text
Single precast-pile hammer driving. Keep the camera fixed, and keep the pile frame,
hammer, wire rope, pile cap, and site unchanged.
The hammer drops to strike the pile cap while the precast pile gradually penetrates
vertically. The video must clearly show both the hammer impacts and the pile sinking.
Do not show workers, extra piles, text, or a completed group-pile state.
```

The skill should produce a prompt that locks the rig and site, makes the hammer impact and vertical pile penetration the only primary action, and uses the later-uploaded first/last frames as endpoint references. It should not invent the number of piles, exact penetration percentage, model, seed, duration, or resolution.

## Example: Excavation

User description:

```text
Show the first excavation layer of a foundation pit from a fixed camera. Keep the
retaining wall and excavator unchanged. Remove only the exposed soil inside the
pit, decreasing the soil volume from the top downward. Do not introduce second-layer
supports, the basement slab, workers, or subtitles early.
```

The skill should describe downward removal inside the bounded pit, lock the wall and excavator, forbid later-stage structures, and tell the user what the initial and target frames should contain.
