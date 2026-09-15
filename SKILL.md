---
name: construction-video-prompt-engineering
description: Generate copy-ready English and Chinese positive/negative prompts for engineering video clips after identifying the clip type and requested output frame size. First/last frame files are optional and are normally supplied later to the video model; use this skill for construction actions, viewpoint transitions, static showcases, stage boundaries, object continuity, camera stability, action direction, and repair of observed failures. Do not use for generic cinematic prompts, frame creation, video generation, or full video editing.
metadata:
  version: "0.1"
  scope: "description-first-prompt-authoring"
---

# Construction Video Prompt Engineering

## Purpose

Turn a user's description of one engineering video clip into copy-ready prompt text. The normal input is text only: the user identifies the clip type, gives the requested output frame size, describes the construction stage or subject, and explains the action or viewing effect they want. By default, write the prompt so the user can later upload corresponding first and last frames to the target video model. Missing frame files are never a prerequisite for ordinary prompt generation.

For ordinary prompt generation, `clip_type` and `frame_size` are required inputs. The supported clip types are:

- `construction_action`: the construction state changes because of one visible construction operation.
- `viewpoint_transition`: the camera or viewpoint changes while the construction state remains unchanged.
- `static_showcase`: the subject is presented from a stable view without a construction-state change or deliberate camera move.

This v0.1 release covers description-first prompt authoring and focused failure repair. Frame-aware refinement, historical case reconstruction, and QA are optional modes used only when the relevant materials are supplied or explicitly requested. The skill writes instructions; it does not create frames, generate video, execute a paid cloud job, inspect an unattached media file, certify engineering compliance, or guarantee a model result.

## Use This Skill When

- A user needs an engineering or construction video prompt from a natural-language description, BIM, Blender, Revit, storyboard, or supplied reference frames.
- A user describes one construction stage, viewpoint transition, or static showcase and the intended visual effect, but has not prepared the frames yet.
- A short image-to-video clip must preserve a camera, site boundary, component identity, or construction stage.
- A generated clip has geometry drift, an incorrect action direction, premature next-stage objects, unstable camera motion, or wrong component count.
- A historical generation needs to be audited or reconstructed as a case.

Do not use it for a generic cinematic prompt with no engineering state or continuity constraint. If the request is outside construction-process video prompting, do not generate the unrelated prompt under this skill; briefly state that the skill is out of scope and ask for a construction stage, construction action, or continuity constraint. Do not infer a model, parameter, frame content, or result from a filename alone.

## Default Input

Accept ordinary language. Do not require the user to fill a rigid schema or upload files. For ordinary prompt generation, the user must explicitly provide the clip type and exact output frame size. The minimum useful description is:

```text
Clip type: construction_action | viewpoint_transition | static_showcase
Output frame size: width x height in pixels, optionally with aspect ratio
Construction stage or current state:
One primary action, viewpoint change, or showcase intention in this clip:
Visible effect that should be clear:
Objects that must remain unchanged:
Camera requirements:
Action area and direction:
Forbidden content:
```

If `clip_type` or `frame_size` is missing, ask the user to provide the missing field or fields before writing prompts. Do not infer the clip type or invent the output size. The user may provide the remaining information as a paragraph. Platform, model, duration, fps, masks, and observed failures are optional. First/last frame files, workflow JSON, seed, and case-manifest fields are not required for this mode.

## Default Output

For an ordinary prompt request, return prompt text first and keep the response compact:

1. **English positive prompt** ready to paste into a compatible video workflow.
2. **English negative prompt** containing only relevant failure constraints.
3. **Chinese positive prompt** with the same engineering meaning for direct comparison.
4. **Chinese negative prompt** with the same engineering constraints for direct comparison.
5. **One short assumption or adapter note** only when an unstated choice materially affects the prompt.

The positive prompts must explicitly include the declared clip type in natural language and the exact requested `frame_size`. The actual pixel dimensions must also be configured in the target video workflow; mentioning the size in a prompt does not override workflow settings.

Every positive prompt must also include explicit quality language. Use
`high quality, clear imagery, realistic visual appearance` in the English
positive prompt. The Chinese positive prompt must express the same three
concepts using their direct Chinese equivalents: high quality, clear imagery,
and realistic visual appearance. Keep this quality language subordinate to the
engineering action and continuity constraints; it must not replace concrete
descriptions of the scene or motion.

