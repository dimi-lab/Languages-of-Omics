#!/usr/bin/env python3
"""Validate the machine-readable omics foundation-model catalog."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from http.client import RemoteDisconnected
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "models.json"

REQUIRED = {
    "id",
    "name",
    "year",
    "status",
    "kind",
    "primary_omics",
    "omics",
    "input_language",
    "output_language",
    "scale",
    "paper",
    "code",
    "weights",
    "why_it_matters",
    "tags",
    "last_verified",
}

STATUSES = {"peer-reviewed", "preprint", "released"}
KINDS = {"foundation-model", "multimodal-bridge", "foundation-enabled-system"}
PRIMARY_OMICS = {
    "genomics",
    "transcriptomics",
    "proteomics",
    "rna",
    "epigenomics",
    "spatial-omics",
    "metabolomics",
    "cross-omics",
}
MODALITIES = PRIMARY_OMICS | {"protein-structure", "natural-language", "pathology"}
TAGS = {
    "api",
    "contrastive",
    "cross-species",
    "design",
    "generative",
    "long-context",
    "mass-spectrometry",
    "multimodal",
    "non-commercial",
    "open-code",
    "perturbation",
    "preprint",
    "regulatory",
    "representation",
    "sequence-to-function",
    "single-cell",
    "spatial",
    "structure-aware",
    "text-interface",
    "weights",
}
URL_FIELDS = ("paper", "code", "weights")


def load_catalog() -> list[dict]:
    try:
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Could not read {CATALOG}: {exc}") from exc
    if not isinstance(data, list):
        raise SystemExit("Catalog root must be a JSON array.")
    return data


def check_url(url: str, timeout: int = 15) -> tuple[bool, str]:
    request = Request(url, headers={"User-Agent": "awesome-omics-catalog-link-check/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            return 200 <= response.status < 400, str(response.status)
    except HTTPError as exc:
        # Some publisher and model-hosting pages reject automation while remaining live.
        if exc.code in {401, 403, 405, 429}:
            return True, f"reachable but automation-limited ({exc.code})"
        return False, f"HTTP {exc.code}"
    except (URLError, TimeoutError, RemoteDisconnected) as exc:
        return False, str(exc)


def validate(records: list[dict], live_links: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: set[str] = set()
    link_targets: list[tuple[str, str, str]] = []

    for index, item in enumerate(records):
        label = item.get("id", f"record[{index}]") if isinstance(item, dict) else f"record[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label}: entry must be an object")
            continue

        missing = REQUIRED - set(item)
        extra = set(item) - REQUIRED
        if missing:
            errors.append(f"{label}: missing fields: {', '.join(sorted(missing))}")
        if extra:
            errors.append(f"{label}: unknown fields: {', '.join(sorted(extra))}")
        if missing:
            continue

        model_id = item["id"]
        if not isinstance(model_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", model_id):
            errors.append(f"{label}: id must be a lowercase kebab-case slug")
        elif model_id in seen_ids:
            errors.append(f"{label}: duplicate id")
        else:
            seen_ids.add(model_id)

        for field in ("name", "input_language", "output_language", "scale", "why_it_matters"):
            value = item[field]
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{label}: {field} must be a non-empty string")

        year = item["year"]
        if not isinstance(year, int) or not 2018 <= year <= date.today().year:
            errors.append(f"{label}: year must be an integer from 2018 through {date.today().year}")

        if item["status"] not in STATUSES:
            errors.append(f"{label}: invalid status {item['status']!r}")
        if item["kind"] not in KINDS:
            errors.append(f"{label}: invalid kind {item['kind']!r}")
        if item["primary_omics"] not in PRIMARY_OMICS:
            errors.append(f"{label}: invalid primary_omics {item['primary_omics']!r}")

        omics = item["omics"]
        if not isinstance(omics, list) or not omics or not all(isinstance(value, str) for value in omics):
            errors.append(f"{label}: omics must be a non-empty string array")
        else:
            unknown = set(omics) - MODALITIES
            if unknown:
                errors.append(f"{label}: unknown omics values: {', '.join(sorted(unknown))}")
            if len(omics) != len(set(omics)):
                errors.append(f"{label}: omics contains duplicates")

        tags = item["tags"]
        if not isinstance(tags, list) or not all(isinstance(value, str) for value in tags):
            errors.append(f"{label}: tags must be a string array")
        else:
            unknown = set(tags) - TAGS
            if unknown:
                errors.append(f"{label}: unknown tags: {', '.join(sorted(unknown))}")
            if tags != sorted(set(tags)):
                errors.append(f"{label}: tags must be unique and alphabetically sorted")
            if item["status"] == "preprint" and "preprint" not in tags:
                errors.append(f"{label}: preprint records must include the preprint tag")
            if item["weights"] and "weights" not in tags and "api" not in tags:
                warnings.append(f"{label}: weights/API URL exists but no weights or api tag is present")

        for field in URL_FIELDS:
            value = item[field]
            if value is not None and (not isinstance(value, str) or not re.match(r"^https?://", value)):
                errors.append(f"{label}: {field} must be null or an HTTP(S) URL")
            elif live_links and value:
                link_targets.append((label, field, value))

        try:
            verified = date.fromisoformat(item["last_verified"])
            if verified > date.today():
                errors.append(f"{label}: last_verified cannot be in the future")
        except (TypeError, ValueError):
            errors.append(f"{label}: last_verified must be an ISO date")

    if live_links:
        # A catalog contains many independent URLs. Checking concurrently keeps the
        # optional audit practical while retaining stable, catalog-order output.
        with ThreadPoolExecutor(max_workers=16) as executor:
            results = executor.map(lambda target: check_url(target[2]), link_targets)
            for (label, field, value), (ok, detail) in zip(link_targets, results):
                if not ok:
                    errors.append(f"{label}: {field} link failed: {detail} — {value}")
                else:
                    print(f"link ok: {label}.{field} ({detail})")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-links",
        action="store_true",
        help="Perform a best-effort live HTTP check (slower and unsuitable for every CI run).",
    )
    args = parser.parse_args()

    records = load_catalog()
    errors, warnings = validate(records, live_links=args.check_links)

    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"Catalog invalid: {len(errors)} error(s), {len(warnings)} warning(s).", file=sys.stderr)
        return 1

    by_section = Counter(item["primary_omics"] for item in records)
    by_status = Counter(item["status"] for item in records)
    print(f"Catalog valid: {len(records)} models")
    print("Sections: " + ", ".join(f"{key}={by_section[key]}" for key in sorted(by_section)))
    print("Status: " + ", ".join(f"{key}={by_status[key]}" for key in sorted(by_status)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
