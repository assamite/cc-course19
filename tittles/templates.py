import random
import spacy


nlp = spacy.load("en_core_web_sm")


class Title:
    def __init__(self, template_string):
        self.orig = template_string
        self.title = template_string.split(" ")

        # Keep slots in memory for injections
        self.slots = {
            "ADJ": [],
            "NP": [],
            "PERSON": [],
            "LOC": [],
        }

        for i, tok in enumerate(self.title):
            if tok == "[[ADJ]]":
                self.slots["ADJ"].append((i, None))
            elif tok in ["[[NOUN]]", "[[PROPN]]"]:
                self.slots["NP"].append((i, "singular"))
            elif tok in ["[[NOUNS]]", "[[PROPNS]]"]:
                self.slots["NP"].append((i, "plural"))
            elif tok == "[[PERSON]]":
                self.slots["PERSON"].append((i, None))
            elif tok == "[[LOC]]":
                self.slots["LOC"].append((i, None))

    def get_slots(self, tag):
        """Get slots for the given tag."""
        assert tag in ["ADJ", "NP", "PERSON", "LOC"]
        return self.slots[tag]

    def inject(self, token, tag, pos=-1):
        """Inject the given token into the title."""
        # Fix these eventually
        assert pos >= -1
        assert pos < len(self.title)
        assert tag in ["ADJ", "NP", "PERSON", "LOC"]

        if len(self.slots[tag]) == 0:
            return None

        if pos >= 0:
            if pos not in self.slots[tag]:
                raise ValueError(
                    "Given position index is not a slot for the given tag."
                )
        else:
            # If 'pos' not given, inject to first available slot
            pos = self.slots[tag][0][0]

        self.title[pos] = token

        return token, pos

    def __str__(self):
        return " ".join(self.title)


class TemplateBank:
    def __init__(self, title_bank):
        self.title_bank = title_bank

    def random_template(self):
        """Get random template from the bank."""
        title = random.choice(list(self.title_bank.values()))["title"].replace('—', '-')

        replacements = []
        tokens = []
        doc = nlp(title)

        for token in doc:
            # Consider named entities as single token.
            if token.ent_type_ in ('PERSON', 'FAC', 'GPE', 'LOC'):
                if token.ent_iob == 1:
                    tokens[-1] += ' ' + token.text
                else:
                    tokens.append(token.text)
                continue

            tokens.append(token.text)
            if token.tag_ in ("NN", "NNP"):
                replacements.append((token.text, "[[NOUN]]"))
            elif token.tag_ in ("NNS", "NNPS"):
                replacements.append((token.text, "[[NOUNS]]"))
            elif token.pos_ == "ADJ":
                replacements.append((token.text, "[[ADJ]]"))

        for entity in doc.ents:
            if entity.label_ == 'PERSON':
                replacements.append((entity.text, '[[PERSON]]'))
            elif entity.label_ in ('FAC', 'GPE', 'LOC'):
                replacements.append((entity.text, '[[LOC]]'))

        if len(replacements) < 2:
            return self.random_template()

        for old, new in random.sample(replacements, 2):
            tokens[tokens.index(old)] = new

        return ' '.join(tokens)