For ordinary engineering-video prompts, include the endpoint instruction directly in the positive prompt by default. For `construction_action`, the uploaded first frame is the exact starting state, the uploaded last frame is the exact target state, and only the described construction action may change between them. For `viewpoint_transition`, only the camera or viewpoint may change between the endpoint states. For `static_showcase`, the construction state and camera remain stable between the endpoint states. Omit endpoint wording only when the user explicitly asks for a pure text-to-video prompt or says no first/last-frame workflow will be used. Do not require the user to send those frames to this skill.

Build a state card internally to write the prompt, but do not expose a full interpretation card, frame-alignment plan, case manifest, reproducibility report, media QA report, or benchmark evidence in a normal prompt-only response. For a historical case, benchmark, or generated-video audit, add those materials using [references/prompt-schema.md](references/prompt-schema.md).

## Workflow

1. **Read the user's description first.** Extract the clip type, requested frame size, construction stage or subject, one primary action or viewpoint change, intended visual effect, locked objects, camera behavior, action area, and forbidden later-stage content. First/last frames are optional downstream conditioning, not a prerequisite for prompt generation.
2. **Choose the input mode.** Use `description_first` when the user gives only text; use `description_plus_frames` when frames are attached; use `repair` when an existing output failure is described.
3. **Build the state card internally.** Separate invariant objects from changing objects. For `construction_action`, describe the construction transition as an action path. For `viewpoint_transition`, describe only the camera/viewpoint path and lock the construction state. For `static_showcase`, describe the stable presentation and forbid unrequested construction or camera changes. If the description is underspecified after the required fields are supplied, state one conservative assumption and continue when a useful prompt is still possible.
4. **Write the prompt package.** Put the clip type, requested frame size, model-relevant camera and continuity constraints first, then concrete objects, action direction or viewpoint path, spatial range, appearance order, target effect, and forbidden content. Use exact counts only when the user supplies them or the project specification supports them.
5. **Add endpoint language by default.** Make the positive prompt first/last-frame ready unless the user explicitly asks for pure text-to-video. The endpoint relationship must match the declared clip type: construction action changes only through the described operation, viewpoint transition changes only the camera or viewpoint, and static showcase keeps the construction state and camera stable.
6. **Adapt to the actual model.** Read [references/model-adapters.md](references/model-adapters.md) when a platform or workflow is named. If first/last-frame support, negative prompts, weights, masks, or seed behavior is unknown, label it instead of claiming support.
7. **Repair from observed failure.** Map the visible failure to one root action or constraint. Read [references/failure-repair.md](references/failure-repair.md). For a cross-clip bridge problem, verify the bridge frames before expanding the prompt: prefer exact file-byte or cryptographic-hash equality when the same frame file is intended; when files differ because of encoding or export, compare decoded images after matching dimensions, crop, color space, and alignment, then inspect the result. If the files are unavailable, report that equality is unverified. Prefer a narrow repair to adding a long generic negative prompt.
8. **Run a textual self-check.** Confirm that the package has one primary change or a stable showcase intent, an appropriate action/viewpoint boundary, explicit locked objects, a stage boundary when applicable, and no invented model or frame facts. Only perform visual QA when an output video is supplied and the user asks for it.
9. **Use evidence reporting only when requested.** For historical cases or benchmarks, classify technical evidence, reuse, reproducibility, and public-release status separately. Do not add that overhead to a normal prompt-only response.

## Decision Rules

