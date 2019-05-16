from collections import defaultdict
import random

def windows(lst, n):
    for i in range(0, len(lst) - n + 1):
        yield tuple(lst[i:i+n])

class MarkovChain:
    def __init__(self, n):
        self.n = n
        self.transition = defaultdict(lambda: defaultdict(int))
        self.corpus = set()

    def add(self, string):
        tokens = string.split()
        for w in windows(['<START>'] * self.n + tokens + ['<END>'], self.n + 1):
            self.transition[w[:-1]][w[-1]] += 1
        self.corpus.add(' '.join(tokens))

    def generate(self):
        output = []
        state = ('<START>',) * self.n
        while True:
            next_state = random.choices(list(self.transition[state].keys()),
                                        list(self.transition[state].values()))[0]
            if next_state == '<END>':
                break
            output.append(next_state)
            state = state[1:] + (next_state,)
        output = ' '.join(output)
        if output in self.corpus:
            return self.generate()
        return output

if __name__ == "__main__":
    import os
    import pickle
    folder = os.path.dirname(os.path.realpath(__file__))
    markov = MarkovChain(3)
    with open(os.path.join(folder, "data", "titles.pickle"), "rb") as f:
        title_bank = pickle.load(f)
    for item in title_bank.values():
        markov.add(item['title'])
    # with open(os.path.join(folder, "data", "templates.short.uniq"), "r") as f:
    #     title_bank = [l.strip() for l in f.readlines()]
    # for title in title_bank:
    #     markov.add(title)
    print(markov.generate())
