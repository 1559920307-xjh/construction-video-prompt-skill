#!/usr/bin/env python3
"""Validate the lightweight case manifest used by the construction-video skill."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


EVIDENCE_LEVELS = {
    "A_complete",
    "B2_artifact_partial",
    "C_process_only",
    "D_anecdotal",
}

REUSE_STATUSES = {
    "reusable",
    "reusable_with_attribution",
    "internal_only",
    "unknown",
}

REPRODUCIBILITY_STATUSES = {
    "complete",
    "partial",
    "process_only",
    "anecdotal",
    "unknown",
}

PUBLIC_RELEASE_STATUSES = {
    "cleared",
    "review_required",
    "prohibited",
    "unknown",
}

COLLECTION_STATUSES = {
    "individual_case",
    "material_pool",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate construction-video case-manifest.json structure."
    )
    parser.add_argument("manifest", type=Path, help="Path to a JSON case manifest.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail when a case is not fully reproducible or has missing fields.",
    )
    return parser.parse_args()


def add_error(errors: list[str], case_id: str, message: str) -> None:
    errors.append(f"{case_id}: {message}")


def validate_case(case: dict, strict: bool, errors: list[str], warnings: list[str]) -> None:
    case_id = str(case.get("case_id", "<missing-case-id>"))
    required = (
        "case_id",
        "title",
        "task_type",
        "evidence_level",
        "reuse_status",
        "reproducibility_status",
        "public_release_status",
        "model",
        "inputs",
        "outputs",
    )
    for field in required:
        if field not in case:
            add_error(errors, case_id, f"missing required field '{field}'")

    evidence = case.get("evidence_level")
    if evidence not in EVIDENCE_LEVELS:
        add_error(errors, case_id, f"invalid evidence_level: {evidence!r}")

    collection_status = case.get("collection_status", "individual_case")
    if collection_status not in COLLECTION_STATUSES:
        add_error(errors, case_id, f"invalid collection_status: {collection_status!r}")

    status_sets = (
        ("reuse_status", REUSE_STATUSES),
        ("reproducibility_status", REPRODUCIBILITY_STATUSES),
        ("public_release_status", PUBLIC_RELEASE_STATUSES),
    )
    for field, allowed in status_sets:
        value = case.get(field)
        if value not in allowed:
            add_error(errors, case_id, f"invalid {field}: {value!r}")

    model = case.get("model") or {}
    for field in ("provider", "family", "id", "version"):
        if field not in model:
            add_error(errors, case_id, f"model.{field} is missing")

    inputs = case.get("inputs") or {}
    for field in ("first_frames", "last_frames", "prompt_positive", "prompt_negative"):
        if field not in inputs:
            add_error(errors, case_id, f"inputs.{field} is missing")

    outputs = case.get("outputs") or {}
    if "videos" not in outputs:
        add_error(errors, case_id, "outputs.videos is missing")

    if evidence == "A_complete":
        missing = []
        if model.get("id") in (None, "", "unknown"):
            missing.append("exact model id")
        if model.get("version") in (None, "", "unknown"):
            missing.append("model version")
        if not inputs.get("first_frames") or not inputs.get("last_frames"):
            missing.append("first/last frames")
        if not inputs.get("prompt_positive") or not inputs.get("prompt_negative"):
            missing.append("positive/negative prompts")
        if not outputs.get("videos"):
            missing.append("output video")
        if missing:
            message = "complete case is missing " + ", ".join(missing)
            if strict:
                add_error(errors, case_id, message)
            else:
                warnings.append(f"{case_id}: {message}")

    if case.get("benchmark_eligible") is True and evidence != "A_complete":
        message = "benchmark_eligible must be false until evidence_level is A_complete"
        if strict:
            add_error(errors, case_id, message)
        else:
            warnings.append(f"{case_id}: {message}")

    if case.get("benchmark_eligible") is True:
        if case.get("reproducibility_status") != "complete":
            add_error(errors, case_id, "benchmark_eligible requires reproducibility_status 'complete'")
        if case.get("public_release_status") != "cleared":
            add_error(errors, case_id, "benchmark_eligible requires public_release_status 'cleared'")


def main() -> int:
    args = parse_args()
    try:
        payload = json.loads(args.manifest.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"error: manifest not found: {args.manifest}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON: {exc}", file=sys.stderr)
        return 2

    if not isinstance(payload, dict) or not isinstance(payload.get("cases"), list):
        print("error: manifest must be an object with a 'cases' array", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    for case in payload["cases"]:
        if not isinstance(case, dict):
            errors.append("case entry is not an object")
            continue
        validate_case(case, args.strict, errors, warnings)

    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}", file=sys.stderr)

    if errors:
        return 1
    print(f"ok: validated {len(payload['cases'])} case(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