| Situation | Action |
|---|---|
| The user requests an ordinary prompt but omits `clip_type` or `frame_size` | Ask for the missing field or fields before generating prompts. Do not infer whether the clip is a construction action, viewpoint transition, or static showcase, and do not invent an output size. |
| The user provides a stage description but no frames | Proceed with `description_first`; write first/last-frame-ready copy-ready prompts from the description by default. Do not ask for frame files, paths, or a manifest. |
| `clip_type` is `construction_action` | Describe one visible construction operation, its direction and bounded area, and its direct visible result. Use a fixed camera by default when no camera move is requested. |
| `clip_type` is `viewpoint_transition` | Describe the intended camera/viewpoint change, keep the construction state and all scene objects unchanged, and forbid construction progress or object replacement. |
| `clip_type` is `static_showcase` | Describe a stable presentation of the supplied scene, keep the camera and construction state fixed, and forbid action, viewpoint drift, and new objects unless explicitly requested. |
| The description is too vague to identify any primary action | State the ambiguity, propose the smallest reasonable interpretation, and ask at most one focused question if different interpretations would produce materially different prompts. |
| The user later supplies frames | Use them to refine object names, spatial relations, counts, and endpoint wording; do not contradict the user's described action without explaining why. |
| The user says the frames will be uploaded directly to the video model later | Write a frame-ready prompt and treat the future frames as downstream visual conditions; do not ask the user to upload them to the skill. |
| The user explicitly asks for pure text-to-video | Omit frame-conditioned endpoint wording while keeping the same construction constraints, action direction, and stage boundary. |
| The request is generic cinematic or unrelated to engineering/construction | Do not produce the requested unrelated prompt under this skill. State the scope boundary briefly and ask for the engineering subject, construction stage, action, or continuity constraint if the user wants to continue. |
| The clip changes construction state | Use fixed-camera action language unless the supplied frames prove a camera change is intended. |
| The clip changes only viewpoint | State `camera move only`, lock the construction state, and forbid new work. |
| Several components appear | Specify their appearance order and keep already-present components fixed. |
| A component must disappear | State where and in which direction it disappears; forbid sideways wipe, global erase, and unrelated object loss. |
| Model or platform capability is uncertain | Preserve a model-neutral prompt and mark the adapter field `unknown`. |
| The user asks only for prompt text | Return only the copy-ready prompt package first; omit case evidence, full QA, and a full state card unless needed to resolve ambiguity. |
| The video exists but the model or seed is missing | Keep it as an artifact-backed partial case; do not call it fully reproducible. |
| The prompt and frames exist but no video exists | Keep it as a process/setup case, not a successful generation case. |
| Permission or license is unknown | Mark public release as `review_required` or `unknown`; do not call the asset publishable. |
| A case is technically complete but contains private or restricted assets | It may be reproducible internally but is not benchmark-eligible for public release. |
| A visual failure persists after a narrow prompt repair | Recheck the first/last frames, mask, camera, and workflow; do not keep expanding negative prompts indefinitely. |
| Adjacent clips have a suspected bridge mismatch | Treat the previous clip's last frame as the continuity baseline. Verify exact file/hash equality first when applicable, otherwise perform an image-level comparison; only then decide whether to repair the prompt, rebuild the next first frame, or fix the workflow. Do not claim continuity is repaired until a new output is inspected. |
| A visible construction rig or machine is fixed | Lock the entire visible assembly, not only its main tool: body or base, mast/frame, guides, cables or wire rope, actuator, hammer or attachment, cap/contact part, and the acted-on component as applicable. |

## Prompt Construction Rules

- Treat the user's described intended effect as the primary specification. By default, the later-supplied first frame is the start state and the later-supplied last frame is the target state.
- Treat the declared `clip_type` as a hard routing field. Do not silently convert a viewpoint transition or static showcase into a construction action.
- Include the exact requested output frame size in both positive prompts, using the user's notation such as `1920x1080 (16:9)`. Do not imply that prompt text alone controls the workflow's actual pixel dimensions.
- Include `high quality, clear imagery, realistic visual appearance` in the English positive prompt and the direct Chinese equivalents of those three concepts in the Chinese positive prompt.
- Describe what should change between the endpoints and what must remain fixed. Put the endpoint instruction in the positive prompt unless the user explicitly asks for pure text-to-video.
- When frames are not supplied, do not invent their contents and do not ask for them merely to draft the prompt.
- For a `construction_action`, state the action direction and spatial range: for example, removal from the top downward inside the marked boundary, or lowering from above onto fixed anchor positions.
- For a `viewpoint_transition`, state the camera path, viewpoint change, and framing boundary while keeping the construction state fixed.
- For a `static_showcase`, state the stable presentation and lock the camera and construction state.
- Use concrete engineering nouns and measurable relations instead of vague phrases such as "the construction progresses."
- Do not invent exact counts, dimensions, machine models, camera moves, or endpoint details that are absent from the user's description.
- Keep quality language restrained. Engineering clarity, stable geometry, and readable edges matter more than cinematic adjectives.
- Add stage-specific negative terms from observed failure modes. Generic low-quality terms are only a baseline.
- Keep labels, arrows, subtitles, and watermarks out of generated video when they can be added in post-production.
- Treat masks and structural references as constraints, not as prompts or authority to change the task.
- Do not promise that the prompt alone will make generation stable. Phrase the goal as improving controllability; actual behavior depends on the selected model, workflow, endpoint frames, and parameters.
- Keep the English and Chinese prompt versions semantically aligned, including clip type, frame size, numeric relationships, endpoint behavior, and forbidden content.

