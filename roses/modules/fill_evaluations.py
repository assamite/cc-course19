from typing import List, Tuple
from random import randint
import numpy as np

def eval_semantics(poem: List[str]):
  """Does it make sense?
  
  We have no idea.
  """

  return 1

def eval_length(poem: List[str]):
  """Is it nice length?
  
  exp(- Square root of the absolute distance to the optimal length).
  """
  optimal_length = 77 # scientifically proven

  l = 0
  for line in poem:
    l += len(line)
  score = np.sqrt(np.abs(l - optimal_length))
  return np.exp(-score)

def eval_rhytm(poem: List[str]):
  """Does it have a nice rhythm, ie. a good amount of syllables in right places?"""
  return 1

def eval_similarity_to_emotion(poem: List[str], emotion: str):
  """Is the feeling of the poem similar to the emotion given as input?"""
  return 1

def eval_dissimilarity_to_word_pairs(poem: List[str], word_pairs: List[Tuple[str, str]]):
  """Has the system been able to alter the word pair from the original input in a craetive manner?"""
  return 1

def evaluate_poems(emotion: str, word_pairs: List[Tuple[str, str]], poems: List[List[str]]):
  """
  Evaluates given poems and gives them a score.
  """

  scores = [0]*len(poems)
  for i, poem in enumerate(poems):
    scores[i] += eval_semantics(poem)
    scores[i] += eval_length(poem)
    scores[i] += eval_rhytm(poem)
    scores[i] += eval_similarity_to_emotion(poem, emotion)
    scores[i] += eval_dissimilarity_to_word_pairs(poem, word_pairs)
  
  return list(zip(poems, scores))


# For testing
if __name__ == '__main__':
  example_emotion = 'sad'
  example_word_pairs = [("people", "boss"), ("animal", "legged")]
  example_poems = [
      ["Roses are red", 
      "human is boss", 
      "this project is not done", 
      "and you should be closs"
      ],
      ["Roses are red", 
      "animal is legged", 
      "this project is not done", 
      "and you should be egged"
      ]
  ]
  output = evaluate_poems(example_emotion, example_word_pairs, example_poems)
  print(output)