---
name: human-tissue-study-auditor-portable
description: Audit Excel/CSV omics-study inventories to identify experiments that directly measure a target disease in human tissue or native human biospecimens. Use for row-by-row screening, evidence quoting, repository/publication verification, exclusion of cell lines, cultured or perturbed primary cells, explants, organoids, animal models, and delivery of a source-backed audit table or workbook.
---

# Human Tissue Study Auditor

Apply a strict, reproducible screen. Do not select studies merely because the title contains the disease name, “human,” “primary,” or an anatomical term.

Read these files before classification:

- [references/decision-rules.md](references/decision-rules.md)
- [references/output-contract.md](references/output-contract.md)
- [references/intermediate-record.md](references/intermediate-record.md)
- [references/platform-use.md](references/platform-use.md) when the model does not support native skills or file tools.

## Core invariant

Mark `YES/☑` only when both gates pass:

1. **Disease gate:** the measured cohort, tissue state, or comparison directly concerns the target disease.
2. **Material gate:** the measured RNA/omics state came from human tissue or a native human biospecimen and existed in vivo before collection.

If either gate fails or remains unproven, mark `NO/☐`.

## Row preservation invariant

- Lock the source scope before reading candidates. Record `source workbook`, exact
  `source sheet`, header row, first/last data row, data-row count, and stable row key.
- If the user names a sheet, use that exact sheet. Do not silently substitute a wider
  sheet such as `Expanded_Data` or a narrower prefiltered sheet.
- If the user says “entire dataset” and no sheet is named, use the workbook's complete
  project inventory rather than a prefiltered subset. Report the selected sheet and
  row count before classification.
- If several sheets could reasonably be the source, do not mix them. Choose only after
  comparing their purposes and row counts; state the choice in the delivery summary.
- Preserve every source data row exactly once, in the original order.
- Require `Audit_Results data-row count == source data-row count` before export.
- Never pre-filter, delete, deduplicate, collapse, or omit rows before or during classification.
- Keep obvious cell-line, animal, organoid, wrong-disease, and irrelevant rows. Mark them `NO/☐` and document the exclusion.
- Preserve every original column and value. Add audit columns only.
- Treat any row-count mismatch, missing source identifier, duplicated source row, or reordered row as a failed audit that must not be delivered.

## Workflow

1. **Inspect before editing**
   - Identify the exact source sheet and whether each row represents a project, study, sample, or experiment.
   - Record the source data-row count excluding the header, the total used-row count including the header, and a stable row key such as source row number plus accession/sample identifier.
   - Preserve all source values, sheets, identifiers, and formatting.
   - Render or preview the source sheet when possible.
   - Copy the complete source sheet to `Audit_Results` before classification. Do not create `Audit_Results` from a filtered candidate subset.

2. **Define the target**
   - Record the exact disease and whether native blood, PBMC, BAL, CSF, sputum, swabs, or freshly sorted cells are eligible.
   - Unless the user narrows the scope, treat native human biospecimens as eligible.

3. **Run the two-gate verification for every row**
   - Read title, abstract, overall design, organism, tissue, source name, cell type, treatment, sample characteristics, protocols, and accessions together.
   - Answer `Disease Gate: PASS/FAIL` with a short evidence-backed reason.
   - Answer `Material Gate: PASS/FAIL/UNPROVEN` with the measured material and post-collection handling.
   - Set `☑` only for `PASS + PASS`; all other combinations must be `☐`.
   - Create the mandatory structured gate record defined in
     `references/intermediate-record.md` before writing the final row. Do not rely on
     keyword impressions or prose such as “after full-field search.”
   - Before setting Disease Gate to `FAIL` or `UNPROVEN`, search every source field for
     the target disease name, abbreviation, spelling variants, and relevant subtype.
     Record which fields matched. Never declare disease evidence absent while the title,
     abstract, description, overall design, diagnosis, phenotype, or sample
     characteristics explicitly names a target-disease patient group.
   - A disease keyword match is a retrieval trigger, not automatic inclusion. Decide
     whether it names the measured cohort or only background context.
   - Before setting Material Gate to `PASS`, run a handling-conflict sweep across every
     field for `in vitro`, `culture`, `passage`, `Th0`, `co-culture`, `stimulation`,
     `treatment`, `vehicle`, `mock`, `infection`, `transfection`, `knockdown`,
     `differentiation`, and equivalent terms. Resolve every hit explicitly.
   - Classify disease relevance independently from study type and material handling.
   - Describe the research subject with a short precise phrase; retain multi-word concepts.

4. **Build a candidate set**
   - Collect explicit disease cases, disease subtypes, lesional/non-lesional samples, treatment-response cohorts, and mixed studies containing a disease arm.
   - Also collect deceptive mentions where the disease may be background only.

5. **Re-review every candidate**
   - Search the accession and exact title in an official repository.
   - Prefer sample-level metadata and extraction/treatment protocols, then overall design, then the original paper.
   - Determine whether sequencing occurred directly or after culture, passage, differentiation, incubation, infection, stimulation, transfection, knockdown, or drug treatment.
   - Inspect the complete sample set before claiming the target tissue is absent.
   - Apply evidence precedence: sample-level `cell source`, `conditions`, `treatment`,
     culture/passaging and extraction fields override a disease-rich title or abstract.
     For example, `cell source;;in vitro | conditions;;Th0` fails the material gate even
     if the title says “expanded in SLE blood.”

