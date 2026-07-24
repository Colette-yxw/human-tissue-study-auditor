---
name: audit-human-disease-tissue-studies
description: Audit Excel/CSV omics-study inventories to identify experiments that directly measure human tissue or native human biospecimens related to a target disease, excluding cell lines, cultured primary cells, organoids, animal models, and ex vivo perturbation experiments. Use when Codex must copy a source sheet into an audit sheet, classify every study, quote original evidence, verify repository and publication metadata, explain included rows, and deliver a source-backed `.xlsx` filter result.
---

# Audit Human Disease Tissue Studies

Apply a strict, reproducible screen for studies that measure disease-associated molecular states already present in human tissue or native biospecimens at collection.

## Required companion workflow

Use the available spreadsheet skill for workbook editing and verification. Browse authoritative sources for repository and publication matching. Keep the source workbook and source sheet unchanged.

Read:

- [references/decision-rules.md](references/decision-rules.md) before classifying rows.
- [references/output-schema.md](references/output-schema.md) before adding audit columns.

## Workflow

1. Inspect the workbook.
   - Identify the requested source sheet using its exact case-sensitive name.
   - Determine whether each row is a study, project, sample, or experiment.
   - Render the source sheet before editing and preserve its formatting.
   - Copy the source sheet to the requested audit-sheet name.

2. Define the target.
   - Extract the target disease from the user request.
   - Interpret “direct human tissue” using the decision rules.
   - State any user-specific expansion or restriction in the audit evidence, not only in formatting.

3. Screen every row using local evidence first.
   - Read title, abstract, description, organism, cell type, source name, treatment, tissue, sample attributes, and accession fields together.
   - Classify study type independently from disease relevance.
   - Do not infer direct tissue merely from words such as “human,” “primary,” “patient-derived,” or an anatomical tissue name.
   - Interpret `primary` from the noun it modifies. `Primary human tumor`,
     `primary tumor tissue`, and `primary human sample` can describe direct tissue;
     they do not mean `primary human cells`. Conversely, `primary fibroblasts` or
     `primary epithelial cells` describe cells and still require a handling review.
   - Select original evidence that directly proves the decisive classification fact;
     do not rewrite analysis as a quote.
   - Describe the research subject with the shortest precise phrase; do not force it to one word. Preserve combined concepts such as `Renal fibrosis`, `Idiopathic pulmonary fibrosis`, or `Kidney transplantation`.

4. Re-review every possible inclusion.
   - Search the project accession, sample accession, GEO/ArrayExpress/BioProject accession, and exact title.
   - Prefer official repository records, then the original paper or PubMed.
   - Read methods/overall design closely enough to determine whether RNA was extracted directly or after isolation, culture, differentiation, stimulation, drug treatment, knockdown, or infection.
   - Separate patient treatment from sample treatment. A biopsy, blood draw, or tissue
     collected before/after an in-vivo clinical therapy remains a direct human sample
     unless the sample itself was cultured or perturbed after collection.
   - A human tissue origin does not rescue a later culture or perturbation experiment.
   - When the user asks for a full row-by-row review, retrieve an official repository record for every project row, not only keyword-positive candidates. Record the official URL even when no publication is matched.
   - When excluding a disease-relevant study because its sequenced material is not the
     target tissue, inspect the complete sample list or overall design. Do not infer that
     the target tissue was absent from one representative sample.

5. Match publications conservatively.
   - Require an accession link, repository citation, exact sample/design match, or uniquely matching title and methods.
   - Do not populate DOI, PMID, or publication title from a merely related paper.
   - Explain the exact match basis in its own column.

6. Populate all requested audit columns.
   - Use `☑` only for rows satisfying both direct human-tissue status and direct target-disease relevance.
   - Use `☐` for all other rows.
   - Fill classification, evidence quote, and evidence location for every row.
   - Fill the personalized explanation for every row. For checked rows, explain why the
     direct human-tissue and target-disease criteria are satisfied. For unchecked rows,
     explain the decisive exclusion reason (wrong disease, wrong tissue, cultured or
     perturbed cells, organoid/iPSC model, animal model, reanalysis, or insufficient
     evidence). Never leave the entire explanation column blank merely because no rows
     qualified.
   - Use plain-text source URLs inside cells.
   - Never propagate `NA` into the normalized tissue-type output. Infer the tissue, biospecimen, cell model, or organism from all available row and official-source evidence. If the source truly does not report it, write `Not reported / unclear`.

7. Perform quality control.
   - Manually re-check all checked rows and all disease-relevant exclusions.
   - Check that no cultured/stimulated/treated samples are checked.
   - Verify that every quote occurs verbatim in the cited row or source.
   - Confirm that every quote proves the exact fact used in the decision; keyword overlap
     or general disease background is not sufficient.
   - Reject quotes cut off mid-sentence, quotes ending in generated ellipses, and
     title-plus-abstract strings produced by mechanical concatenation.
   - Check that `Study type`, `Tissue type`, the evidence quote, and the personalized
     explanation describe the same experimental material and handling.
   - Run a contradiction audit across every row. Flag any explanation that mentions
     culture, passage, transfection, stimulation, infection, differentiation, incubation,
     or drug treatment unless the cited quote or source explicitly proves that handling.
   - Never route `Freshly isolated human cells` through a generic `cell`/`culture`
     explanation branch merely because its label contains the word `cells`.
   - For every row classified as `Freshly isolated human cells`, explicitly determine
     whether the cells were sequenced immediately or underwent later culture/perturbation.
     If handling is not reported, do not invent it; lower confidence or use
     `Unclear/other` as appropriate.
   - Recheck phrases containing `primary human tumor`, `primary tumor`, `frozen specimen`,
     `resected tissue`, `surgical sample`, `biopsy`, `autopsy`, and `post-mortem tissue`
     for possible direct-tissue classification.
   - Confirm that identifiers remain text and DOI/PMID values are not corrupted.
   - Scan for formula errors, inspect key ranges, render the audit sheet, and export one final `.xlsx`.

