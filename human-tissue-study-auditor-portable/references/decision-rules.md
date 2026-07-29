# Decision rules

## 1. Two-gate decision

| Disease gate | Material gate | Decision |
|---|---|---|
| pass | pass | `YES/☑` |
| pass | fail or unclear | `NO/☐` |
| fail | pass | `NO/☐` |
| fail | fail | `NO/☐` |

Use only `direct` or `no` for disease relevance unless the user requests another scale.

## 2. Include

- Surgical, biopsy, frozen, resected, autopsy, transplant, or punch-biopsy human tissue with direct RNA/omics extraction.
- Lesional and non-lesional tissue collected from patients.
- Native whole blood, blood, PBMC, BAL/BALF, CSF, sputum, lavage, swab, urine, or brushing when within user scope.
- Freshly isolated or sorted cells only when no later culture or perturbation is documented.
- Samples collected before or after a therapy administered to the patient in vivo.
- A project-level mixed study with an independently identifiable direct human-disease tissue arm. State that only this arm qualifies.

## 3. Exclude

- Immortalized or transformed cell lines.
- Primary human cells expanded, passaged, maintained, differentiated, or cultured before measurement.
- Patient-derived material treated after collection with drugs, vehicle, cytokines, pathogens, smoke, hypoxia, antibodies, siRNA, CRISPR, transfection, or other perturbations.
- Explant cultures, even when the condition is labelled `untreated`, `vehicle`, or `control`.
- Organoids, iPSC-derived cells, reconstructed tissue, air–liquid interface cultures, co-cultures, and decellularized scaffolds.
- Animal models, xenografts, and psoriasiform/disease-like models without an independently qualifying human arm.
- Public-data reanalysis when the user asks for newly measured direct tissue.
- Disease mentions used only as pathway background, risk-locus context, or possible therapeutic relevance.

## 4. High-risk boundary cases

### In-vivo treatment versus ex-vivo treatment

- `Patient received etanercept; biopsy collected afterward` → direct tissue can qualify.
- `Biopsy incubated with etanercept after removal` → ex-vivo perturbation; exclude.

The word `treatment` alone is not sufficient. Identify who or what received the treatment.

### “Primary” ambiguity

- `Primary human tumor`, `primary tumor tissue`, `primary human biopsy` → may be direct tissue.
- `Primary fibroblasts`, `primary keratinocytes`, `primary epithelial cells` → cells; inspect handling.

### Freshly isolated cells

Use `Freshly isolated human cells` only when cells were isolated/sorted and sequenced without documented later manipulation. Do not mention culture or stimulation unless evidence explicitly says so.

### Untreated controls

`Untreated`, `vehicle`, `mock`, or `control` does not restore direct-tissue status if the material was cultured, passaged, incubated, or transfected.

### Mixed projects

- Project-level row containing both full-thickness biopsies and cultured keratinocytes: include only if the direct biopsy arm is explicit; classify as mixed and explain the qualifying arm.
- Sample-level cultured-keratinocyte row from that project: exclude.

### Disease-like terminology

`Psoriasiform`, `fibrosis-like`, `AD-like`, or similar terminology may describe an animal or in-vitro model. It is not automatically direct patient disease.

## 5. Study-type vocabulary

Prefer:

- `Human tissue (direct)`
- `Human biospecimen (direct)`
- `Freshly isolated human cells`
- `Mixed direct human tissue / cultured primary cells`
- `Primary human cells (ex vivo/cultured)`
- `Primary human cells (ex vivo/cultured/perturbed)`
- `Primary human tissue explant (ex vivo/perturbed)`
- `Cell line/culture`
- `Organoid/iPSC model`
- `Animal model`
- `Mixed human/animal`
- `Public-data reanalysis`
- `Unclear/other`

## 6. Confidence

- `high`: explicit disease, material, and handling evidence confirmed by an authoritative source.
- `moderate`: strong classification but one non-decisive metadata detail or publication match is incomplete.
- `low`: material, organism, handling, or disease relationship is substantially ambiguous.

Confidence never overrides the two-gate rule.
