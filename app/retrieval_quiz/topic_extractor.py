import spacy

class TopicExtractor:
    def __init__(self, spacy_model: str):
        self.nlp = spacy.load(spacy_model)
        self.keep_labels = {
            "ORG", "PRODUCT", "GPE", "LOC", "PERSON",
            "WORK_OF_ART", "EVENT", "NORP", "FAC"
        }

    def extract(self, text: str):
        doc = self.nlp(text)
        ents = [ent.text for ent in doc.ents if ent.label_ in self.keep_labels]
        chunks = [c.text for c in doc.noun_chunks if len(c.text.split()) <= 3]
        kws = [
            tok.lemma_ for tok in doc
            if tok.pos_ in {"NOUN", "PROPN", "ADJ"} and not tok.is_stop and len(tok.text) > 2
        ]
        return list(set(ents + chunks + kws))