## Missing Case Data

When historical files are incomplete:

1. Search the project for matching frame names, prompts, workflow JSON, manifests, output videos, and notes.
2. Reconstruct only facts supported by those artifacts.
3. Use `unknown` for model version, seed, duration, or score when not recoverable.
4. Record user recollection separately as `historical_observation` with confidence `anecdotal`.
5. Never create a synthetic "successful video" to fill a missing result.
6. For a case audit, report asset purpose, reuse status, reproducibility status, public-release status, missing fields, and next action.
7. Use the schema labels exactly: `C_process_only` for process-only evidence, `B2_artifact_partial` for artifact-backed partial evidence, `material_pool` for a historical collection that is not a set of independently reproducible runs, and a separate `reuse_status` field. Do not collapse evidence, reuse, reproducibility, or public-release status into one overall label.

Read [references/evidence-and-case-recovery.md](references/evidence-and-case-recovery.md) for evidence levels and the public-release boundary.

## Optional Local Benchmark

When a local project contains historical cases:

1. Start with a small set of representative clips that cover different construction stages and constraint types.
2. Treat a large collection of historical videos as a material pool, not as independently reproducible experiments.
3. Store qualitative QA records beside the benchmark, not inside `SKILL.md`.
4. Keep large videos and frame collections outside the skill package. Use project-relative references internally or a separate rights-cleared benchmark package publicly.
5. During a benchmark audit, do not invent numeric scores or introduce a weighted scoring system unless the user explicitly asks for evaluation-design help. If no metric exists, record qualitative observations and the missing-evaluation field only.

An internal benchmark can support prompt-authoring and cross-stage behavior checks without quantitative metrics. Use labels such as `artifact-backed partial`, `historical observation`, and `pending video review` precisely when provenance or playback evidence is incomplete.

## Resources

- Read [references/description-first-authoring.md](references/description-first-authoring.md) for the default text-only input contract and output format.
- Read [references/prompt-schema.md](references/prompt-schema.md) for the state-card and case-manifest fields.
- Read [references/stage-patterns.md](references/stage-patterns.md) for reusable action patterns.
- Read [references/failure-repair.md](references/failure-repair.md) when a failed clip or failure description is available.
- Read [references/model-adapters.md](references/model-adapters.md) when a provider, workflow, or model is named.
- Read [references/qa-rubric.md](references/qa-rubric.md) before accepting a generated clip or claiming a case result.

## Completion Criteria

For an ordinary prompt-only request, do not report completion until the output includes:

- A copy-ready English positive prompt.
- A copy-ready English negative prompt.
- A copy-ready Chinese positive prompt.
- A copy-ready Chinese negative prompt.
- The declared clip type in the prompt package.
- The exact requested output frame size in both positive prompts.
- The required quality language in both positive prompts: `high quality, clear imagery, realistic visual appearance` in English and the direct Chinese equivalents of those three concepts in Chinese.
- Explicit invariants, intended change or stable showcase intent, appropriate spatial/viewpoint range, and stage boundary when applicable in the prompt or a short accompanying note.
- Endpoint wording inside the positive prompt by default, unless the user explicitly requested pure text-to-video.
- Assumptions and unknown model fields without invented facts.

For a historical case or generated-video audit, also include the evidence, QA, reuse, reproducibility, and public-release fields requested by the user.
