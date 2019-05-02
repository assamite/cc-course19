import random
import spacy


nlp = spacy.load("en_core_web_sm")


class Title:
    def __init__(self, template_string):
        self.orig = template_string
        self.title = template_string.split(" ")

    def list_slots(self):
        for i, tok in enumerate(self.title):
            if tok == "[[ADJ]]":
                yield (i, "ADJ")
            elif tok == "[[NOUN]]":
                yield (i, "NOUN")
            elif tok == "[[NOUNS]]":
                yield (i, "NOUNS")
            elif tok == "[[PERSON]]":
                yield (i, "PERSON")
            elif tok == "[[LOC]]":
                yield (i, "LOC")

    def inject(self, token, tag, pos):
        """Inject the given token into the title."""
        assert pos >= -1
        assert pos < len(self.title)
        assert tag in ["ADJ", "NOUN", "NOUNS", "PERSON", "LOC"]
        assert self.title[pos] == "[[" + tag + "]]"
        self.title[pos] = token

    def __str__(self):
        return " ".join(self.title)


class TemplateBank:
    def __init__(self, title_bank):
        self.title_bank = title_bank

    def random_template(self, recursion_count=0):
        """Get random template from the bank."""

        if recursion_count > 25:
            raise RecursionError("Title generation was unable to find fitting template and produces deep recursion.")

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
            return self.random_template(recursion_count=recursion_count+1)

        try:
            # Randomly choose two (text, POS)-pairs and use them to create a template
            for old, new in random.sample(replacements, 2):
                tokens[tokens.index(old)] = new
        except ValueError:
            # Amount of templates should be enough to stop infinite recursion.
            return self.random_template(recursion_count=recursion_count+1)

        return ' '.join(tokens)
