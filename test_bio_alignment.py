import unittest
import warnings
from bio_alignment import align_predictions_to_bio, normalize_entity_type

ID = {0: "O", 1: "B-PER", 2: "I-PER", 3: "B-ORG", 4: "I-ORG", 5: "B-LOC", 6: "I-LOC", 7: "B-MISC", 8: "I-MISC"}
class AlignmentChecks(unittest.TestCase):
    def convert(self, tokens, entities):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            return align_predictions_to_bio([{"tokens": tokens, "ner_tags": [0]*len(tokens)}], [{"entities": entities}], ID, strict=False)[1][0]
    def test_misc_full_label(self):
        self.assertEqual(self.convert(["French", "team"], [{"entity_text":"French", "entity_type":"MISC"}]), ["B-MISC", "O"])
    def test_multitoken(self):
        self.assertEqual(self.convert(["New", "York"], [{"entity_text":"New York", "entity_type":"LOCATION"}]), ["B-LOC", "I-LOC"])
    def test_aliases(self):
        self.assertEqual([normalize_entity_type(x) for x in [" person ", "ORGANISATION", "B-MISC"]], ["PER", "ORG", "MISC"])
    def test_unsupported_fails(self):
        with self.assertRaises(ValueError):normalize_entity_type("DATE")
    def test_repeated_mentions(self):
        e={"entity_text":"Paris", "entity_type":"LOC"}
        self.assertEqual(self.convert(["Paris", "and", "Paris"], [e,e]), ["B-LOC", "O", "B-LOC"])
    def test_overlaps(self):
        self.assertEqual(self.convert(["New", "York", "University"], [{"entity_text":"New York", "entity_type":"LOC"}, {"entity_text":"New York University", "entity_type":"ORG"}]), ["B-ORG", "I-ORG", "I-ORG"])
    def test_no_partial_token(self):
        self.assertEqual(self.convert(["Yorkshire"], [{"entity_text":"York", "entity_type":"LOC"}]), ["O"])
    def test_mismatched_sentences(self):
        with self.assertRaises(ValueError):align_predictions_to_bio([{"tokens":[],"ner_tags":[]}], [], ID)
    def test_gold_lengths(self):
        with self.assertRaises(ValueError):align_predictions_to_bio([{"tokens":["a"],"ner_tags":[]}], [{"entities":[]}], ID)
class StrictEvaluationChecks(unittest.TestCase):
    def strict(self, tokens, entities):
        return align_predictions_to_bio(
            [{"tokens": tokens, "ner_tags": [0] * len(tokens)}],
            [{"entities": entities}], ID)
    def test_unmatched_aborts(self):
        with self.assertRaises(ValueError):
            self.strict(["Yorkshire"], [{"entity_text": "York", "entity_type": "LOC"}])
    def test_repeated_without_offsets_aborts(self):
        with self.assertRaises(ValueError):
            self.strict(["Paris", "and", "Paris"], [{"entity_text": "Paris", "entity_type": "LOC"}])
    def test_overlapping_aborts(self):
        with self.assertRaises(ValueError):
            self.strict(["New", "York", "University"], [
                {"entity_text": "New York", "entity_type": "LOC"},
                {"entity_text": "New York University", "entity_type": "ORG"}])
    def test_misc_exact_entity_evaluation(self):
        from seqeval.metrics import classification_report
        from seqeval.scheme import IOB2
        gold, pred = align_predictions_to_bio(
            [{"tokens": ["French", "team"], "ner_tags": [7, 0]}],
            [{"entities": [{"entity_text": "French", "entity_type": "MISC"}]}], ID)
        report = classification_report(gold, pred, mode="strict", scheme=IOB2,
                                       output_dict=True, zero_division=0)
        self.assertEqual(report["MISC"]["f1-score"], 1.0)

if __name__ == "__main__":
    unittest.main()
