# Output contract

Append these columns to the copied source sheet:

| Column | Required content |
|---|---|
| Checkbox | `☑` only when both gates pass; otherwise `☐` |
| Research subject | Short, precise multi-word subject |
| Disease relevance | `direct` or `no` |
| Study type | Controlled classification |
| Confidence | `low`, `moderate`, or `high` |
| Original evidence quote | Complete verbatim decisive evidence |
| Evidence location | Sheet row/field plus accession, section, sample, and URL when available |
| Personalized explanation (YES rows re-reviewed) | Row-specific reasoning for every row |
| Official source URL | GEO, SRA, ENA, ArrayExpress, BioProject, or other official record |
| Publication title | Exact title only when conservatively matched |
| Tissue type | Normalized tissue, biospecimen, cell model, or organism; never `NA` |
| Publication URL | Journal, PubMed, or PMC URL |
| DOI | DOI only |
| PMID | Text identifier |
| Publication match basis | Exact accession/title/sample/method link establishing the match |

## Evidence quality hierarchy

1. Sample-level `source_name`, characteristics, treatment, extraction, and culture protocol.
2. Official repository overall design and complete sample list.
3. Publication Methods or supplementary sample table.
4. Official study description.
5. Workbook row.

## Evidence acceptance test

A quote is acceptable only when:

- it occurs verbatim in the stated source;
- it directly proves the decision;
- it is a complete sentence or complete field value;
- it is not cut off or ended with generated ellipses;
- its subject is the material actually measured in that row/project.

Absence cannot be quoted. To exclude because target tissue is absent, cite the complete enumerated sample set and state that absence is an inference.

## Personalized explanation templates

### Included

> 该项目直接测量[患者/受试者]取得的[组织或原生样本]。[疾病状态]在取材前已于体内形成；[RNA/组学]直接来自该样本，未见取材后的培养、刺激、转染或药物处理，因此保留 YES。

### Excluded after manipulation

> 该项目虽与[目标疾病]直接相关，但实际测量材料为[材料]，并在取材后接受了[培养/刺激/转染/处理]。测得状态由离体实验形成，不是患者体内已经存在的原生组织状态，因此排除 NO。

### Wrong disease

> 该项目直接测量[实际材料]，但研究对象为[实际疾病/人群]；[目标疾病]仅为背景或未设置病例组，因此疾病条件不满足，排除 NO。

Do not copy templates mechanically. Replace every bracket with row-specific facts.

## Mandatory QC matrix

For every `YES` row verify:

| Check | Must be true |
|---|---|
| Disease | Explicit target-disease cohort/state |
| Human | Human organism/material |
| Material | Tissue/native biospecimen/fresh cells |
| Timing | State existed before collection |
| Handling | No later manipulation, or separate qualifying project arm |
| Evidence | Verbatim and decisive |
| Consistency | Type, tissue, quote, and explanation agree |

For every disease-relevant `NO`, verify that the exact exclusion mechanism is named and evidenced.
