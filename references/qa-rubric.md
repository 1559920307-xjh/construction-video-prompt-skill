# Video QA Rubric

Score each dimension from 0 to 2:

- `0`: fails or cannot be checked;
- `1`: partly acceptable or minor drift;
- `2`: clear pass.

| Dimension | Question |
|---|---|
| Stage correctness | Does the clip show only the intended construction stage? |
| Endpoint match | Does it start and end at the supplied states? |
| Camera continuity | Is the camera stable or moving exactly as specified? |
| Geometry continuity | Do site boundaries, walls, slabs, and fixed components retain shape and position? |
| Component identity | Are machinery and repeated components the same category, count, and approximate silhouette? |
| Action direction | Does the change occur in the specified direction and area? |
| Order | Do multi-component actions occur in the required sequence? |
| Artifact quality | Are frames playable, sharp enough, and free of flicker, black frames, text, or watermarks? |

## Acceptance Guidance

- `14-16`: candidate for editing, with any remaining defects disclosed.
- `10-13`: usable only with a repair note or selective trimming.
- `0-9`: failure sample; revise prompt, inputs, or workflow.

Do not convert an uncheckable dimension into a pass. Record `not_checked` when no output or no suitable inspection artifact exists.

## Cross-Clip Checks

For a sequence:

1. Compare each clip's last frame to the next clip's first frame.
2. Prefer byte or hash equality for an intentional bridge frame.
3. Check that a later-stage component does not appear before its stage.
4. Check camera, site scale, and recurring machinery across at least two adjacent clips.
5. Report the number of clips checked, not only the best clip.

