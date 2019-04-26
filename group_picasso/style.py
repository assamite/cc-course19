import operator

__doc__ = """ This module contains a  """
__version__ = """ version_01"""
__author__ = """Afhuertass """

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import os




def load_probabilities():

	# this can be changed 
	probs = dict()
	probs["anger"] = [  1.0/12]*12
	probs["disgust"] = [  1.0/12]*12
	probs["fear"] = [  1.0/12]*12
	probs["happines"] = [  1.0/12]*12
	probs["sadness"] = [  1.0/12]*12
	probs["surprise"] = [  1.0/12]*12

	return probs 


def get_subdirs(dir):
    "Get a list of immediate subdirectories"
    return next(os.walk(dir))[1]

def get_subfiles(dir):
    "Get a list of immediate subfiles"
    return next(os.walk(dir))[2]

def select_style( path ,emotion ):

	#EMOTIONS = ['anger', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']

	probs = load_probabilities()
	directories_styles = list( get_subdirs(path) ) 
	directories_styles = sorted( directories_styles )
	#print( len(directories_styles) )
	if len( directories_styles ) != 12:
		
		return None

	style  = np.random.choice( directories_styles , p = probs[emotion] )

	images = list( get_subfiles( path + "/" + style  )  )
	style_image = np.random.choice( images )
	final_path = path + "/" + style + "/" + style_image
	return final_path , style 


def main():

	select_style( path = "./images/styles2" , emotion = "sadness")


if __name__ == "__main__":
	main()