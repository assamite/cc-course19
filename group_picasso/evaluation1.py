# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 13:07:03 2019

@author: KatMal
"""
import operator

from PIL import Image

__doc__ = """this module is for evaluating images """
__version__ = """ version_01"""
__author__ = """KatMal """

import numpy as np
from matplotlib import colors
from scipy.spatial import cKDTree as KDTree


class EmotionEvaluator:

    def __init__(self):
        self.counts = None
        self.emotions = {}

        self.dark_blues = ["blue", "cornflowerblue", "darkblue", "deepskyblue", "dodgerblue", "mediumblue",
                           "midnightblue", "navy", "royalblue", "steelblue", "teal"]
        self.light_blues = ["lightsteelblue", "lightblue", "lightskyblue", "skyblue", "powderblue"]
        self.blacks = ["black"]
        self.light_browns = ["bisque", "blanchedalmond", "cornsilk", "navajowhite", "wheat"]
        self.mid_browns = ["burlywood", "chocolate", "darkgoldenrod", "goldenrod", "peru", "rosybrown", "saddlebrown",
                           "sandybrown", "sienna", "tan"]
        self.red_browns = ["brown", "maroon"]
        self.dark_cyans = ["cadetblue", "darkcyan", "teal"]
        self.light_cyans = ["aqua", "aquamarine", "cyan", "darkturquoise", "lightcyan", "lightseagreen",
                            "mediumturquoise", "paleturquoise", "turquoise"]
        self.slate_grays = ["darkslategray", "darkslategrey", "lightslategray", "lightslategrey", "slategray",
                            "slategrey"]
        self.other_grays = ["darkgray", "darkgrey", "dimgray", "gainsboro", "gray", "grey", "lightgray", "lightgrey",
                            "silver"]
        self.dark_greens = ["darkgreen", "darkolivegreen", "darkseagreen", "forestgreen", "green", "mediumseagreen",
                            "olive", "olivedrab", "seagreen"]
        self.light_greens = ["chartreuse", "greenyellow", "lawngreen", "lightgreen", "lime", "limegreen",
                             "mediumaquamarine", "mediumspringgreen", "palegreen", "springgreen", "yellowgreen"]
        self.red_oranges = ["orangered", "tomato"]
        self.other_oranges = ["coral", "darkorange", "orange"]
        self.pinks = ["deeppink", "mediumvioletred", "hotpink", "lightpink", "palevioletred", "pink"]
        self.dark_purples_violets = ["blueviolet", "darkmagenta", "darkorchid", "darkslateblue", "darkviolet", "indigo",
                                     "mediumorchid", "mediumpurple", "mediumslateblue", "purple", "rebeccapurple",
                                     "slateblue"]
        self.light_purples_violets = ["fuchsia", "lavender", "magenta", "orchid", "plum", "thistle", "violet"]
        self.dark_reds = ["crimson", "darkred", "firebrick", "indianred", "red"]
        self.light_reds = ["darksalmon", "lightcoral", "lightsalmon", "salmon"]
        self.whites = ["aliceblue", "antiquewhite", "azure", "beige", "floralwhite", "ghostwhite", "honeydew", "ivory",
                       "lavenderblush", "linen", "mintcream", "mistyrose", "oldlace", "seashell", "snow", "white",
                       "whitesmoke"]
        self.dark_yellows = ["darkkhaki"]
        self.mid_yellows = ["gold", "yellow"]
        self.light_yellows = ["khaki", "lemonchiffon", "lightgoldenrodyellow", "lightyellow", "moccasin",
                              "palegoldenrod", "papayawhip", "peachpuff"]

    def emotions_by_colours(self, path):
        pic = Image.open(path)
        if pic.mode is not "RGB":
            pic = pic.convert("RGB")
        pic = np.array(pic)
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

        # self.__print_top_colors()

        self.emotions["anger"] = self.__sum_counts(self.red_browns + self.red_oranges + self.dark_reds)
        self.emotions["sadness"] = self.__sum_counts(
            self.dark_blues + self.slate_grays + self.dark_purples_violets + self.dark_cyans)
        self.emotions["happiness"] = self.__sum_counts(
            self.pinks + self.light_reds + self.light_yellows + self.mid_yellows + self.whites)
        self.emotions["fear"] = self.__sum_counts(self.blacks + self.other_grays + self.whites)
        self.emotions["surprise"] = self.__sum_counts(
            self.light_blues + self.light_cyans + self.light_greens + self.other_oranges + self.pinks +
            self.light_purples_violets + self.light_reds + self.mid_yellows)
        self.emotions["disgust"] = self.__sum_counts(self.mid_browns + self.dark_greens + self.dark_yellows)

        # self.__print_top_emotions()

        max_emotion = max(self.emotions.items(), key=operator.itemgetter(1))[0]
        return max_emotion, self.emotions[max_emotion]

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