6. **Handle row granularity correctly**
   - Assign every row `project`, `study`, `sample`, or `experiment` granularity before
     applying either gate.
   - For a project-level row, a separately identifiable qualifying human-tissue arm can justify inclusion; explicitly state which arm qualifies and which arms do not.
   - For a sample-level row, judge only that sample. Do not rescue a cultured sample because the larger project also contains tissue.
   - For project/study rows, enumerate every independent dataset/arm named in title,
     abstract, overall design, sample list, or official record. A representative
     sample's `treatment`, `diagnosis`, or `conditions` must not overwrite other arms.

7. **Capture decisive evidence**
   - Quote one or two complete, verbatim passages proving the decisive fact.
   - For `YES`, prove disease, human material, and direct collection/extraction.
   - For `NO`, prove the decisive failure: wrong disease, wrong material, culture, perturbation, animal model, organoid, or insufficient handling evidence.
   - Never use generated ellipses, paraphrases, mechanically joined fields, or a general disease-background sentence as evidence.
   - Do not write `...` or `…` anywhere in an evidence quote. Do not join non-contiguous
     passages with ellipses. Put two separately quoted passages on separate lines and
     give each its own source field/location.
   - For workbook evidence, verify programmatically that every quoted passage is an
     exact substring of an original source cell. For website evidence, save the exact
     URL, accession, section/field, and retrieved passage used for verification.

8. **Populate every audit field**
   - Fill `Research subject`, `Disease relevance`, `Study type`, `Confidence`, evidence quote, evidence location, tissue type, and personalized explanation for every row, including every `NO/☐` row.
   - Make each personalized explanation state both gate results in prose: whether the disease gate passed and whether the material gate passed.
   - Do not leave required audit fields blank merely because a row is excluded.
   - Never output `NA` as normalized tissue type; use `Not reported / unclear` only after checking all available sources.
   - Match publications conservatively. Leave DOI/PMID/title blank rather than guessing.
   - Never fill missing publication fields with `NA`, and never copy a study title or
     abstract fragment into `Publication title` unless a publication match is proven.
   - Do not reuse an identical generic exclusion explanation across unrelated rows.
     Every claimed culture, stimulation, induction, treatment, or cell-line step must
     be supported by that row's evidence.

9. **Run the consistency gate**
   - Recount rows and verify one-to-one correspondence with the source before any other QC.
   - Compare stable row keys and source-column values to ensure no row was deleted, duplicated, reordered, or altered.
   - Recheck all `YES` rows and every disease-relevant `NO`.
   - Confirm evidence is verbatim and actionable.
   - Confirm study type, tissue type, quote, and explanation refer to the same measured material.
   - Flag `Disease relevance = direct` + direct human tissue/biospecimen study type +
     `Checkbox = ☐` as a decision contradiction unless the material gate is explicitly
     unresolved and the study type is changed to `Unclear/other`.
   - Confirm no `YES` row contains post-collection culture or perturbation unless a separate direct-tissue arm is explicitly identified at project level.
   - Run a disagreement audit: list all rows where disease evidence contains the target
     term but Disease Gate is not `PASS`, and all checked rows containing any handling
     conflict term. Manually resolve every listed row before export.
   - Report publication metadata coverage (`matched title/DOI/PMID counts`). Blank is
     preferable to guessing, but do not skip the official-record/publication search for
     possible inclusions.
   - Run `scripts/validate_audit.py` on a CSV export with `--source-csv` or `--expected-rows` when possible.
   - Always pass `--gate-records` and `--target-terms` for a disease audit. Treat any
     validation error as a stop condition, not a warning.

10. **Deliver**
    - Preserve the source workbook.
    - Freeze the header, enable filters, wrap long audit fields, and visibly highlight checked rows without relying on color alone.
    - Report total rows, number retained, major exclusion categories, and the output path.

## Explanation rule

For `YES`, explain:

1. what was measured;
2. how it was collected;
3. why the disease state existed in vivo before collection;
4. why it is not a cell-line, culture, organoid, animal, or ex-vivo perturbation model;
5. the final retention decision.

For `NO`, name the actual model/material and the decisive exclusion reason. Do not write a generic “not relevant” sentence.

## Stop conditions

- Do not include an ambiguous row to increase recall.
- Do not deliver if source and audit row counts differ.
- Do not deliver if the structured gate-record count differs from the source row count.
- Do not deliver with unresolved disease-alias or handling conflicts.
- Do not deliver when a target alias is present but its exact field and passage are
  absent from the gate record.
- Do not deliver a project/study row with multiple datasets/arms unless qualifying and
  excluded arms were enumerated.
- Do not deliver when a local quote fails exact per-passage substring validation.
- Do not deliver when an identical personalized explanation appears on more than two rows.
- Do not invent missing handling details.
- Do not infer “cultured” merely from `primary` or `cells`.
- Do not infer direct tissue merely from `patient-derived`.
- Lower confidence and keep unchecked when decisive evidence remains unavailable.
