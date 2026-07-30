#!/usr/bin/env python3
"""Validate a CSV export produced by the Human Tissue Study Auditor."""

import argparse
import csv
import re
import sys
from collections import Counter
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

HANDLING_CONFLICT = re.compile(
    r"\bin vitro\b|cultured?|passages?|passaged|th0|co-?culture|stimulat(?:ed|ion)|"
    r"treat(?:ed|ment)|vehicle|mock|infect(?:ed|ion)|transfect(?:ed|ion)|"
    r"knockdown|differentiat(?:ed|ion)|incubat(?:ed|ion)",
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
    parser.add_argument(
        "--target-terms",
        help="Comma-separated target-disease aliases used for disease-conflict checks.",
    )
    parser.add_argument(
        "--strict-local-quotes",
        action="store_true",
        help="Require every evidence quote to occur verbatim in one original source cell.",
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

    source_rows = []
    source_headers = []
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
        if not quote or "..." in quote or "…" in quote:
            errors.append(f"row {number}: missing, spliced, or truncated evidence quote")
        if not explanation:
            errors.append(f"row {number}: blank personalized explanation")
        if checkbox == "☑" and relevance != "direct":
            errors.append(f"row {number}: checked row is not disease-direct")
        if (
            checkbox == "☐"
            and relevance == "direct"
            and re.search(r"human (?:tissue|biospecimen) \(direct\)", study_type, re.I)
        ):
            errors.append(
                f"row {number}: decision contradiction — disease is direct and study type is direct human material, but checkbox is NO"
            )
        if checkbox == "☑" and PERTURBED.search(study_type):
            if not study_type.lower().startswith("mixed direct human tissue"):
                errors.append(f"row {number}: checked row classified as cultured/perturbed")

        if source_rows and number - 2 < len(source_rows):
            source_row = source_rows[number - 2]
            source_text = " | ".join(source_row.get(name, "") for name in source_headers)
            if args.strict_local_quotes and quote:
                if not any(quote in source_row.get(name, "") for name in source_headers):
                    errors.append(
                        f"row {number}: evidence quote is not an exact substring of any original source cell"
                    )
            if checkbox == "☑":
                conflict = HANDLING_CONFLICT.search(source_text)
                if conflict:
                    resolved = re.search(
                        r"\bin vivo\b|clinical trial|patient treatment|separate(?:ly)? "
                        r"(?:identifiable )?(?:arm|dataset)|mixed",
                        explanation,
                        re.I,
                    )
                    if not resolved:
                        errors.append(
                            f"row {number}: checked row has unresolved handling-conflict term "
                            f"'{conflict.group(0)}'"
                        )

            if args.target_terms:
                aliases = [
                    term.strip()
                    for term in args.target_terms.split(",")
                    if term.strip()
                ]
                disease_hit = next(
                    (term for term in aliases if term.lower() in source_text.lower()),
                    None,
                )
                if disease_hit and relevance != "direct":
                    resolved_background = re.search(
                        r"background|背景|仅.{0,8}(?:提及|相关)|not (?:the )?"
                        r"(?:measured|study|patient|cohort)|wrong disease",
                        explanation,
                        re.I,
                    )
                    if not resolved_background:
                        errors.append(
                            f"row {number}: target term '{disease_hit}' occurs in source, "
                            "but disease relevance is not direct and background status is unresolved"
                        )

        for field in ("Publication title", "Publication URL", "DOI", "PMID"):
            if row.get(field, "").strip().lower() in {"na", "n/a", "unknown"}:
                errors.append(
                    f"row {number}: use blank, not '{row.get(field)}', for unmatched {field}"
                )

    duplicate_explanations = Counter(
        row.get("Personalized explanation (YES rows re-reviewed)", "").strip()
        for row in rows
        if row.get("Personalized explanation (YES rows re-reviewed)", "").strip()
    )
    for explanation_text, count in duplicate_explanations.items():
        if count > 2:
            errors.append(
                f"generic explanation reuse: identical personalized explanation appears {count} times"
            )

    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK: {len(rows)} rows passed structural consistency checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
