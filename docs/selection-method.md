# Selection method

## Scope

The catalog covers models whose pretraining data or intended transfer tasks are specific to an omics layer, a biomolecular sequence layer directly used in omics, or an explicit bridge between such layers.

The seed catalog was literature-checked through **2026-08-25**. It is deliberately selective, not exhaustive.

## What qualifies as a foundation model here

An entry is normally included when it has broad pretraining, reusable representations or conditional generation, and evidence across multiple downstream tasks. “Foundation model” is a claim about reuse and adaptation, not merely parameter count or use of a transformer.

The `kind` field distinguishes:

- `foundation-model`: broad pretrained backbone within one or more biological modalities;
- `multimodal-bridge`: explicit alignment or conditional mapping between modalities;
- `foundation-enabled-system`: a system built around one or more foundation backbones for a new omics interface.

## Evidence hierarchy

Links are selected in this order:

1. peer-reviewed primary paper at the publisher or DOI;
2. primary preprint when no peer-reviewed version exists;
3. official source repository;
4. official model/checkpoint or API page.

The catalog does not use review articles as the primary link for individual models. Reviews informed discovery and taxonomy only.

## Publication status

- `peer-reviewed` means a journal or archival conference paper was verified.
- `preprint` means no peer-reviewed version was identified during the last sweep.
- `released` is reserved for an official artifact without a primary manuscript.

Publication status is time-sensitive. Each record therefore carries `last_verified`.

## Availability

`code` and `weights` are independent fields. A public repository does not imply reproducible weights, commercial permission, or an open model license. License restrictions remain the responsibility of the user and should be checked at the linked source.

## What is not ranked

The catalog does not create a global performance ranking because model inputs, pretraining corpora, leakage controls, organisms, fine-tuning regimes, and evaluation tasks differ. Reported scale is descriptive; it is not a quality score.

## Known limitations

- Fast-moving preprints and repositories can change after verification.
- Training-corpus overlap is often difficult to audit.
- “Omics” sometimes refers to molecular sequences and sometimes to measured abundance matrices; the catalog records the actual input language to expose that distinction.
- Several models marketed as multimodal align embeddings but do not generate one assay from another.
- Paper-reported performance is not equivalent to independent replication, mechanistic validation, or clinical utility.

## Updating the sweep

A maintainer should periodically:

1. search each modality for newly peer-reviewed primary work;
2. check whether preprints have been superseded;
3. verify official repository and checkpoint links;
4. update `last_verified` only for entries actually checked;
5. regenerate `CATALOG.md` and run validation.
