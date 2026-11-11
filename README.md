# GPT-4o prompting for named entity recognition

This was my June 2025 Natural Language Processing project at the University of Padova, taught by Prof. Giorgio Satta. The university submission listed **Farzam Nikbakhsh Jorshari and Amirreza Soltani**. I was the primary developer and carried out the implementation and experiments.

Published on GitHub in **November 2026**. The code repairs below are November maintenance, separate from the original coursework.

I compared three ways of asking GPT-4o to extract named entities from CoNLL-2003: a direct prompt, a prompt asking for explanations, and a demonstration prompt with a few examples. The demonstration condition is few-shot. The development and test sections each used 50 sentences, shuffled with seed 42; this was a small course experiment, not a full benchmark evaluation.

The original BIO conversion truncated labels to three characters, turning MISC into MIS. This archive fixes label normalization, reads the gold schema from dataset metadata, and uses strict entity matching. Ambiguous, overlapping or unmatched predicted spans now stop evaluation instead of being silently discarded. Failed API requests and malformed JSON also stop the run.

**No corrected model scores are available.** The [historical evaluation note](docs/historical-evaluation.md) records the saved June 2025 scores as unverified. No API evaluation was rerun for publication. The original model alias did not record a snapshot, so a later call is a new experiment.

## Use

Tested with Python 3.10.2:

    python -m pip install -r requirements.txt
    python -m unittest -v test_bio_alignment.py

Open [ner_coursework.ipynb](ner_coursework.ipynb) in Jupyter after setting OPENAI_API_KEY and CONLL2003_PATH in your shell. The latter points to an authorized local Hugging Face DatasetDict export with validation/test splits, tokens and ClassLabel-based ner_tags. The variable names are documented in .env.example; it is not automatically loaded.

The repository includes no dataset text, API responses or credentials. Running the experiment cells makes paid API requests. Local checks cover label alignment and scoring behavior; they do not establish model performance. See [maintenance notes](docs/maintenance.md) for the changes and remaining limitations.

The prompting comparison was inspired by [Xie et al. (2023)](https://arxiv.org/abs/2310.10035); the dataset task is described by [Tjong Kim Sang and De Meulder (2003)](https://aclanthology.org/W03-0419/).
