# Prompt and Case Schema

Use `unknown` when a value should exist but cannot be recovered. Use `not_applicable` only when the field is genuinely irrelevant. Do not use an empty string to hide missing evidence.

## Interpretation Card and State Card

For an ordinary prompt request, frames are not required. Use `input_mode` to distinguish a text-only request from a request that includes actual visual references supplied for wording refinement.

```yaml
project: "project name"
case_id: "stable-case-id"
clip_id: "clip-01"
input_mode: "description_first | description_plus_frames | repair"
construction_stage: "single stage or operation"
mode: "fixed_camera_action | camera_only | mixed"
primary_action: "one primary action"
target_effect: "desired visible effect"
first_frame: "path or URI, or not_supplied"
last_frame: "path or URI, or not_supplied"
planned_first_state: "what the first frame should show when frames are prepared later"
planned_last_state: "what the last frame should show when frames are prepared later"
intended_change:
  action: "one primary action"
  direction: "downward | upward | horizontal | toward_target | away_from_target | opacity_only | unknown"
  spatial_range: "where the action may occur"
  order:
    - "step 1"
    - "step 2"
invariants:
  - "camera pose or permitted camera change"
  - "site boundary"
  - "component identity and position"
required_components:
  - id: "component-id"
    description: "observable identity"
    count: "exact integer, range, or unknown"
    position: "position or relation"
forbidden_components:
  - "next-stage object or unrelated object"
known_failures:
  - "visible failure phrased as an observation"
assumptions:
  - "explicit assumption made because the user did not specify a fact"
```

## Case Manifest

The manifest describes an experiment or historical reconstruction. It is separate from the runtime skill instructions.

```yaml
schema_version: "0.1"
case_id: "stable-case-id"
title: "human-readable title"
domain: "construction process"
task_type: "video_generation | image_realification | mixed"
collection_status: "individual_case | material_pool"
benchmark_eligible: false
evidence_level: "A_complete | B2_artifact_partial | C_process_only | D_anecdotal"
reuse_status: "reusable | reusable_with_attribution | internal_only | unknown"
reproducibility_status: "complete | partial | process_only | anecdotal | unknown"
public_release_status: "cleared | review_required | prohibited | unknown"
source_refs:
  - "relative/path/to/file"
model:
  provider: "provider or unknown"
  family: "model family or unknown"
  id: "exact model ID or unknown"
  version: "version or unknown"
workflow:
  platform: "ComfyUI | RunningHub | LibTV | unknown"
  file: "relative/path/to/workflow.json"
  revision: "workflow revision or unknown"
inputs:
  first_frames:
    - "relative/path/to/start.png"
  last_frames:
    - "relative/path/to/end.png"
  masks:
    - "relative/path/to/mask.png"
  prompt_positive: "relative/path or inline reference"
  prompt_negative: "relative/path or inline reference"
parameters:
  duration_seconds: "number or unknown"
  fps: "number or unknown"
  resolution: "width x height or unknown"
  seed: "number, fixed, or unknown"
  steps: "number or unknown"
outputs:
  videos:
    - "relative/path/to/output.mp4"
  output_count: "integer or unknown"
evaluation:
  score: "number or unknown"
  rubric: "relative/path or unknown"
  measured_metrics: []
  qualitative_observation:
    text: "what was observed"
    source: "artifact | user_report | reconstruction"
    confidence: "high | medium | anecdotal"
license:
  inputs: "license or permission status"
  outputs: "license or permission status"
  model_and_workflow: "license or permission status"
notes: "remaining uncertainty"
```

## Status Semantics

- `collection_status` describes whether the manifest represents one case or a historical collection of materials. `material_pool` does not mean that every item is an independently reproducible run.
- `reuse_status` asks whether the prompt, workflow, or method may be reused for another task. It is not a license decision.
- `reproducibility_status` asks whether another operator can recreate the technical run from the surviving artifacts.
- `public_release_status` asks whether the cited assets may be redistributed outside the project. If permission or license is unknown, use `review_required` or `unknown`, never `cleared`.
- `benchmark_eligible` may be `true` only when `reproducibility_status` is `complete`, the output and QA are present, all cited assets have stable references or hashes, and `public_release_status` is `cleared`.

## Minimum Fields by Claim

| Claim | Minimum evidence |
|---|---|
| Prompt draft | Natural-language construction description plus the internally derived state card; frames are not required |
| Process case | Prompt, input references, and workflow or parameter notes |
| Artifact-backed partial result | Prompt, first/last frames, output video, and at least one workflow or model clue |
| Fully reproducible result | Exact model/version, first/last frames, prompts, relevant parameters, workflow, output, hashes or stable asset references, and a QA record |
