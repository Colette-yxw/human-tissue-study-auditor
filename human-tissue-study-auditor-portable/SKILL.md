---
name: human-tissue-study-auditor-portable
description: Audit Excel/CSV omics-study inventories to identify experiments that directly measure a target disease in human tissue or native human biospecimens. Use for row-by-row screening, evidence quoting, repository/publication verification, exclusion of cell lines, cultured or perturbed primary cells, explants, organoids, animal models, and delivery of a source-backed audit table or workbook.
---

# Human Tissue Study Auditor

Apply a strict, reproducible screen. Do not select studies merely because the title contains the disease name, “human,” “primary,” or an anatomical term.

Read these files before classification:

- [references/decision-rules.md](references/decision-rules.md)
- [references/output-contract.md](references/output-contract.md)
- [references/platform-use.md](references/platform-use.md) when the model does not support native skills or file tools.

## Core invariant

Mark `YES/☑` only when both gates pass:

1. **Disease gate:** the measured cohort, tissue state, or comparison directly concerns the target disease.
2. **Material gate:** the measured RNA/omics state came from human tissue or a native human biospecimen and existed in vivo before collection.

If either gate fails or remains unproven, mark `NO/☐`.

## Workflow

1. **Inspect before editing**
   - Identify the exact source sheet and whether each row represents a project, study, sample, or experiment.
   - Preserve all source values, sheets, identifiers, and formatting.
   - Render or preview the source sheet when possible.
   - Copy the source sheet to `Audit_Results`.

2. **Define the target**
   - Record the exact disease and whether native blood, PBMC, BAL, CSF, sputum, swabs, or freshly sorted cells are eligible.
   - Unless the user narrows the scope, treat native human biospecimens as eligible.

3. **Read every row as a unit**
   - Read title, abstract, overall design, organism, tissue, source name, cell type, treatment, sample characteristics, protocols, and accessions together.
   - Classify disease relevance independently from study type.
   - Describe the research subject with a short precise phrase; retain multi-word concepts.

4. **Build a candidate set**
   - Collect explicit disease cases, disease subtypes, lesional/non-lesional samples, treatment-response cohorts, and mixed studies containing a disease arm.
   - Also collect deceptive mentions where the disease may be background only.

5. **Re-review every candidate**
   - Search the accession and exact title in an official repository.
   - Prefer sample-level metadata and extraction/treatment protocols, then overall design, then the original paper.
   - Determine whether sequencing occurred directly or after culture, passage, differentiation, incubation, infection, stimulation, transfection, knockdown, or drug treatment.
   - Inspect the complete sample set before claiming the target tissue is absent.

6. **Handle row granularity correctly**
   - For a project-level row, a separately identifiable qualifying human-tissue arm can justify inclusion; explicitly state which arm qualifies and which arms do not.
   - For a sample-level row, judge only that sample. Do not rescue a cultured sample because the larger project also contains tissue.

7. **Capture decisive evidence**
   - Quote one or two complete, verbatim passages proving the decisive fact.
   - For `YES`, prove disease, human material, and direct collection/extraction.
   - For `NO`, prove the decisive failure: wrong disease, wrong material, culture, perturbation, animal model, organoid, or insufficient handling evidence.
   - Never use generated ellipses, paraphrases, mechanically joined fields, or a general disease-background sentence as evidence.

8. **Populate every audit field**
   - Fill classification, evidence, location, tissue type, and personalized explanation for every row.
   - Never output `NA` as normalized tissue type; use `Not reported / unclear` only after checking all available sources.
   - Match publications conservatively. Leave DOI/PMID/title blank rather than guessing.

9. **Run the consistency gate**
   - Recheck all `YES` rows and every disease-relevant `NO`.
   - Confirm evidence is verbatim and actionable.
   - Confirm study type, tissue type, quote, and explanation refer to the same measured material.
   - Confirm no `YES` row contains post-collection culture or perturbation unless a separate direct-tissue arm is explicitly identified at project level.
   - Run `scripts/validate_audit.py` on a CSV export when possible.

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
- Do not invent missing handling details.
- Do not infer “cultured” merely from `primary` or `cells`.
- Do not infer direct tissue merely from `patient-derived`.
- Lower confidence and keep unchecked when decisive evidence remains unavailable.
