# Reusable Stage Patterns

Use one primary pattern per clip. Replace project-specific nouns and counts with the values from the state card.

## Fixed-Camera State Change

Use when construction changes but the viewpoint should stay fixed:

```text
Use the uploaded first frame as the exact starting state and the uploaded last frame as the exact target state.
Keep the camera, site boundary, scale, and all locked components unchanged.
Only [one action] changes, inside [bounded area], moving [direction] from [start relation] to [target relation].
Do not introduce [next-stage objects].
```

When the skill is writing a normal construction-video prompt before the frames exist, keep the endpoint logic in the prompt by default. Omit it only for an explicitly requested pure text-to-video prompt. Do not describe unseen frame details as if they were inspected.

Typical actions:

- excavation: remove the soil volume from the exposed top downward, with a fixed boundary and a flat final bottom;
- filling or casting: add the layer in its target region, with thickness and boundary controlled by the last frame;
- lowering or installation: descend from above, align to fixed references, and settle without floating;
- pumping or draining: change only the water state in place while the pump, pipe, pit, and bottom layer remain fixed.

## Camera-Only Transition

Use when the construction state is unchanged:

```text
Camera move only. Keep the same construction state, object count, geometry, materials, and lighting.
Move smoothly from [first viewpoint] to [last viewpoint].
Do not add, remove, or advance any construction operation.
```

## Ordered Appearance

When multiple objects need to appear:

```text
First, [component A] appears or stabilizes in [location].
After A is stable, [component B] appears at [target positions].
Keep all previously completed components fixed.
```

Do not use "generate A and B" when the order is part of the teaching content.

## Localized Fade or Materialization

Use when a mark, thin layer, or surface detail should appear without moving:

```text
[feature] fades in at the exact target positions already indicated by the last frame.
It is attached to [surface], changes only in opacity or local material, and does not travel, expand, trace, or redraw the site.
```

## Component Identity Lock

Use for recurring machinery or repeated components:

```text
Keep the same [component identity], count, silhouette, orientation, scale, contact point, and relative position.
Only [permitted articulation or motion] may change.
No duplicate, replacement, category change, or disappearance.
```

For a fixed construction rig, lock the whole visible assembly rather than naming
only the active tool. Include the machine body or base, mast or pile frame, guides,
cables or wire rope, actuators, hammer or attachment, cap or contact part, and the
acted-on component when those parts are visible or relevant. Only the explicitly
permitted articulation or construction action may change.

Example:

```text
Keep the entire visible pile-driving rig fixed in identity and position, including
the base, vertical pile frame, guides, wire rope, hammer, pile cap, and pile.
Only the hammer's downward impact and the pile's vertical penetration may change.
Do not duplicate, detach, bend, replace, or drift any rig component.
```

## Stage Boundary

Every clip should state both:

- what is allowed to change now;
- what belongs to a later stage and must not appear early.

Examples of forbidden early content include a foundation before reinforcement is complete, equipment before the foundation is ready, or a second excavation layer before the first layer reaches its target state.

## Description-First Action Block

Use this block when the user supplies a construction description but no frames:

```text
Show one controlled construction operation: [primary action].
The intended visible effect is [target effect].
Keep [locked objects] fixed in identity, count, silhouette, scale, and relative position.
Perform the action only inside [bounded area], moving [direction] from [initial relation] toward [target relation].
Keep the camera [fixed / specified move].
Do not introduce [later-stage or unrelated content].
Use the uploaded first and last frames as the exact endpoint references without changing the intended operation. Omit this sentence only for an explicitly requested pure text-to-video prompt.
```

Do not use a generic "construction progresses" sentence as a substitute for the action block.
