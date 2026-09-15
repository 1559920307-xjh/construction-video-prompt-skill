# Model Adapter Notes

This reference is intentionally capability-oriented. Video platforms and model files change quickly, and a workflow filename is not enough to prove the exact runtime model.

## Evidence From the Project Workflows

The inspected hammer-pile RunningHub / ComfyUI JSON is an image-realization graph,
not a video graph. It loads `RealVisXL V5.0 (BakedVAE) fp32`, SDXL Canny and Depth
Control-LoRA models, and uses KSampler, VAE inpainting, and `SaveImage` nodes. It has
no `WanFirstLastFrameToVideo`, `CreateVideo`, or `SaveVideo` node. Treat it as an
upstream workflow for producing realistic keyframes.

The project also contains a separate native ComfyUI / RunningHub **Wan 2.2 FLF2V**
workflow whose graph includes Wan 2.2 high-noise and low-noise I2V 14B models, Wan
UMT5, Wan VAE, separate start/end image inputs, `WanFirstLastFrameToVideo`, and video
output nodes. That workflow shape is the primary project-aligned target for prompts
from this skill. This is repository evidence about the inspected workflow, not a
guarantee about every installation or future model revision.

## Record These Fields

| Field | Required question |
|---|---|
| `provider` | Which service or local runtime executed the job? |
| `model.id` and `model.version` | What exact model or checkpoint was loaded? |
| `task_type` | Text-to-video, image-to-video, first/last-frame video, image editing, or a mixed pipeline? |
| `frame_conditioning` | Does the actual workflow consume first and last frames, or only one image? |
| `negative_prompt` | Is a negative prompt input actually used by the workflow? |
| `seed` | Is the seed exposed and fixed, or unknown? |
| `duration`, `fps`, `resolution` | What output settings were used? |
| `workflow` | Which JSON, node graph, or API request was executed? |
| `output` | Where is the output video, and is it playable? |

## Public Adapter Boundary

Video platforms and first/last-frame workflows change quickly. Treat names such as ComfyUI, RunningHub, LibTV, Wan FLF2V, VACE, or any hosted video model as user-supplied workflow context, not as proof of capability. When a user names a platform, inspect the actual workflow or current official documentation before making adapter-specific claims.

Project-specific workflow clues, local manifests, and historical run notes belong in a separate internal benchmark or case record, not in the public skill instructions.

## Adapter Behavior

If a capability is not confirmed:

1. Keep the core prompt model-neutral.
2. Put provider syntax in a separate adapter block.
3. Mark unsupported or unknown fields explicitly.
4. Do not promise that weights, negative prompts, masks, or dual-frame conditioning are honored.
5. Preserve the original prompt and the adapted prompt separately in the case record.

The skill can write a description-first prompt before frames are prepared. This does not prove that the target workflow supports first/last-frame conditioning. If the user plans to upload frames later, label the prompt as frame-ready and verify the actual workflow's conditioning behavior separately.
