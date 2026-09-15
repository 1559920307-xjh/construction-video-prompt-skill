# Failure Repair

Repair the smallest observable cause first. A negative prompt is a constraint supplement, not a substitute for incorrect frames, masks, or workflow settings.

| Visible failure | Positive repair | Targeted negative terms | Recheck |
|---|---|---|---|
| Camera rotates during an action | `fixed camera; only the specified component moves` | `camera orbit, camera pan, camera rotation, changing viewpoint` | First/last composition |
| Excavation grows upward | `remove the exposed volume from the top surface downward` | `raised platform, ground rising, object growing upward` | Boundary and final depth |
| Pit or site boundary drifts | `keep the complete boundary fixed throughout` | `boundary drift, shrinking frame, expanding frame, cropped corner` | Four corners and scale |
| Surface layer turns the whole image white | `only the local target layer changes color and thickness` | `global white flash, whole pit turning white, exposure jump` | Locality and lighting |
| Liquid or material sweeps like a wipe | `appear or recede in place with a stable local boundary` | `wipe transition, progress-bar sweep, side-to-side sheet` | Direction and edge shape |
| Reinforcement becomes tangled | `sparse regular aligned grid, one stable plane` | `dense lines, tangled cluster, vines, random particles` | Count, spacing, plane |
| A component becomes dots | `short vertical cylinders or another explicit 3D form, thicker than the surrounding lines` | `dot-like component, random black dots, stains` | Shape and count |
| Wrong machine category appears | `same named machine identity, silhouette, and permitted parts` | `replacement category, unrelated machine, duplicate machine` | Identity and position |
| Equipment floats or passes through structure | `descend, align, contact the target surface, and remain stable` | `floating, passing through, detached shadow` | Contact point and shadow |
| Next-stage objects appear early | Remove triggering words from the positive prompt and state the current stage boundary | `next-stage object too early, completed later structure` | Stage-only content |
| A bridge frame differs between clips | `reuse the exact previous end frame as the next start frame` | `independent bridge redraw, changed bridge identity` | Prefer exact file-byte or cryptographic-hash equality; if files differ by encoding, compare decoded pixels after matching dimensions, crop, color space, and alignment, then inspect visually |

## Repair Order

1. Confirm that the first and last frames represent the intended states.
2. For a suspected cross-clip mismatch, verify the bridge-frame relationship before changing the prompt. If the files are not available, mark the equality as unverified rather than assuming that the filenames identify the same frame.
3. Confirm that the action is physically and spatially described.
4. Add one or two targeted positive constraints.
5. Add targeted negatives for the observed failure.
6. Reduce duration or camera motion if the task is underconstrained.
7. If the same failure survives, change the input mask, structural reference, or workflow branch before adding more prose.

Do not claim that a negative term "fixed" a result unless a new output was actually inspected.
