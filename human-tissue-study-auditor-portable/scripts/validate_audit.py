#!/usr/bin/env python3
"""Validate a CSV export produced by the Human Tissue Study Auditor."""

import argparse
import csv
import json
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

GRANULARITIES = {"project", "study", "sample", "experiment"}
DISEASE_GATES = {"PASS", "FAIL"}
MATERIAL_GATES = {"PASS", "FAIL", "UNPROVEN"}
HIT_ROLES = {"measured_cohort", "background", "unclear"}
HANDLING_RESOLUTIONS = {
    "ex_vivo_exclusion",
    "patient_in_vivo_treatment",
    "separate_nonqualifying_arm",
    "background_only",
    "unresolved",
}


def load_gate_records(path):
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("gate-record JSON must be a list")
        return data
    with path.open(encoding="utf-8-sig", newline="") as handle:
        records = list(csv.DictReader(handle))
    for record in records:
        for field in (
            "disease_alias_hits",
            "handling_conflicts",
            "qualifying_arms",
            "excluded_arms",
        ):
            value = record.get(field, "")
            if value:
                record[field] = json.loads(value)
            else:
                record[field] = []
    return records


def quote_passages(quote):
    passages = []
    for line in re.split(r"\r?\n+", quote):
        line = line.strip().strip("\"'“”")
        line = re.sub(r"^[-•]\s*", "", line)
        if line:
            passages.append(line)
    return passages


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
    parser.add_argument(
        "--gate-records",
        type=Path,
        help="Mandatory JSON/CSV structured gate records for a full disease audit.",
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

    gate_records = []
    gate_by_row = {}
    if args.gate_records:
        try:
            gate_records = load_gate_records(args.gate_records)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"cannot read gate records: {exc}")
        if gate_records and len(gate_records) != len(rows):
            errors.append(
                "gate-record preservation failure: "
                f"audit has {len(rows)} rows, gate records have {len(gate_records)}"
            )
        for record in gate_records:
            try:
                source_row = int(record.get("source_row"))
            except (TypeError, ValueError):
                errors.append("gate record has invalid source_row")
                continue
            if source_row in gate_by_row:
                errors.append(f"duplicate gate record for source row {source_row}")
            gate_by_row[source_row] = record

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
                for passage in quote_passages(quote):
                    if not any(
                        passage in source_row.get(name, "") for name in source_headers
                    ):
                        errors.append(
                            f"row {number}: evidence passage is not an exact substring "
                            f"of any original source cell: {passage[:120]}"
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

            if args.gate_records:
                record = gate_by_row.get(number)
                if not record:
                    errors.append(f"row {number}: missing structured gate record")
                else:
                    granularity = str(record.get("granularity", "")).strip().lower()
                    disease_gate = str(record.get("disease_gate", "")).strip().upper()
                    material_gate = str(record.get("material_gate", "")).strip().upper()
                    record_checkbox = str(record.get("final_checkbox", "")).strip()
                    disease_hits = record.get("disease_alias_hits") or []
                    handling_hits = record.get("handling_conflicts") or []
                    qualifying_arms = record.get("qualifying_arms") or []
                    excluded_arms = record.get("excluded_arms") or []

                    if granularity not in GRANULARITIES:
                        errors.append(f"row {number}: invalid gate-record granularity")
                    if disease_gate not in DISEASE_GATES:
                        errors.append(f"row {number}: invalid disease_gate")
                    if material_gate not in MATERIAL_GATES:
                        errors.append(f"row {number}: invalid material_gate")
                    expected_checkbox = (
                        "☑"
                        if disease_gate == "PASS" and material_gate == "PASS"
                        else "☐"
                    )
                    if record_checkbox != expected_checkbox or checkbox != expected_checkbox:
                        errors.append(
                            f"row {number}: gate-record decision does not match PASS+PASS rule"
                        )
                    if (disease_gate == "PASS") != (relevance == "direct"):
                        errors.append(
                            f"row {number}: disease_gate and Disease relevance disagree"
                        )

                    source_key = str(record.get("source_key", "")).strip()
                    if not source_key:
                        errors.append(f"row {number}: blank gate-record source_key")
                    elif source_key not in {
                        str(source_row.get(name, "")).strip() for name in source_headers
                    }:
                        errors.append(
                            f"row {number}: gate-record source_key not found in source row"
                        )

                    for hit in disease_hits:
                        field = str(hit.get("field", "")).strip()
                        alias = str(hit.get("alias", "")).strip()
                        passage = str(hit.get("passage", "")).strip()
                        role = str(hit.get("role", "")).strip()
                        if field not in source_headers:
                            errors.append(
                                f"row {number}: disease hit uses unknown field '{field}'"
                            )
                            continue
                        if not passage or passage not in source_row.get(field, ""):
                            errors.append(
                                f"row {number}: disease-hit passage is not verbatim in field '{field}'"
                            )
                        if not alias or alias.lower() not in passage.lower():
                            errors.append(
                                f"row {number}: disease-hit passage does not contain its alias"
                            )
                        if role not in HIT_ROLES:
                            errors.append(f"row {number}: invalid disease-hit role")
                        if disease_gate == "FAIL" and role != "background":
                            errors.append(
                                f"row {number}: non-PASS disease hit is not resolved as background"
                            )

                    if args.target_terms:
                        aliases = [
                            term.strip()
                            for term in args.target_terms.split(",")
                            if term.strip()
                        ]
                        for field in source_headers:
                            value = source_row.get(field, "")
                            for alias in aliases:
                                if alias.lower() in value.lower():
                                    covered = any(
                                        str(hit.get("field", "")).strip() == field
                                        and str(hit.get("alias", "")).strip().lower()
                                        == alias.lower()
                                        and str(hit.get("passage", "")).strip() in value
                                        for hit in disease_hits
                                    )
                                    if not covered:
                                        errors.append(
                                            f"row {number}: target alias '{alias}' in field "
                                            f"'{field}' is absent from the gate record"
                                        )

                    handling_fields = {
                        field
                        for field in source_headers
                        if HANDLING_CONFLICT.search(source_row.get(field, ""))
                    }
                    recorded_handling_fields = {
                        str(hit.get("field", "")).strip() for hit in handling_hits
                    }
                    for field in sorted(handling_fields - recorded_handling_fields):
                        errors.append(
                            f"row {number}: handling conflict in field '{field}' is absent "
                            "from the gate record"
                        )
                    for hit in handling_hits:
                        field = str(hit.get("field", "")).strip()
                        passage = str(hit.get("passage", "")).strip()
                        resolution = str(hit.get("resolution", "")).strip()
                        if field not in source_headers:
                            errors.append(
                                f"row {number}: handling hit uses unknown field '{field}'"
                            )
                            continue
                        if not passage or passage not in source_row.get(field, ""):
                            errors.append(
                                f"row {number}: handling passage is not verbatim in field '{field}'"
                            )
                        if resolution not in HANDLING_RESOLUTIONS:
                            errors.append(f"row {number}: invalid handling resolution")
                        if resolution == "unresolved":
                            errors.append(
                                f"row {number}: unresolved handling conflict blocks export"
                            )

                    has_multiple_arms = re.search(
                        r"\b(?:dataset|arm)s?\b|independent datasets?",
                        source_text,
                        re.I,
                    )
                    if granularity in {"project", "study"} and has_multiple_arms:
                        if not qualifying_arms and not excluded_arms:
                            errors.append(
                                f"row {number}: project/study has multiple arms but none "
                                "were enumerated"
                            )
                        if disease_gate == "PASS" and handling_fields:
                            if not qualifying_arms or not excluded_arms:
                                errors.append(
                                    f"row {number}: mixed project requires both qualifying "
                                    "and excluded arm lists"
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
