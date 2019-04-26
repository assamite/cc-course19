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

    def __init__(self, path):
        self.reds = ['crimson', 'darkred', 'darksalmon', 'firebrick', 'indianred', 'lightcoral', 'lightsalmon', 'red',
                     'salmon']
        self.oranges = ['coral', 'darkorange', 'orange', 'orangered', 'tomato']
        self.pinks = ['deeppink', 'mediumvioletred', 'hotpink', 'lightpink', 'palevioletred', 'pink']
        self.yellows = ['darkkhaki', 'gold', 'khaki', 'lemonchiffon', 'lightgoldenrodyellow', 'lightyellow', 'moccasin',
                        'palegoldenrod', 'papayawhip', 'peachpuff', 'yellow']
        self.browns = ['bisque', 'blanchedalmond', 'brown', 'burlywood', 'chocolate', 'cornsilk', 'darkgoldenrod',
                       'goldenrod', 'maroon', 'navajowhite', 'peru', 'rosybrown', 'saddlebrown', 'sandybrown', 'sienna',
                       'tan', 'wheat']
        self.purples_violets = ['blueviolet', 'darkmagenta', 'darkorchid', 'darkslateblue', 'darkviolet', 'fuchsia',
                                'indigo', 'lavender', 'magenta', 'mediumorchid', 'mediumpurple', 'mediumslateblue',
                                'orchid', 'plum', 'purple', 'rebeccapurple', 'slateblue', 'thistle', 'violet']
        self.whites = ['aliceblue', 'antiquewhite', 'azure', 'beige', 'floralwhite', 'ghostwhite', 'honeydew', 'ivory',
                       'lavenderblush', 'linen', 'mintcream', 'mistyrose', 'oldlace', 'seashell', 'snow', 'white',
                       'whitesmoke']
        self.grays_blacks = ['black', 'darkgray', 'darkgrey', 'darkslategray', 'darkslategrey', 'dimgray', 'gainsboro',
                             'gray', 'grey', 'lightgray', 'lightgrey', 'lightslategray', 'lightslategrey', 'silver',
                             'slategray', 'slategrey']
        self.greens = ['chartreuse', 'darkgreen', 'darkolivegreen', 'darkseagreen', 'forestgreen', 'green',
                       'greenyellow', 'lawngreen', 'lightgreen', 'lime', 'limegreen', 'mediumaquamarine',
                       'mediumseagreen', 'mediumspringgreen', 'olive', 'olivedrab', 'palegreen', 'seagreen',
                       'springgreen', 'yellowgreen']
        self.cyans = ['aqua', 'aquamarine', 'cadetblue', 'cyan', 'darkcyan', 'darkturquoise', 'lightcyan',
                      'lightseagreen', 'mediumturquoise', 'paleturquoise', 'teal', 'turquoise']

        self.blues = ['blue', 'cornflowerblue', 'darkblue', 'deepskyblue', 'dodgerblue', 'lightblue', 'lightskyblue',
                      'lightsteelblue', 'mediumblue', 'midnightblue', 'navy', 'powderblue', 'royalblue', 'skyblue',
                      'steelblue', 'teal']

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
        self.count = dict(zip(names, np.bincount(idx.ravel(), None, ncol + 1)))

        for k in self.count:
            self.count[k] = round((self.count.get(k) / pixels), 2)

    def emotions_by_colours(self, emotion):
        """evaluates emotions based on the colours in the image,
        input should be path to the image and emotion to be detected
        """
        print('Top colors in the image...')
        sorted_counts = sorted(self.count.items(), key=operator.itemgetter(1), reverse=True)
        for i in range(len(sorted_counts)):
            if sorted_counts[i][1] < .03:
                break
            print(sorted_counts[i])

        emotions = {'anger': 0, 'sadness': 0, 'happiness': 0, 'fear': 0, 'surprise': 0, 'disgust': 0}

        for e in emotions:
            if e == 'anger':
                emotions[e] = self.__sum_counts(self.reds + self.oranges + self.browns)
            if e == 'sadness':
                emotions[e] = self.__sum_counts(self.blues + self.purples_violets + self.cyans + self.grays_blacks)
            if e == 'happiness':
                emotions[e] = self.__sum_counts(self.whites + self.pinks + self.yellows + self.purples_violets)
            if e == 'fear':
                emotions[e] = self.__sum_counts(self.grays_blacks + self.whites)
            if e == 'surprise':
                emotions[e] = self.__sum_counts(
                    self.greens + self.cyans + self.yellows + self.oranges + self.reds + self.pinks)
            if e == 'disgust':
                emotions[e] = self.__sum_counts(self.browns + self.greens)

        print('Emotions in the image...')
        print(emotions)

        maximumemotion = emotions.get('anger')
        emotiondetected = 'anger'
        for e in emotions:
            if emotions.get(e) > maximumemotion:
                maximumemotion = emotions.get(e)
                emotiondetected = e

        if emotion != emotiondetected:
            maximumemotion = 0

        return (maximumemotion)

    def __sum_counts(self, colors):
        sum = 0
        for color in colors:
            sum += self.count.get(color)
        return sum
