# Decision rules

## Inclusion rule

Check a row only when both conditions are satisfied:

1. The measured RNA/omics material came directly from human tissue or a native human biospecimen.
2. The study directly investigates the target disease, its patient phenotype, or disease-associated tissue state.

“Directly” means the molecular state existed in vivo before collection and was not subsequently manufactured by culture, differentiation, stimulation, infection, genetic manipulation, or drug treatment.

Interpret words in context:

- `primary human kidney tumor`, `primary tumor tissue`, and `primary human sample`
  may be direct human tissue.
- `primary fibroblasts`, `primary epithelial cells`, and similar phrases describe
  cells; review their post-isolation handling separately.
- Never classify a sample as cultured merely because `primary` or `cells` appears.

## Include

- Surgical or biopsy tissue with RNA extracted from the tissue.
- Fresh/frozen/resected/autopsy/transplant human tissue measured without culture.
- Native blood, whole blood, sputum, BAL/BALF, brushing, swab, or lavage when the user treats these as eligible human biospecimens.
- Freshly sorted or isolated cells only when RNA is extracted immediately and the user’s scope includes native tissue-derived cell fractions.
- Tissue or native biospecimens collected before or after an in-vivo clinical treatment,
  when no ex-vivo manipulation occurs before RNA extraction.

## Exclude

- Immortalized or transformed cell lines.
- Primary human cells expanded, passaged, maintained, differentiated, or cultured before measurement.
- Patient-derived cells treated with vehicle, drug, cytokine, LPS, smoke extract, pathogen, siRNA, CRISPR, transfection, hypoxia, or another perturbation before RNA extraction.
- Organoids, air–liquid interface cultures, iPSC-derived cells, reconstructed tissue, decellularized scaffolds, explant cultures, and co-cultures.
- Animal models, xenografts, and cross-species studies unless an independently qualifying human-tissue arm is represented by the audited row.
- In silico reanalysis without new human-tissue measurements, unless the user explicitly includes public-data reanalysis.
- Studies where the target disease is only background context, a cited application, a risk locus mention, or a possible downstream relevance.

## Important boundary examples

### Primary human kidney tumors; frozen specimen

Classify as `Human tissue (direct)` when the record identifies primary human tumors
and frozen/resected/biopsy tissue without later culture. `Primary` modifies `tumors`;
it does not mean freshly isolated primary cells.

### Freshly isolated or sorted human cells

Classify as `Freshly isolated human cells` only when the cells are directly isolated
or sorted and sequenced without documented later manipulation. Do not describe them
as cultured, passaged, transfected, stimulated, or drug-treated unless a source
explicitly states that handling.

### Patient samples collected before and after clinical treatment

Classify the collected material according to what was sequenced (for example,
`Human tissue (direct)` or `Human biospecimen (direct)`). Treatment administered to
the patient in vivo is not the same as treating the removed sample ex vivo.

### Primary human lung fibroblasts — vehicle — 24h

Classify as `Primary human cells (ex vivo/cultured)` and exclude. The cells originated from human lung but were separated, cultured, and exposed to a vehicle-control condition for 24 hours before measurement.

### Alveolar macrophages from COPD patients, incubated overnight and stimulated with LPS/JQ1

Disease relevance is direct, but classify as `Primary human cells (ex vivo/cultured/perturbed)` and exclude. The sequenced state reflects an ex vivo intervention.

### Surgically obtained COPD lung tissue processed for RNA-seq

Classify as `Human tissue (direct)` and include. The disease-associated transcriptome existed in vivo before resection.

### Bronchial brushing placed into culture and differentiated at air–liquid interface

Exclude. The human origin and airway relevance do not make the later culture a direct-tissue measurement.

## Recommended study-type vocabulary

- `Human tissue (direct)`
- `Human biospecimen (direct)`
- `Freshly isolated human cells`
- `Primary human cells (ex vivo/cultured)`
- `Primary human cells (ex vivo/cultured/perturbed)`
- `Cell line/culture`
- `Organoid/iPSC model`
- `Animal model`
- `Mixed human/animal`
- `Public-data reanalysis`
- `Unclear/other`

## Required evidence for handling claims

Do not state that a sample was cultured, passaged, differentiated, transfected,
stimulated, infected, incubated, or drug-treated unless the cited evidence or an
actionable source location explicitly supports that claim. When handling evidence is
missing, preserve the known material type, lower confidence when necessary, and state
that handling is unclear instead of filling the gap with a generic exclusion template.

## Disease relevance

Use only:

- `direct`: the study population, comparison, or measured disease tissue directly concerns the target disease.
- `no`: the disease appears only incidentally, as background, or not at all.

Do not use “related” as a middle category unless the user requests it.
