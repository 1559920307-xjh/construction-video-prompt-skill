# Construction Video Prompt Engineering Skill

Version: `v0.1`

An agent skill for writing controllable prompts for short engineering and construction videos. The user identifies whether the clip is a construction action, a viewpoint transition, or a static showcase; provides the requested output frame size; and describes the intended action or visual effect. The skill converts that description into copy-ready English and Chinese positive and negative prompts.

The skill is a prompt-authoring layer only. It does not create first or last frame images, run ComfyUI, submit cloud jobs, or guarantee a generated video result.

## Primary Target

This skill is designed primarily for **first/last-frame video generation**, especially workflows that receive both a starting image and an ending image and synthesize the motion between them.

The main project-aligned target is:

- **Wan 2.2 FLF2V**: Wan 2.2 First-Last-Frame-to-Video generation;
- **ComfyUI workflows** that expose separate first-frame and last-frame inputs;
- workflows with positive and negative text conditioning;
- short image-to-video clips in which the scene remains controlled during one construction action, one viewpoint transition, or one static showcase.

This design choice is important: construction-process videos usually need a reliable relationship between two engineering states. The first frame defines the starting condition, the last frame defines the target condition, and the prompt describes the allowed action between them.

## Wan 2.2 and ComfyUI Workflow Compatibility

The skill's default prompt structure matches a Wan 2.2 FLF2V workflow with the following general components:

```text
First frame image --------------\
                                  -> first/last-frame video conditioning
Last frame image ---------------/                    |
                                                       v
Positive prompt -> Wan text encoder -> positive conditioning
Negative prompt -> Wan text encoder -> negative conditioning
                                                       |
Wan 2.2 high-noise model -----------------------------|
Wan 2.2 low-noise model ------------------------------|-> sampling / decoding
Wan VAE ----------------------------------------------|
                                                       v
                                                   output video
```

A compatible ComfyUI workflow commonly includes:

- separate loaders or inputs for the first and last images;
- Wan 2.2 high-noise and low-noise video model components, commonly using the 14B model family;
- the Wan UMT5 text encoder;
- the Wan VAE;
- a first/last-frame conditioning node such as `WanFirstLastFrameToVideo`;
- positive and negative prompt conditioning;
- sampling, video creation, and video saving nodes.

The exact node names, model files, sampler settings, resolution limits, frame count, and output format may vary between ComfyUI workflows. This skill does not hard-code those parameters. It supplies the semantic prompt layer that describes:

1. what must remain fixed;
2. what construction action is allowed;
3. where the action occurs;
4. in which direction the action develops;
5. how the starting and target states are related;
6. which artifacts or later-stage elements must not appear.

## Why First/Last-Frame Models Are the Best Fit

Construction videos are state-transition problems rather than purely cinematic scenes. A frame-conditioned workflow is therefore usually a better fit than pure text-to-video when the result must preserve engineering structure.

First/last-frame conditioning is useful for:

- preserving the position and identity of machines, structures, and site elements;
- defining the exact beginning and end of one construction operation;
- controlling the appearance order of components;
- limiting changes to a marked area or one component;
- reducing camera drift and unintended geometry changes;
- making adjacent clips easier to connect through shared endpoint states.

The skill writes prompts for this workflow by default. It does not require the user to provide the frames to the agent. The user can describe the intended clip first, receive the prompt, and upload the corresponding first and last frames later in ComfyUI or another compatible video workflow.

## Model Compatibility

| Video workflow type | Compatibility | Notes |
|---|---|---|
| Wan 2.2 FLF2V in ComfyUI | Primary | The default prompt structure is designed for this workflow shape. |
| Other first/last-frame video workflows | Strong with adaptation | Keep the construction constraints and adapt the model-specific prompt fields. |
| Other start/end-frame image-to-video workflows | Applicable | Verify frame order, negative-prompt support, and workflow-specific syntax. |
| Single-image image-to-video workflows | Partial | Keep the action and object-continuity rules, but remove unsupported target-endpoint claims. |
| Pure text-to-video workflows | Limited | Ask explicitly for a text-to-video prompt; no endpoint constraint can be enforced by this skill. |

The skill does not claim that every model supports first/last-frame conditioning, negative prompts, the same tokenization, or the same prompt syntax. Verify the target workflow before using model-specific features.

## Installation

Install this folder as a Codex skill under your Codex skills directory:

```text
~/.codex/skills/construction-video-prompt-engineering/
```

The required skill entry point is:

```text
SKILL.md
```

The optional UI metadata file is:

```text
agents/openai.yaml
```

## Basic Usage

Describe one clip and explicitly provide the clip type and output frame size:

