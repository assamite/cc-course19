import pandas as pd
import random
import os

#this function will choose a random image with the given emotion
#assumes the face images have been classified in a file called face_emotions.csv 
#returns the name of the file choosen, the files are in the face/ folder
#print_emotion_matrix = True will print all the possible images and their classes
def emotionFaceChooser(emotion: str, print_emotion_matrix: bool = False):
  emotionFile = 'face_emotions.csv'
  dir_path = os.path.dirname(os.path.realpath(__file__))
  emotion_file_path = os.path.join(dir_path, emotionFile)
  #facepath = 'faces/'
  df = pd.read_csv(emotion_file_path)
  emotiondf = df.loc[df[emotion] == 1]

  #if there is no images with given emotion, then just give a random image
  if emotiondf.size == 0:
    print('No faces with emotion found, giving an random face instead') 
    emotiondf = df
  	
  filename = emotiondf['file'].sample(n=1) 
  if print_emotion_matrix == True:
    print(emotiondf)
  
  real_path = os.path.join(dir_path, 'faces', filename.values[0])
  return real_path


# example on usage
#print(emotionFaceChooser('happiness'))
#print(emotionFaceChooser('disgust'))
