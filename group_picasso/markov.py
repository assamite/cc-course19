import random
from collections import defaultdict, Counter

import numpy as np
from PIL import Image


def get_neighbours(x, y):
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


class MarkovChain(object):
    def __init__(self):
        self.counters = defaultdict(Counter)

    def train(self, img):
        width, height = img.size
        img = np.array(img)
        for x in range(height):
            for y in range(width):
                color = tuple(img[x, y])
                for neighbour in get_neighbours(x, y):
                    try:
                        self.counters[color][tuple(img[neighbour])] += 1
                    except IndexError:
                        continue

    def generate(self, width=64, height=64):
        img = np.array(Image.new('RGB', (width, height), 'white'))
        init_pos = (np.random.randint(0, height), np.random.randint(0, width))
        img[init_pos] = random.choice(list(self.counters.keys()))
        stack = [init_pos]
        colored = set()
        colored.add(init_pos)
        distribs = {}
        while stack:
            x, y = stack.pop()
            colors = None
            probs = None
            color = tuple(img[x, y])
            if color not in distribs:
                counter = self.counters[color]
                colors = list(counter.keys())
                freqs = list(counter.values())
                total = sum(freqs, 0.0)
                probs = np.divide(freqs, total)
                distribs[color] = (colors, probs)
            else:
                colors, probs = distribs[color]
            color_idxs = np.arange(len(colors))
            neighbours = get_neighbours(x, y)
            np.random.shuffle(neighbours)
            for neighbour in neighbours:
                if neighbour not in colored and 0 <= neighbour[0] < width and 0 <= neighbour[1] < height:
                    color_idx = np.random.choice(color_idxs, p=probs)
                    img[neighbour] = colors[color_idx]
                    colored.add(neighbour)
                    stack.append(neighbour)
        return Image.fromarray(img)
