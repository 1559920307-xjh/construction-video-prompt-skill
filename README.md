# Construction Video Prompt Engineering Skill

Version: `v0.1`

An agent skill for writing controllable prompts for short construction-process videos. The user describes one construction stage, the intended action, and the desired visual effect. The skill converts that description into a copy-ready positive prompt and a focused negative prompt.

The skill is a prompt-authoring layer only. It does not create first or last frame images, run ComfyUI, submit cloud jobs, or guarantee a generated video result.

## Primary Target

This skill is designed primarily for **first/last-frame video generation**, especially workflows that receive both a starting image and an ending image and synthesize the motion between them.

The main project-aligned target is:

- **Wan 2.2 FLF2V**: Wan 2.2 First-Last-Frame-to-Video generation;
- **ComfyUI workflows** that expose separate first-frame and last-frame inputs;
- workflows with positive and negative text conditioning;
- short image-to-video clips in which the scene should remain stable while one construction action occurs.

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

Describe one construction clip and ask the agent to use the skill:

```text
Use $construction-video-prompt-engineering to write a Wan 2.2 FLF2V prompt.
The current stage is foundation pit excavation. Keep the retaining wall,
excavator, surrounding ground, and camera unchanged. Remove only the exposed
soil inside the pit from top to bottom so the change in excavation depth is
clear. Do not show workers, labels, water, or the next construction stage. I
will upload the first and last frames to ComfyUI later.
```

The agent should return a positive prompt and a negative prompt that can be copied into the corresponding ComfyUI text-conditioning fields.

## Recommended Input

A natural-language paragraph is sufficient. The following information improves controllability:

```yaml
construction_stage: "current construction stage"
primary_action: "one visible action in this clip"
desired_effect: "what the viewer should clearly understand"
camera_behavior: "fixed camera, close-up, pullback, or unknown"
locked_objects: "objects that must remain unchanged"
allowed_change: "what may change during the clip"
action_area_and_direction: "where the action happens and in which direction"
forbidden_content: "objects or stages that must not appear"
target_model_or_workflow: "optional, for example Wan 2.2 FLF2V in ComfyUI"
output_requirements: "optional duration, aspect ratio, resolution, or fps"
observed_failure: "optional failure from an earlier generation"
```

First and last frame files are optional for prompt writing. If they are not supplied, the skill must not block on missing files or invent their contents. If they are supplied, the agent may use them to refine object names, spatial relations, counts, and endpoint wording.

## Expected Output

For a normal request, the skill produces:

1. an English positive prompt;
2. an English negative prompt;
3. Chinese review text when requested by the user;
4. a short assumption note only when an unstated choice materially affects the prompt.

For first/last-frame workflows, the positive prompt normally states that the uploaded first frame is the exact starting state and the uploaded last frame is the target state. Only the described construction action may change between those states.

If the user explicitly requests pure text-to-video, the endpoint wording is omitted.

## Prompting Principles

The skill emphasizes construction control over generic cinematic language:

- describe one primary action per clip;
- identify the current construction stage;
- lock unchanged objects and the camera;
- define the action area and direction;
- preserve object identity and spatial relationships;
- state the intended visible effect;
- prevent later-stage or unrelated content from appearing early;
- use negative prompts that target the likely failure modes;
- do not invent model names, counts, dimensions, seeds, or output settings.

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
