# Human Tissue Study Auditor

Evidence-backed audit skill for screening Excel/CSV omics-study inventories and
identifying experiments that directly measure native human tissue or biospecimens
associated with a target disease.

The skill separates direct human tissue from cell lines, cultured primary cells,
organoids, animal models, ex-vivo perturbation experiments, and studies concerning
the wrong disease or anatomical site. It also requires traceable evidence quotes,
publication matching, row-specific explanations, and classification consistency
checks.

## Repository structure

```text
audit-human-disease-tissue-studies/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── decision-rules.md
    └── output-schema.md
```

## Install in Codex

Ask Codex:

```text
$skill-installer install https://github.com/Colette-yxw/human-tissue-study-auditor/tree/main/audit-human-disease-tissue-studies
```

Start a new task after installation, then invoke:

```text
Use $audit-human-disease-tissue-studies to audit this workbook for experiments
that directly measure human tissue associated with [target disease].
```

## Install in Hermes Agent

Hermes supports `SKILL.md` packages and referenced support files. Install from the
raw GitHub URL:

```bash
hermes skills install \
  https://raw.githubusercontent.com/Colette-yxw/human-tissue-study-auditor/main/audit-human-disease-tissue-studies/SKILL.md \
  --name audit-human-disease-tissue-studies
```

Start a new Hermes session, or use `--now` if supported by the installed Hermes
version.

### Hermes compatibility note

The scientific decision rules and evidence-audit workflow are portable. The Codex
version expects the Codex spreadsheet skill and `@oai/artifact-tool` for `.xlsx`
authoring and rendering. Hermes can apply the audit logic, but automated workbook
editing requires an Excel-capable tool or a separate Hermes spreadsheet workflow.

## Core safeguards

- `primary human tumor` is not treated as `primary human cells`.
- Freshly isolated cells are not described as cultured without direct evidence.
- Treatment administered to a patient is distinguished from ex-vivo sample treatment.
- Culture, passage, transfection, stimulation, infection, or drug-treatment claims
  require explicit source evidence.
- Direct human tissue from the wrong disease remains classified as direct tissue and
  is excluded for disease mismatch, not through an invented handling reason.
- Study type, tissue type, evidence quote, and explanation must describe the same
  experimental material.

## Access

This repository is public. Feel free to download it.
