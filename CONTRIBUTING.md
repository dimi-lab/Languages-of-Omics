# Contributing

Thank you for helping keep the omics foundation-model landscape useful rather than merely long.

## Inclusion criteria

A core entry should satisfy all of the following:

1. It is pretrained on broad, reusable biological data rather than trained for only one narrow prediction target.
2. It supports multiple downstream tasks, transfer, retrieval, conditional generation, or explicit cross-modal alignment.
3. A primary paper or preprint exists.
4. The input and output “languages” can be stated concretely.
5. Publication status, code, and weights are represented without implying that unavailable artifacts are open.

Task-specific methods can be proposed when they are genuine translation systems with unusual relevance to the talk, but should be labeled `foundation-enabled-system` rather than `foundation-model`.

## Add or update a model

1. Edit `catalog/models.json`.
2. Use stable primary links: DOI or publisher for the paper, official source repository for code, and an official checkpoint page for weights.
3. Set `last_verified` to the date on which you checked the links and status.
4. Run:

   ```bash
   python scripts/validate_catalog.py
   python scripts/render_catalog.py
   python scripts/render_catalog.py --check
   ```

5. In the pull request, state whether the model is peer-reviewed, a preprint, or a released artifact without a paper.

## Editorial rules

- Prefer the year of the peer-reviewed publication; otherwise use the first public preprint year.
- Do not equate “open source” with “weights available.” Record both separately.
- Use the shortest defensible scale statement and avoid marketing adjectives.
- A model may list several `omics` values, but `primary_omics` determines its catalog section.
- Claims in `why_it_matters` should describe architecture, data, or translation direction—not declare a winner.
- When a peer-reviewed paper supersedes a preprint, update the paper URL, year, and status while retaining the same `id`.

## Review checklist

- [ ] The entry passes schema validation.
- [ ] Paper, code, and weights point to primary or official sources.
- [ ] The availability flags match the URLs.
- [ ] Input and output language descriptions are intelligible to a biologist.
- [ ] Preprint status is visible.
- [ ] The generated `CATALOG.md` is included.
