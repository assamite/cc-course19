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
        self.color_to_emotion = {
            'aliceblue': (),
            'antiquewhite': (),
            'aqua': (),
            'aquamarine': (),
            'azure': (),
            'beige': (),
            'bisque': (),
            'black': (),
            'blanchedalmond': (),
            'blue': (),
            'blueviolet': (),
            'brown': (),
            'burlywood': (),
            'cadetblue': (),
            'chartreuse': (),
            'chocolate': (), 'coral': (), 'cornflowerblue': (), 'cornsilk': (), 'crimson': (),
            'cyan': (), 'darkblue': (), 'darkcyan': (), 'darkgoldenrod': (), 'darkgray': (),
            'darkgreen': (), 'darkgrey': (), 'darkkhaki': (), 'darkmagenta': (),
            'darkolivegreen': (), 'darkorange': (), 'darkorchid': (), 'darkred': (),
            'darksalmon': (), 'darkseagreen': (), 'darkslateblue': (), 'darkslategray': (),
            'darkslategrey': (), 'darkturquoise': (), 'darkviolet': (), 'deeppink': (),
            'deepskyblue': (), 'dimgray': (), 'dimgrey': (), 'dodgerblue': (), 'firebrick': (),
            'floralwhite': (), 'forestgreen': (), 'fuchsia': (), 'gainsboro': (), 'ghostwhite': (),
            'gold': (), 'goldenrod': (), 'gray': (), 'green': (), 'greenyellow': (), 'grey': (),
            'honeydew': (), 'hotpink': (), 'indianred': (), 'indigo': (), 'ivory': (), 'khaki': (),
            'lavender': (), 'lavenderblush': (), 'lawngreen': (), 'lemonchiffon': (),
            'lightblue': (), 'lightcoral': (), 'lightcyan': (), 'lightgoldenrodyellow': (),
            'lightgray': (), 'lightgreen': (), 'lightgrey': (), 'lightpink': (), 'lightsalmon': (),
            'lightseagreen': (), 'lightskyblue': (), 'lightslategray': (), 'lightslategrey': (),
            'lightsteelblue': (), 'lightyellow': (), 'lime': (), 'limegreen': (), 'linen': (),
            'magenta': (), 'maroon': (), 'mediumaquamarine': (), 'mediumblue': (),
            'mediumorchid': (), 'mediumpurple': (), 'mediumseagreen': (), 'mediumslateblue': (),
            'mediumspringgreen': (), 'mediumturquoise': (), 'mediumvioletred': (),
            'midnightblue': (), 'mintcream': (), 'mistyrose': (), 'moccasin': (),
            'navajowhite': (), 'navy': (), 'oldlace': (), 'olive': (), 'olivedrab': (),
            'orange': (), 'orangered': (), 'orchid': (), 'palegoldenrod': (), 'palegreen': (),
            'paleturquoise': (), 'palevioletred': (), 'papayawhip': (), 'peachpuff': (),
            'peru': (), 'pink': (), 'plum': (), 'powderblue': (), 'purple': (),
            'rebeccapurple': (), 'red': (), 'rosybrown': (), 'royalblue': (), 'saddlebrown': (),
            'salmon': (), 'sandybrown': (), 'seagreen': (), 'seashell': (), 'sienna': (),
            'silver': (), 'skyblue': (), 'slateblue': (), 'slategray': (), 'slategrey': (),
            'snow': (), 'springgreen': (), 'steelblue': (), 'tan': (), 'teal': (), 'thistle': (),
            'tomato': (), 'turquoise': (), 'violet': (), 'wheat': (), 'white': (),
            'whitesmoke': (), 'yellow': (), 'yellowgreen': ()}

    def emotions_by_colours(self, path, emotion):
        """evaluates emotions based on the colours in the image, input should be path to the image and emotion to be detected """
        pic = plt.imread(path)
        pixels = pic.shape[0] * pic.shape[1]
        plt.imshow(pic)
        # col = ['red', 'darkred', 'pink', 'lightpink', 'green', 'lightgreen', 'darkgreen', 'blue', 'lightblue',
        #        'darkblue', 'yellow', 'lightyellow', 'purple', 'lavender', 'black', 'grey', 'darkgrey', 'lightgrey',
        #        'orange', 'white', 'darkorange', 'brown', 'darkslategray', 'saddlebrown']
        col = list(colors.cnames.keys())
        colours = {k: colors.cnames[k] for k in col}
        named = {k: tuple(map(int, (v[1:3], v[3:5], v[5:7]), 3 * (16,)))
                 for k, v in colours.items()}
        ncol = len(named)
        tup = np.array(list(named.values()))

        names = list(named)
        tree = KDTree(tup[:-1])
        dist, idx = tree.query(pic, distance_upper_bound=np.inf)
        count = dict(zip(names, np.bincount(idx.ravel(), None, ncol + 1)))

        for k in count:
            count[k] = round((count.get(k) / pixels), 2)

        print('percentages of colour in the image')
        print(sorted(count.items(), key=operator.itemgetter(1), reverse=True))

        emotions = {'anger': 0, 'sadness': 0, 'happiness': 0, 'fear': 0, 'surprise': 0, 'disgust': 0}

        for e in emotions:
            if e == 'anger':
                emotions[e] = count.get('red') + count.get('darkred') + count.get('black') + count.get(
                    'crimson') + count.get('indianred') + count.get('tomato') + count.get('firebrick')
            if e == 'sadness':
                emotions[e] = count.get('darkblue') + count.get('darkgrey') + count.get('darkviolet') + count.get(
                    'darkslategray') + count.get('steelblue') + count.get('dimgray') + count.get(
                    'cadetblue') + count.get('slategray') + count.get('darkslateblue') + count.get(
                    'lightslategrey') + count.get('grey')
            if e == 'happiness':
                emotions[e] = count.get('lightyellow') + count.get('yellow') + count.get('lightpink') + count.get(
                    'pink') + count.get('lightgreen') + count.get('lightblue') + count.get('goldenrod') + count.get(
                    'limegreen') + count.get('mediumseagreen') + count.get('peachpuff') + count.get('mistyrose')
            if e == 'fear':
                emotions[e] = count.get('white') + count.get('black') + count.get('darkgrey')
            if e == 'surprise':
                emotions[e] = count.get('purple') + count.get('lavender') + count.get('green') + count.get(
                    'lightgreen') + count.get('limegreen')
            if e == 'disgust':
                emotions[e] = count.get('brown') + count.get('darkgreen') \
                              + count.get('darkorange') + count.get('darkslategray') + count.get(
                    'saddlebrown') + count.get('sienna') + count.get('darkolivegreen') + count.get(
                    'darkkhaki') + count.get('olivedrab')

        print('\nemotions in the image')
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
