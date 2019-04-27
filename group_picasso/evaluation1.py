# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 13:07:03 2019

@author: KatMal
"""
import operator

__doc__ = """this module is for evaluating images """
__version__ = """ version_01"""
__author__ = """KatMal """

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.spatial import cKDTree as KDTree


class EmotionEvaluator:

    def __init__(self):
        self.counts = None
        self.emotions = {}

        self.blues = ["blue", "cornflowerblue", "darkblue", "deepskyblue", "dodgerblue", "lightblue", "lightskyblue",
                      "lightsteelblue", "mediumblue", "midnightblue", "navy", "powderblue", "royalblue", "skyblue",
                      "steelblue", "teal"]
        self.blacks = ["black"]
        self.browns = ["bisque", "blanchedalmond", "brown", "burlywood", "chocolate", "cornsilk", "darkgoldenrod",
                       "goldenrod", "maroon", "navajowhite", "peru", "rosybrown", "saddlebrown", "sandybrown", "sienna",
                       "tan", "wheat"]
        self.cyans = ["aqua", "aquamarine", "cadetblue", "cyan", "darkcyan", "darkturquoise", "lightcyan",
                      "lightseagreen", "mediumturquoise", "paleturquoise", "teal", "turquoise"]
        self.grays = ["darkgray", "darkgrey", "darkslategray", "darkslategrey", "dimgray", "gainsboro", "gray", "grey",
                      "lightgray", "lightgrey", "lightslategray", "lightslategrey", "silver", "slategray", "slategrey"]
        self.greens = ["chartreuse", "darkgreen", "darkolivegreen", "darkseagreen", "forestgreen", "green",
                       "greenyellow", "lawngreen", "lightgreen", "lime", "limegreen", "mediumaquamarine",
                       "mediumseagreen", "mediumspringgreen", "olive", "olivedrab", "palegreen", "seagreen",
                       "springgreen", "yellowgreen"]
        self.oranges = ["coral", "darkorange", "orange", "orangered", "tomato"]
        self.pinks = ["deeppink", "mediumvioletred", "hotpink", "lightpink", "palevioletred", "pink"]
        self.purples_violets = ["blueviolet", "darkmagenta", "darkorchid", "darkslateblue", "darkviolet", "fuchsia",
                                "indigo", "lavender", "magenta", "mediumorchid", "mediumpurple", "mediumslateblue",
                                "orchid", "plum", "purple", "rebeccapurple", "slateblue", "thistle", "violet"]
        self.reds = ["crimson", "darkred", "darksalmon", "firebrick", "indianred", "lightcoral", "lightsalmon", "red",
                     "salmon"]
        self.whites = ["aliceblue", "antiquewhite", "azure", "beige", "floralwhite", "ghostwhite", "honeydew", "ivory",
                       "lavenderblush", "linen", "mintcream", "mistyrose", "oldlace", "seashell", "snow", "white",
                       "whitesmoke"]
        self.yellows = ["darkkhaki", "gold", "khaki", "lemonchiffon", "lightgoldenrodyellow", "lightyellow", "moccasin",
                        "palegoldenrod", "papayawhip", "peachpuff", "yellow"]

    def emotions_by_colours(self, path, emotion):
        pic = plt.imread(path)
        pixels = pic.shape[0] * pic.shape[1]
        col = list(colors.cnames.keys())
        colours = {k: colors.cnames[k] for k in col}
        named = {k: tuple(map(int, (v[1:3], v[3:5], v[5:7]), 3 * (16,)))
                 for k, v in colours.items()}
        ncol = len(named)
        tup = np.array(list(named.values()))
        names = list(named)
        tree = KDTree(tup[:-1])
        dist, idx = tree.query(pic, distance_upper_bound=np.inf)
        self.counts = dict(zip(names, np.bincount(idx.ravel(), None, ncol + 1)))
        for k in self.counts:
            self.counts[k] = round((self.counts.get(k) / pixels), 2)

        self.__print_top_colors()

        self.emotions["anger"] = self.__sum_counts(self.browns + self.oranges + self.reds)
        self.emotions["sadness"] = self.__sum_counts(self.blues + self.grays + self.purples_violets)
        self.emotions["happiness"] = self.__sum_counts(self.pinks + self.purples_violets + self.yellows + self.whites)
        self.emotions["fear"] = self.__sum_counts(self.blacks + self.grays + self.whites)
        self.emotions["surprise"] = self.__sum_counts(
            self.blues + self.cyans + self.greens + self.oranges + self.pinks + self.purples_violets + self.reds +
            self.yellows)
        self.emotions["disgust"] = self.__sum_counts(self.browns + self.greens)

        self.__print_top_emotions()

        max_emotion = max(self.emotions.items(), key=operator.itemgetter(1))[0]
        if max_emotion is emotion:
            return self.emotions[max_emotion]
        else:
            return 0

    def __sum_counts(self, counts):
        total = 0
        for count in counts:
            total += self.counts.get(count)
        return round(total, 2)

    def __print_top_colors(self):
        print("Top colors in the image...")
        sorted_counts = sorted(self.counts.items(), key=operator.itemgetter(1), reverse=True)
        for count in sorted_counts:
            if count[1] < .03:
                break
            print("\t{}".format(count))

    def __print_top_emotions(self):
        print("Emotions in the image...")
        sorted_emotions = sorted(self.emotions.items(), key=operator.itemgetter(1), reverse=True)
        for e in sorted_emotions:
            print("\t{}".format(e))
        print()
