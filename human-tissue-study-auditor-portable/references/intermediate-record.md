# Mandatory intermediate gate record

Create one record for every locked source row before writing `Audit_Results`. Save the
records as JSON or CSV and pass them to `scripts/validate_audit.py --gate-records`.

## Required JSON schema

```json
[
  {
    "source_row": 2,
    "source_key": "SRP000001",
    "granularity": "project",
    "disease_alias_hits": [
      {
        "alias": "SLE",
        "field": "study_abstract",
        "passage": "Complete verbatim sentence containing the alias.",
        "role": "measured_cohort"
      }
    ],
    "disease_gate": "PASS",
    "material_gate": "PASS",
    "handling_conflicts": [
      {
        "term": "treatment",
        "field": "study_abstract",
        "passage": "Complete verbatim handling passage.",
        "resolution": "patient_in_vivo_treatment"
      }
    ],
    "qualifying_arms": [
      "dataset2: freshly sorted cells from 10 SLE patients"
    ],
    "excluded_arms": [
      "dataset1: in-vitro Th0 cells"
    ],
    "final_checkbox": "☑"
  }
]
```

## Controlled values

- `granularity`: `project`, `study`, `sample`, or `experiment`
- disease hit `role`: `measured_cohort`, `background`, or `unclear`
- `disease_gate`: `PASS` or `FAIL`
- `material_gate`: `PASS`, `FAIL`, or `UNPROVEN`
- handling `resolution`: `ex_vivo_exclusion`, `patient_in_vivo_treatment`,
  `separate_nonqualifying_arm`, `background_only`, or `unresolved`
- `final_checkbox`: `☑` only for `PASS + PASS`; otherwise `☐`

## Disease alias rule

Search every original source field separately. For every target-disease alias hit,
store the exact field name and complete verbatim passage. If Disease Gate is not
`PASS`, every hit must be classified as `background`; `unclear` is unresolved and
blocks export. Merely writing “after full-field search” is invalid.

## Project/study granularity rule

For `project` and `study` rows:

1. parse all independent datasets/arms from the overall design and complete sample set;
2. populate both `qualifying_arms` and `excluded_arms` when the project is mixed;
3. never let one representative sample override other explicitly described arms;
4. allow inclusion when a separately identifiable arm passes both gates.

For `sample` and `experiment` rows, judge only that row and leave unrelated project
arms out of the decision.

## Conflict completion rule

Record every handling-conflict match with its field, verbatim passage, and resolution.
Export is forbidden when any resolution is `unresolved`.

The gate record is an auditable verification artifact. It is not a request to reveal
private hidden reasoning.