```text
Use $construction-video-prompt-engineering to write a Wan 2.2 FLF2V prompt.
Clip type: construction_action.
Output frame size: 1920x1080 (16:9).
Duration: 3-5 seconds.
I have first and last frame images for a hammer-driven pile installation clip.
Show one complete construction action: the hammer lifts vertically, then falls
vertically and makes one impact on the pile cap; the pile sinks vertically by
approximately 25% relative to its initial reference position. Keep the
pile-driving rig, guide frame, wire rope, hammer, pile cap, pile, construction
site, camera position, and composition unchanged. Do not show workers, extra
piles, multiple impacts, repeated cycles, text, or watermarks. I will upload
the first and last frames to the Wan 2.2 FLF2V ComfyUI workflow.
```

The agent should return four copy-ready prompt blocks:

1. English positive prompt.
2. English negative prompt.
3. Chinese positive prompt.
4. Chinese negative prompt.

The two positive prompts must explicitly mention the declared clip type and output frame size. The Chinese version is for semantic comparison before the English version is pasted into the video workflow.

## Required Prompt Inputs

For ordinary prompt generation, provide these two fields explicitly:

- **Clip type**:
  - `construction_action`: the construction state changes because of one visible construction operation.
  - `viewpoint_transition`: the camera or viewpoint changes while the construction state remains unchanged.
  - `static_showcase`: the subject is presented from a stable view without a construction-state change or deliberate camera move.
- **Output frame size**: provide the exact width and height in pixels, preferably with the aspect ratio, for example `1920x1080 (16:9)` or `1024x576 (16:9)`.

If either required field is missing, the agent should ask for it instead of guessing. First and last frame images are optional for writing the prompt and can be uploaded later to the target video workflow.

## Recommended Input

A natural-language paragraph is sufficient. The following information improves controllability:

```yaml
clip_type: "construction_action | viewpoint_transition | static_showcase"
frame_size: "1920x1080 (16:9)"
construction_stage_or_subject: "current construction stage or subject being shown"
primary_action_or_viewpoint_change: "one visible construction action or one camera/viewpoint change"
desired_effect: "what the viewer should clearly understand"
camera_behavior: "fixed camera, close-up, pullback, or unknown"
locked_objects: "objects that must remain unchanged"
allowed_change: "what may change during the clip"
action_area_and_direction: "where the action happens and in which direction"
forbidden_content: "objects or stages that must not appear"
target_model_or_workflow: "optional, for example Wan 2.2 FLF2V in ComfyUI"
duration: "optional, for example 3-5 seconds"
output_settings: "optional fps, seed, sampler, or other workflow settings"
observed_failure: "optional failure from an earlier generation"
```

First and last frame files are optional for prompt writing. If they are not supplied, the skill must not block on missing files or invent their contents. If they are supplied, the agent may use them to refine object names, spatial relations, counts, and endpoint wording.

## Expected Output

For a normal request, the skill produces:

1. an English positive prompt;
2. an English negative prompt;
3. a Chinese positive prompt;
4. a Chinese negative prompt;
5. a short assumption or adapter note only when an unstated choice materially affects the prompt.

For first/last-frame workflows, both positive prompts normally state that the uploaded first frame is the exact starting state and the uploaded last frame is the target state. They also include the declared clip type and exact output frame size. Only the change allowed by that clip type may occur between those states.

If the user explicitly requests pure text-to-video, the endpoint wording is omitted.

## Prompting Principles

The skill emphasizes construction control over generic cinematic language:

- describe one primary action per clip;
- classify the clip as a construction action, viewpoint transition, or static showcase;
- include the requested output frame size in both positive prompts;
- identify the current construction stage;
- lock unchanged objects and the camera;
- define the action area and direction;
- preserve object identity and spatial relationships;
- state the intended visible effect;
- prevent later-stage or unrelated content from appearing early;
- use negative prompts that target the likely failure modes;
- do not invent model names, engineering counts or dimensions, seeds, or workflow settings;
- keep the English and Chinese versions semantically aligned;
- distinguish prompt-level frame-size wording from the actual resolution configured in the video workflow.

## Boundaries

This skill does not:

- generate or edit images;
- generate or edit videos;
- execute ComfyUI or cloud workflows;
- inspect a video unless the user supplies it for a separate repair or QA task;
- certify construction safety, engineering compliance, or construction sequencing;
- guarantee stable results for any particular model or seed;
- include private project media, BIM files, model weights, credentials, or workflow assets.

## Testing

Text-only evaluation cases are provided in:

```text
evals/evals.json
```

The cases check description-first prompt generation, first/last-frame behavior, pure text-to-video handling, failure repair, and avoidance of unsupported claims.

Run the manual evaluation procedure in:

```text
evals/README.md
```

These evaluations test prompt behavior. They do not prove that a particular Wan 2.2 checkpoint, ComfyUI workflow, sampler, or parameter set will produce a specific visual result.

## Repository Layout

```text
construction-video-prompt-engineering/
|-- SKILL.md
|-- README.md
|-- LICENSE
|-- agents/
|   `-- openai.yaml
|-- evals/
|-- references/
`-- scripts/
```
