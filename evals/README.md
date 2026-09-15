# Generic Evaluation Guide

These are text-only behavioral evaluations for the public skill package. They test description-first prompt-generation behavior, not the visual quality of a video model.

## What Each Case Tests

`evals.json` covers:

- direct construction-video prompt generation from a description without frames;
- optional refinement when first/last frames are supplied;
- bridge-frame and component-drift repair;
- incomplete historical evidence;
- a request that should not trigger this skill;
- ordered construction-component appearance;
- a workflow with no verified output;
- a description-only hammer-pile request that should still produce first/last-frame-ready prompts;
- an explicit pure text-to-video request where endpoint wording should be omitted.

## Manual Test Procedure

1. Start a fresh agent session with this skill installed.
2. Give the agent one `prompt` from `evals.json` exactly as written.
3. Do not provide the entry's `expectations` to the agent.
4. Compare the response with the expected route and every expectation.
5. Record pass, partial, or fail in a copy of `eval-results-template.json`.
6. Repeat for every case after any meaningful change to `SKILL.md` or its references.

## Pass Criteria

- `expected_route` must match.
- Every expectation that protects engineering correctness, evidence honesty, or task boundaries must pass.
- Style differences are acceptable when the copy-ready prompts contain the required engineering constraints and evidence treatment is appropriate to the request.
- A response must not block on absent frames for an ordinary description-first request.
- Ordinary construction-video prompts should include first/last-frame endpoint wording by default.
- Endpoint wording should be omitted only when the user explicitly asks for pure text-to-video or no first/last-frame workflow.
- A response must not invent unavailable frame contents, model capabilities, seed values, licenses, benchmark scores, or successful outputs.

Do not treat generic text-only results as proof that a specific video model will render correctly. Test actual visual behavior separately with an internal or rights-cleared media benchmark.

## Recommended Release Gate

Publish a new version only when all route checks pass and no case fails a critical expectation. Keep the completed result record with the release notes or repository CI artifacts.
