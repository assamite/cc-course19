# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 13:07:03 2019

@author: KatMal
"""

__doc__ = """this module is for evaluating images """
__version__ = """ version_01"""
__author__ = """KatMal """

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.spatial import cKDTree as KDTree


def emotionsbycolours(path, emotion):
    """evaluates emotions based on the colours in the image, input should be path to the image and emotion to be detected """
    pic = plt.imread(path)
    pixels = pic.shape[0]*pic.shape[1]
    plt.imshow(pic)
    col = ['red', 'darkred', 'pink', 'lightpink', 'green', 'lightgreen', 'darkgreen', 'blue', 'lightblue', 'darkblue', 'yellow', 'lightyellow', 'purple', 'lavender', 'black', 'grey', 'darkgrey', 'lightgrey', 'orange', 'white', 'darkorange', 'brown']
    colours = {k: colors.cnames[k] for k in col}
    named = {k: tuple(map(int, (v[1:3], v[3:5], v[5:7]), 3*(16,)))
                for k, v in colours.items()}
    ncol = len(named)
    tup = np.array(list(named.values()))

    names = list(named)
    tree = KDTree(tup[:-1])
    dist, idx = tree.query(pic, distance_upper_bound = np.inf)
    count = dict(zip(names, np.bincount(idx.ravel(), None, ncol+1)))
    
    for k in count:
        count[k] = round((count.get(k) / pixels),2)

    print('percentages of colour in the image')
    print(count)

    emotions = {'anger': 0, 'sadness':0, 'happiness': 0, 'fear':0, 'surprise': 0, 'disgust':0}

    for e in emotions:
        if e == 'anger':
            emotions[e] = count.get('red') + count.get('darkred') + count.get('black')
        if e == 'sadness':
            emotions[e] = count.get('blue') + count.get('darkblue') + count.get('lightblue') + count.get('grey') + count.get('lightgrey') + count.get('darkgrey')
        if e == 'happiness':
            emotions[e] = count.get('lightyellow') + count.get('yellow') + count.get('lightpink') + count.get('pink') + count.get('lightgreen') + count.get('white')
        if e == 'fear':
            emotions[e] = count.get('white') + count.get('black') + count.get('grey') + count.get('lightgrey') + count.get('darkgrey')
        if e == 'surprise':
            emotions[e] = count.get('purple') + count.get('lavender') + count.get('green') + count.get('lightgreen')
        if e == 'disgust':
            emotions[e] = count.get('brown') + count.get('green') + count.get('orange') + count.get('darkgreen') + count.get('darkorange')
        
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