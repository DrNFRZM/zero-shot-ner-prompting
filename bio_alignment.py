"""BIO alignment maintenance for the June 2025 course notebook (November 2026)."""
import unicodedata
import warnings

ALIASES = {
    "PER": "PER", "PERSON": "PER", "PERSONS": "PER",
    "ORG": "ORG", "ORGANIZATION": "ORG", "ORGANISATION": "ORG",
    "LOC": "LOC", "LOCATION": "LOC", "MISC": "MISC",
    "MISCELLANEOUS": "MISC",
}
VALID = {"O"} | {prefix + label for prefix in ("B-", "I-") for label in ("PER", "ORG", "LOC", "MISC")}

def normalize_entity_type(value):
    if not isinstance(value, str):
        raise ValueError("Entity type must be a string")
    value = value.strip().upper()
    if value.startswith(("B-", "I-")):
        value = value[2:]
    if value not in ALIASES:
        raise ValueError("Unsupported CoNLL-2003 entity type")
    return ALIASES[value]

def _text(value):
    return " ".join(unicodedata.normalize("NFC", value).casefold().split())

def _alignment_issue(message, strict):
    if strict:
        raise ValueError(message)
    warnings.warn(message, RuntimeWarning)


def align_predictions_to_bio(true_data, predictions, entity_type_map, *, strict=True):
    """Map spans to whole-token BIO labels; strict mode aborts uncertain mappings.

    Repeated text without offsets is ambiguous. Strict mode (the default) aborts
    unmatched, repeated or overlapping spans rather than silently scoring them.
    strict=False offers a diagnostic longest-first mapping with warnings; it is
    not a validated evaluation of those uncertain predictions.
    """
    if len(true_data) != len(predictions):
        raise ValueError("Sentence and prediction counts differ")
    y_true, y_pred = [], []
    for item, prediction in zip(true_data, predictions):
        tokens = item["tokens"]
        if len(tokens) != len(item["ner_tags"]):
            raise ValueError("Token and gold-label lengths differ")
        gold = [entity_type_map[tag] for tag in item["ner_tags"]]
        if any(tag not in VALID for tag in gold):
            raise ValueError("Unexpected gold-label schema")
        tags = ["O"] * len(tokens)
        candidates = []
        for order, entity in enumerate(prediction["entities"]):
            value = entity.get("entity_text")
            if not isinstance(value, str) or not value.strip():
                raise ValueError("Entity text must be nonempty")
            label = normalize_entity_type(entity.get("entity_type"))
            matches = [(i, j) for i in range(len(tokens))
                       for j in range(i + 1, len(tokens) + 1)
                       if _text(" ".join(tokens[i:j])) == _text(value)]
            if not matches:
                _alignment_issue("An entity did not align to a whole-token span", strict)
                continue
            if len(matches) > 1:
                _alignment_issue("Repeated entity text has no offsets; using first free span", strict)
            candidates.append((-(matches[0][1] - matches[0][0]), order, label, matches))
        for _, _, label, matches in sorted(candidates):
            for start, end in matches:
                if all(tag == "O" for tag in tags[start:end]):
                    tags[start] = "B-" + label
                    tags[start + 1:end] = ["I-" + label] * (end - start - 1)
                    break
            else:
                _alignment_issue("Overlapping entity omitted after longest-span resolution", strict)
        y_true.append(gold)
        y_pred.append(tags)
    return y_true, y_pred
