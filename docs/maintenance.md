# November 2026 maintenance

The June 2025 submission is preserved privately. This public copy changes only the parts needed for safer execution and defensible evaluation:

- Authentication reads OPENAI_API_KEY from the environment. The exposed original key was revoked; no credential or saved response is included.
- Full PER/ORG/LOC/MISC aliases replace three-character truncation. Gold numeric labels are read from dataset features, with validation/test schema checks.
- BIO conversion checks sentence/token counts and whole-token spans. Strict mode stops on ambiguous repeated text, unmatched spans and overlaps. Diagnostic strict=False preserves a deterministic longest-first mapping with warnings, for inspection rather than validated scoring.
- Prompt entity types are limited to the four CoNLL categories. The original three prompt structures and GPT-4o alias remain.
- API failures and malformed JSON abort evaluation. They no longer become empty predictions.
- Evaluation uses seqeval strict IOB2 matching and explicit zero-division handling. No new model metrics were computed.
- Dataset loading uses CONLL2003_PATH and load_from_disk, avoiding automatic remote dataset-script execution or redistribution. Obtain data only under its own access terms.
- Saved outputs, student IDs, attachments and unnecessary metadata are removed. Plots no longer impose the old 0.6-0.85 score range. Reference author names were corrected from the linked arXiv records.

Checks cover normalization, multi-token spans, repeated/overlapping text, unmatched spans, length mismatches, and exact-entity scoring on a hand-written fixture. Notebook structure/import/schema checks are separate from real model evaluation.

The original span-only responses contain no token offsets. Strict alignment can therefore require manual review; the code does not pretend it can infer missing offsets reliably. The subset is small and the original alias is not a frozen model snapshot.

[OpenAI authentication documentation](https://developers.openai.com/api/reference/overview) describes environment-based credentials. The [GPT-4o model page](https://developers.openai.com/api/docs/models/gpt-4o) currently marks the model deprecated; access was not tested here and no newer model was substituted. [Hugging Face loading documentation](https://huggingface.co/docs/datasets/loading) describes local saved datasets.
