import random
from collections import defaultdict, Counter

import numpy as np
from PIL import Image


def get_neighbours(x, y):
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


class MarkovChain(object):
    def __init__(self, bucket_size=1):
        self.counters = defaultdict(Counter)
        self.distribs = {}
        self.bucket_size = bucket_size

    def train(self, img):
        width, height = img.size
        img = np.array(img)[:, :, :3] // self.bucket_size * self.bucket_size
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
        img[init_pos] = random.choice(tuple(self.counters.keys()))
        stack = [init_pos]
        colored = set()
        colored.add(init_pos)
        while stack:
            x, y = stack.pop()
            color = tuple(img[x, y])
            colors = probs = ()
            if color in self.distribs:
                colors, probs = self.distribs[color]
            else:
                counter = self.counters[color]
                colors = tuple(counter.keys())
                freqs = tuple(counter.values())
                total = sum(freqs, 0.0)
                probs = np.divide(freqs, total)
                self.distribs[color] = (colors, probs)
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
