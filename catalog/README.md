# Catalog schema

`models.json` is the source of truth. `CATALOG.md` is generated from it.

Required fields:

| Field | Meaning |
|---|---|
| `id` | stable lowercase slug |
| `name` | displayed model name |
| `year` | peer-reviewed year, otherwise first public preprint year |
| `status` | `peer-reviewed`, `preprint`, or `released` |
| `kind` | model / bridge category defined in the selection method |
| `primary_omics` | section used in the rendered catalog |
| `omics` | all represented modalities |
| `input_language` | concrete model input |
| `output_language` | reusable representation, prediction, or generated modality |
| `scale` | concise pretraining or parameter scale statement |
| `paper` | primary paper or preprint URL |
| `code` | official code URL or `null` |
| `weights` | official weights/API URL or `null` |
| `why_it_matters` | neutral, talk-relevant summary |
| `tags` | controlled tags used for filtering |
| `last_verified` | ISO date |

Allowed omics values and controlled tags are enforced by `scripts/validate_catalog.py`.