## Explanation style for checked rows

Write the explanation in the user’s language. Cover:

1. What human tissue/biospecimen was measured.
2. How it was collected and whether RNA came directly from it.
3. Why the disease state existed in vivo before collection.
4. Why the experiment is not a cell-line, culture, organoid, animal, or ex vivo perturbation model.
5. A clear final retention statement.

Use this reasoning pattern, adapting it to the row:

> 该项目直接测量患者取得的[组织/样本]。[疾病相关状态]在样本取下前已经于受试者体内形成；RNA读取的是这一既存状态，不是把细胞或组织取出后通过培养、刺激或药物处理制造该表型，因此保留 YES。

## Explanation style for excluded rows

Give every excluded row a concise, row-specific explanation in the user’s language.
Name the actual tissue/model and research subject, identify the decisive failure, and
finish with a clear exclusion statement. Distinguish:

- correct disease but cultured/perturbed material;
- direct human tissue but wrong disease or anatomical site;
- animal, cell-line, organoid/iPSC, or public-data models;
- insufficient evidence for direct human target-disease tissue.

Do not use a generic sentence that merely repeats `NO`.

## Confidence

- `high`: explicit sample type and handling evidence, plus authoritative source confirmation.
- `moderate`: classification is strongly indicated but one handling detail or publication match is incomplete.
- `low`: organism, sample identity, handling, or disease relationship remains ambiguous.

Never use confidence to turn an ambiguous row into an inclusion. Ambiguous rows remain unchecked.

## Original evidence standard

Treat the evidence column as an auditable proof chain, not a search-result snippet.

1. Identify the decisive claim before selecting a quote.
   - For inclusion: prove the target disease, human status, target tissue/biospecimen,
     and direct extraction without later culture or perturbation.
   - For exclusion: prove the single decisive failure, such as wrong organ/disease,
     cell line, culture/passaging, transfection/treatment, organoid, animal model, or
     absence of the target tissue from the sequenced sample set.

2. Prefer sources in this order:
   - sample-level `Source name`, `Characteristics`, extraction/culture protocol, and
     treatment fields;
   - official repository overall design and complete sample list;
   - publication Methods or Supplementary sample table;
   - official study description;
   - workbook row fields.

3. Use a study title alone only when it explicitly proves the decisive wrong disease,
   wrong organ, cell line, or model. A title is not sufficient to establish sample
   handling or direct tissue extraction.

4. Quote one or two complete, compact original passages. Preserve wording exactly.
   Never:
   - truncate at a fixed character count;
   - end a quote with `...` or `…` generated by the audit;
   - splice non-contiguous fragments into a sentence;
   - present a paraphrase, normalized tissue label, or absence inference as a quote.

5. Handle negative evidence explicitly.
   - Absence cannot be proved by quoting an omitted item.
   - Inspect the complete sample list/overall design and cite that location.
   - Quote the passages that identify the actual sequenced materials.
   - State in the personalized explanation that the lack of target tissue is an
     inference from the complete enumerated sample set.

6. Make `Evidence location` independently actionable. Include the accession, exact
   page section or field, sample accession when applicable, and direct URL for
   sample-level evidence.

7. Verify each quote programmatically or manually as an exact substring of the cited
   source. If decisive evidence remains unavailable, do not make a stronger claim:
   leave the row unchecked, lower confidence, and state that direct target-tissue
   status is unproven.

## Classification–explanation consistency gate

Before export, apply these non-negotiable checks:

- `Human tissue (direct)`: describe the actual tissue and collection evidence. Do not
  call it cultured merely because the source uses `primary human samples`.
- `Human biospecimen (direct)`: distinguish native blood, PBMC, BAL, CSF, brushing,
  plasma, urine, and similar samples from cell culture. Clinical treatment before
  collection is not ex-vivo perturbation.
- `Freshly isolated human cells`: state only that cells were isolated/sorted and
  sequenced without documented later manipulation. Do not mention culture, passage,
  transfection, stimulation, or drug treatment without evidence.
- `Primary human cells (ex vivo/cultured[/perturbed])`: require explicit handling
  evidence such as culture duration, passage, medium, differentiation, incubation,
  vehicle, stimulation, transfection, infection, or treatment after collection.
- If the sample type is direct human tissue but the disease is wrong, retain the direct
  tissue classification and exclude for disease mismatch. Do not manufacture a
  handling-based exclusion reason.
- If classification and disease relevance fail for different reasons, name both
  accurately, but make the decisive exclusion reason clear.
