# Evidence and Case Recovery

## Why Missing Historical Records Are Recoverable

A successful old run can still provide useful evidence even when its original experiment log is incomplete. Treat the surviving files as a forensic reconstruction, not as a new controlled experiment. Keep three judgments separate: whether the method is reusable, whether the run is technically reproducible, and whether the assets may be publicly redistributed.

Search for these artifact classes:

1. **Inputs:** first frames, last frames, Blender renders, masks, depth or edge references.
2. **Instruction:** positive prompt, negative prompt, stage table, failure notes, or prompt history.
3. **Execution:** workflow JSON, platform name, model file names, seed, steps, duration, resolution, and run date.
4. **Outputs:** generated video, frame sequence, contact sheet, selected/final version, or edit timeline.
5. **Assessment:** score, comparison table, failure label, user report, or a note explaining why one result was selected.

Create a case directory or manifest that points to the original files. Do not duplicate large media unless a release package needs a small, rights-cleared fixture.

## Evidence Levels

| Level | Meaning | What may be claimed |
|---|---|---|
| `A_complete` | Inputs, exact model/version, prompts, relevant parameters, workflow, output, and QA are all present | Reproducible case, subject to platform/model drift |
| `B2_artifact_partial` | Important inputs and output survive, but one or more execution fields are missing | Artifact-backed result; not fully reproducible |
| `C_process_only` | Prompt, inputs, workflow, or design notes survive, but no verified output survives | Process/setup evidence only |
| `D_anecdotal` | Only memory or a narrative assertion survives | Historical observation, not an experiment result |

An output video without the exact model is still valuable. A prompt and model without an output video are not evidence that the prompt worked.

Evidence level does not imply permission. A technically complete case can still be `review_required` for public release, and a partially documented case can still be useful for internal method reuse.

## Build a Recovery Map

For each candidate project or clip family, record:

| Candidate | What survives | Provisional classification | Missing or uncertain |
|---|---|---|---|
| Historical output clips with first/last frames and prompts | Inputs, outputs, and instruction records | Usually `B2_artifact_partial` | Exact runtime model, per-run parameters, hashes, or QA |
| Workflow and stage images with no verified video | Inputs and process records | `C_process_only` | A verified output video and execution record |
| Image-realification or continuity experiments | Masks, references, and image workflows | Supporting evidence, not automatically a video case | A video-generation output and video-model run metadata |

These classifications are deliberately conservative. They can be upgraded when an exact model field, run metadata, or output QA record is recovered. Keep the labels separate: evidence level describes what survives, `reuse_status` describes whether the method can be reused, `reproducibility_status` describes whether the run can be recreated, and `public_release_status` describes redistribution permission.

The recovery map is a candidate inventory, not a fact registry. Before using a case in a release, recheck that every referenced path exists, that the frame pair matches the described clip, that the workflow contains the claimed model/settings, and that the output is the claimed file.

## Reconstruction Procedure

1. Copy only small metadata or create a manifest with relative source references.
2. Compute a hash for every input and output that will be cited in a release.
3. Extract the prompt and negative prompt from the manifest or workflow; if a prompt was edited after generation, preserve both the run version and the later revision.
4. Resolve first/last-frame pairs by filename and continuity notes. Confirm that adjacent clips really share the same bridge frame.
5. Inspect workflow JSON for model filenames and node settings. A workflow title is a clue, not proof that a named model was used.
6. Record missing values as `unknown`.
7. Record the original qualitative observation separately, for example: "user reports that cross-case generation worked very well." Mark its source and confidence.
8. Re-run only the smallest representative cases if a controlled result is needed. Use the recovered files as a historical baseline, not as a replacement for missing provenance.
9. Assign `reuse_status`, `reproducibility_status`, and `public_release_status` independently. Treat unknown permission as not cleared.
10. If many historical clips share a project but lack per-run model, seed, and execution records, call them a `material_pool` or historical case library. Do not call the collection a complete public benchmark, and do not imply that every clip is independently reproducible.
11. If no formal metric exists, report qualitative QA only. Do not invent scores or a weighted rubric during evidence recovery unless evaluation design is explicitly requested.

## Public Release Boundary

The portable skill should contain:

- `SKILL.md`, references, schemas, and small text-only evaluation prompts.
- Optional tiny, rights-cleared fixtures or synthetic placeholders.
- Clear statements about model/platform assumptions and unknowns.

Keep these outside the core skill unless licensing and file size are explicitly handled:

- Model weights, API keys, account identifiers, or cloud task URLs.
- Large collections of generated videos and hundreds of high-resolution frames.
- Proprietary BIM files, private project geometry, or third-party images without redistribution permission.
- Claims that a particular model will reproduce the result indefinitely.

A separate benchmark release may contain a few representative bundles:

```text
case-id/
├── case.json
├── first.png
├── last.png
├── prompt_positive.txt
├── prompt_negative.txt
├── output.mp4
├── qa.json
└── LICENSE
```

The benchmark bundle is useful for demonstrating and evaluating the skill, but it is not required for the skill to generate a new prompt. Set `benchmark_eligible` to `true` only after the technical and permission gates in [references/prompt-schema.md](prompt-schema.md) pass.
