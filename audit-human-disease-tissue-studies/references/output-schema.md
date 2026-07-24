# Audit output schema

Append these columns to the copied source sheet unless the user specifies different labels or order:

| Column | Required content |
|---|---|
| Checkbox | `☑` for qualified rows; otherwise `☐` |
| Research subject | Short, precise subject phrase. Use multi-word disease concepts where needed, such as `Renal fibrosis`, `Idiopathic pulmonary fibrosis`, `Renal cancer`, or `Kidney transplantation`; never split a combined disease concept merely to make it one word |
| Disease relevance | `direct` or `no`; preserve the user’s exact requested header even if it contains a typo |
| Study type | Controlled classification from the decision rules |
| Confidence | `low`, `moderate`, or `high` |
| Original evidence quote | One or two complete, verbatim passages that directly prove the decisive inclusion/exclusion fact. Never use generated ellipses, fixed-length truncation, mechanical title/abstract concatenation, paraphrases, or unsupported absence claims |
| Evidence location | Independently actionable source location: accession plus exact workbook field, repository section, sample accession/protocol field, or publication Methods/Supplementary section; include a direct sample-level URL when applicable |
| Personalized explanation (YES rows re-reviewed) | User-language, row-specific explanation for every row. Checked rows explain why both inclusion criteria are met; unchecked rows explain the decisive exclusion reason and name the actual tissue/model and research subject. The legacy header may be preserved, but unchecked rows must not be left blank |
| Official source URL | Official GEO/SRA/ENA/ArrayExpress/BioProject record |
| Publication title | Exact matched publication title |
| Tissue type | Concise, normalized tissue, native biospecimen, cell model, or organism description. Never write `NA`; use `Not reported / unclear` only after checking all row fields and the official record |
| Publication URL | Original journal, PubMed, or PMC URL |
| DOI | DOI only, without invented values |
| PMID | PMID as text |
| Publication match basis | Exact accession/title/sample/method link used to establish the match |

## Formatting

- Preserve all original columns and values.
- Freeze the header row and keep filters enabled.
- Use wrapped text for long evidence and explanation fields.
- Make added headers visually distinct while matching the workbook.
- Use conditional formatting to highlight checked rows.
- Keep URLs as plain text so the workbook remains portable.
- Do not encode audit decisions only by color.

## Evidence requirements

- Map every quote to the exact decision it proves. General disease background,
  pathway relevance, or a mention of fibrosis is not decisive sample evidence.
- A title alone is insufficient when handling or direct extraction determines inclusion.
- Use complete sentences or complete field values; never cut a sentence at a character
  limit or add `...`/`…`.
- Use up to two passages when separate evidence is required for disease/organ identity
  and sample handling.
- Prefer sample-level source/characteristics/protocol/treatment fields, followed by
  official overall design and complete sample lists, publication Methods, and official
  study descriptions.
- When excluding because no target tissue was sequenced, inspect the complete sample
  set. Quote the actual sequenced materials and record the absence conclusion as an
  inference in the explanation, not as fabricated quoted text.
- For website evidence, name the accession and exact repository section, sample field,
  or publication Methods/Supplementary subsection, and include the direct URL when
  sample-level evidence is used.
- Confirm every quote occurs verbatim in its cited source and is consistent with
  `Study type`, `Tissue type`, and the personalized explanation.
- For unmatched publications, leave publication metadata blank and state that no exact match was asserted.
- For a requested full row-by-row review, include an official repository URL and a publication-match basis for every row, including negative rows.
