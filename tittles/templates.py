import random


class Title:
    def __init__(self, template_string):
        self.orig = template_string
        self.title = template_string.split(" ")

        # Keep slots in memory for injections
        self.slots = {
            "ADJ": [],
            "NP": []
        }

        for i, tok in enumerate(self.title):
            if tok == "[[ADJ]]":
                self.slots["ADJ"].append((i, None))
            elif tok in ["[[NOUN]]", "[[PROPN]]"]:
                self.slots["NP"].append((i, "singular"))
            elif tok in ["[[NOUNS]]", "[[PROPNS]]"]:
                self.slots["NP"].append((i, "plural"))

    def get_slots(self, tag):
        """Get slots for the given tag."""
        assert tag in ["ADJ", "NP"]
        return self.slots[tag]

    def inject(self, token, tag, pos=-1):
        """Inject the given token into the title."""
        # Fix these eventually
        assert pos >= -1
        assert pos < len(self.title)
        assert tag in ["ADJ", "NP"]

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
    def __init__(self, filepath=None):
        self.template_strings = []
        if filepath:
            self.read_templates(filepath)

    def read_templates(self, filepath):
        """Read tempaltes from the given file."""
        try:
            with open(filepath, "r") as f:
                self.template_strings = [l.strip() for l in f.readlines()]
        except FileNotFoundError:
            return 0

        return len(self.template_strings)

    def __len__(self):
        return len(self.template_strings)

    def __getitem__(self, i):
        if (i < 0) or (i >= len(self)):
            raise ValueError("Got index {} while bank has {} templates".format(
                i, len(self)))

        return self.template_strings[i]

    def random_template(self):
        """Get random template from the bank."""
        return self.template_strings[random.randint(0, len(self) - 1)]
