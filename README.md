# Construction Video Prompt Engineering Skill

Current version: `v0.1`

An agent skill for writing copy-ready prompts for short construction-process video generation. The user describes one construction stage, the intended action, and the desired visual effect; the skill turns that description into structured positive and negative prompts for a video model.

This skill only generates prompt text. It does not create images, upload frames, run a video model, or guarantee a model result.

## What This Skill Is For

Use this skill when you need a prompt for a controlled construction-process clip, especially when the video should preserve:

- the construction stage boundary;
- the identity and position of key objects;
- a fixed or clearly specified camera;
- the direction and spatial range of the construction action;
- the difference between the starting state and target state;
- negative constraints such as no extra machinery, no premature later-stage content, no labels, and no unrelated geometry changes.

The default use case is description-first authoring: users do not need to send the first and last frames to the agent. The generated prompt is first/last-frame-ready by default, so users can later paste the prompt into a compatible video model and upload the corresponding start and end frames there.

## Suitable Video Models

This skill is model-agnostic at the prompt-writing level. It is most useful for short video workflows that accept:

- a text prompt;
- a start frame and an end frame, or an equivalent first/last-frame condition;
- optional positive and negative prompt fields;
- image-to-video or frame-conditioned video generation.

Typical compatible targets include first/last-frame video workflows, start/end-frame image-to-video systems, and construction-oriented video pipelines built around tools such as ComfyUI or other node-based generation interfaces.

It can also be adapted to single-image image-to-video models, but the prompt should be revised because those models do not have a true target end frame. For pure text-to-video models, ask explicitly for a text-to-video prompt; endpoint wording should then be omitted.

This repository does not claim support for a specific seed, sampler, provider, model checkpoint, resolution, or cloud service. Always verify the actual target workflow before relying on model-specific syntax.

## Installation

Install this folder as a Codex skill by placing it under your Codex skills directory, for example:

```text
~/.codex/skills/construction-video-prompt-engineering/
```

The required entry point is:

```text
SKILL.md
```

Optional UI metadata is included in:

```text
agents/openai.yaml
```

## Basic Usage

After installing the skill, ask the agent for a construction video prompt:

```text
Use $construction-video-prompt-engineering to write a prompt for a fixed-camera
construction video. The current stage is foundation pit excavation. Only the
exposed soil inside the pit should be removed from top to bottom. The retaining
wall, excavator position, surrounding ground, and camera must remain unchanged.
Do not show workers, water, labels, or the next construction stage. I will upload
the first and last frames to the video model later.
```

The skill should return prompt text that can be copied into the target video workflow.

## Recommended Input

Describe one clip at a time. A short paragraph is enough, but the following fields help the agent produce a more controllable prompt:

```yaml
construction_stage: "current construction stage"
primary_action: "one visible action in this clip"
desired_effect: "what the viewer should clearly understand"
camera_behavior: "fixed camera, close-up, pullback, or unknown"
locked_objects: "objects that must remain unchanged"
allowed_change: "what may change during the clip"
action_area_and_direction: "where the action happens and in which direction"
forbidden_content: "objects, stages, labels, or artifacts that must not appear"
target_workflow: "optional model or workflow name"
output_requirements: "optional duration, aspect ratio, resolution, or fps"
observed_failure: "optional failure to repair from a previous result"
```

If frames are not supplied, the skill should not ask for them just to draft the prompt. If frames are supplied, the agent may use them to refine object names, spatial relations, and endpoint wording.

## Expected Output

For an ordinary prompt request, the skill should produce:

1. An English positive prompt.
2. An English negative prompt.
3. Chinese review text when the user asks in Chinese or requests bilingual output.
4. A short assumption note only when an unstated choice materially affects the prompt.

The positive prompt should normally state that the uploaded first frame is the starting state and the uploaded last frame is the target state. This endpoint wording should be omitted only when the user explicitly asks for pure text-to-video or says no first/last-frame workflow will be used.

## Prompting Principles

The skill prioritizes engineering control over generic cinematic style:

- describe one primary construction action per clip;
- lock unchanged objects explicitly;
- define the action area and direction;
- keep camera movement conservative unless the user asks for it;
- prevent later construction stages from appearing early;
- avoid invented counts, dimensions, model names, seeds, or output settings;
- keep negative prompts focused on likely construction-video failures.

## Boundaries

This skill does not:

- run generation jobs;
- create first or last frames;
- inspect videos unless the user supplies them in a separate QA task;
- certify construction safety or engineering correctness;
- guarantee that any particular model will produce a stable result;
- bundle private BIM files, project media, model weights, credentials, or cloud workflow assets.

## Testing

Text-only evaluation cases are provided in:

```text
evals/evals.json
```

These cases check whether the skill follows the expected prompt-writing behavior, such as generating prompts from descriptions without requiring frames, handling pure text-to-video requests, and avoiding unsupported claims.

Run the tests manually according to:

```text
evals/README.md
```

These tests evaluate prompt behavior only. They are not proof that a specific video model will render a high-quality clip.

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
