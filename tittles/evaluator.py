import cmudict

class evaluator():
    def __init__(self):
        self.value = 0
        self.cmudict = cmudict.dict()

    def evaluate(self, title):
        """Runs the different evaluation schemes, which return values between 0 and 1, and returns an average over them.
        Title comes as a list
        """
        self.eval_novelty(title)
        self.eval_alliteration(title)
        return self.value / 2

    def eval_novelty(self, title):
        if self.title_bank is None:
            self.value += 0.8
            return
        for b_id, b_info in self.title_bank.items():
            # Check novelty
            if str(title).lower().strip() == b_info["title"].lower().strip():
                self.value += 0.5
                return
        self.value += 1.0

    def eval_alliteration(self, title):
        unique_phonemes = []
        title_length = 1
        for word in title:
            try:
                phonemes = self.cmudict[word][0]
                title_length += len(phonemes)
                for phoneme in phonemes:
                    if phoneme not in unique_phonemes:
                        unique_phonemes.append(phoneme)
            except:
                #word was not in dict
                continue
        self.value += len(unique_phonemes) / title_length

    def get_alliteration_score(self, ratio):
        """ A function that has it maximum = 1 when ratio is 1/2, meaning half of the phonemes in the
        title are non-unique, otherwise it grows close to 0
        """
        return (-4*(ratio-0.5))**2 + 1
