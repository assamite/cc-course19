# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 02:42:12 2019

@author: KatMal
"""
__doc__ = """this module is for evaluating distances between images"""
__version__ = """ version_01"""
__author__ = """KatMal """


import numpy as np
import matplotlib.pyplot as plt
from skimage import color

class DistanceEvaluator:
    def sortbysecond(t):
        """sorts a list based on the second entry in a tuple"""
        return t[1] 
    
    def difference(self ,dlist, grayscale = False):
        """calculates the euclidean distance between images and gives them a score"""
        images = []
        for t in dlist:
            if grayscale == False: 
                images.append(plt.imread(t.get('path')))
            if grayscale == True:
                images.append(color.rgb2grey(plt.imread(t.get('path'))))
        
        
        mat = np.zeros((len(images),len(images)))
        for i in range(0,len(images)):
            for j in range(0,len(images)):
                distance = np.sum((images[i]-images[j])**2)
                mat[i][j] = distance
        
        tt = np.sum(mat, axis = 0)
        i = list(range(0,len(images)))
        d = list(zip(i,tt))
            
        d.sort(key = DistanceEvaluator.sortbysecond, reverse = True)
        
        lista = []
        k = 1.0
        l = k / len(images)
        for i in d:
            h = (i[0],round(k,1))
            lista.append(h)
            k = k - l
                
        lista2 = []
        for i in range(0,len(images)):
            for j in lista:
                if i == j[0]:
                    lista2.append(j[1])
    
        j = 0
        for t in dlist:
            t['distance_score'] = lista2[j]
            j = j + 1
        
        return dlist
