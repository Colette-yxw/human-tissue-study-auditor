#!/usr/bin/env python3
"""Validate a CSV export produced by the Human Tissue Study Auditor."""

import argparse
import csv
import re
import sys
from pathlib import Path

REQUIRED = [
    "Checkbox",
    "Research subject",
    "Disease relevance",
    "Study type",
    "Confidence",
    "Original evidence quote",
    "Evidence location",
    "Personalized explanation (YES rows re-reviewed)",
    "Official source URL",
    "Publication title",
    "Tissue type",
    "Publication URL",
    "DOI",
    "PMID",
    "Publication match basis",
]

PERTURBED = re.compile(
    r"cultured|culture|passaged|transfected|stimulated|infected|incubated|"
    r"knockdown|differentiated|ex vivo/cultured|ex vivo/perturbed",
    re.I,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument(
        "--source-csv",
        type=Path,
        help="Optional source CSV. Enforces equal row count, order, and unchanged original columns.",
    )
    parser.add_argument(
        "--expected-rows",
        type=int,
        help="Expected number of audit data rows, excluding the header.",
    )
    args = parser.parse_args()

    with args.csv_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
        headers = handle.seek(0) or next(csv.reader(handle))

    errors = []
    missing = [name for name in REQUIRED if name not in headers]
    if missing:
        errors.append(f"missing columns: {', '.join(missing)}")

    if args.expected_rows is not None and len(rows) != args.expected_rows:
        errors.append(
            f"row preservation failure: expected {args.expected_rows} data rows, found {len(rows)}"
        )

    if args.source_csv:
        with args.source_csv.open(encoding="utf-8-sig", newline="") as handle:
            source_reader = csv.DictReader(handle)
            source_rows = list(source_reader)
            source_headers = source_reader.fieldnames or []
        if len(rows) != len(source_rows):
            errors.append(
                "row preservation failure: "
                f"source has {len(source_rows)} data rows, audit has {len(rows)}"
            )
        missing_source_columns = [name for name in source_headers if name not in headers]
        if missing_source_columns:
            errors.append(
                "audit is missing original columns: " + ", ".join(missing_source_columns)
            )
        for index, (source_row, audit_row) in enumerate(
            zip(source_rows, rows), start=2
        ):
            changed = [
                name
                for name in source_headers
                if source_row.get(name, "") != audit_row.get(name, "")
            ]
            if changed:
                errors.append(
                    f"row {index}: original values/order changed in columns "
                    + ", ".join(changed[:8])
                )

    required_nonblank = [
        "Research subject",
        "Disease relevance",
        "Study type",
        "Confidence",
        "Original evidence quote",
        "Evidence location",
        "Personalized explanation (YES rows re-reviewed)",
        "Tissue type",
        "Publication match basis",
    ]

    for number, row in enumerate(rows, start=2):
        checkbox = row.get("Checkbox", "").strip()
        relevance = row.get("Disease relevance", "").strip()
        confidence = row.get("Confidence", "").strip()
        tissue = row.get("Tissue type", "").strip()
        quote = row.get("Original evidence quote", "").strip()
        explanation = row.get("Personalized explanation (YES rows re-reviewed)", "").strip()
        study_type = row.get("Study type", "").strip()

        for field in required_nonblank:
            if not row.get(field, "").strip():
                errors.append(f"row {number}: blank required field '{field}'")
        if checkbox not in {"☑", "☐"}:
            errors.append(f"row {number}: invalid checkbox")
        if relevance not in {"direct", "no"}:
            errors.append(f"row {number}: invalid disease relevance")
        if confidence not in {"low", "moderate", "high"}:
            errors.append(f"row {number}: invalid confidence")
        if not tissue or tissue.upper() == "NA":
            errors.append(f"row {number}: missing/NA tissue type")
        if not quote or quote.endswith(("...", "…")):
            errors.append(f"row {number}: missing or truncated evidence quote")
        if not explanation:
            errors.append(f"row {number}: blank personalized explanation")
        if checkbox == "☑" and relevance != "direct":
            errors.append(f"row {number}: checked row is not disease-direct")
        if checkbox == "☑" and PERTURBED.search(study_type):
            if not study_type.lower().startswith("mixed direct human tissue"):
                errors.append(f"row {number}: checked row classified as cultured/perturbed")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK: {len(rows)} rows passed structural consistency checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
