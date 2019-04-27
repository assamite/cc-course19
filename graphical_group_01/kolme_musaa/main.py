"""Main pipeline access"""

from kolme_musaa.step_1 import upote_main as step_1_main

def run_pipeline(emotion, word_pairs, n_art):
    ready_step_1 = step_1_main.execute(word_pairs=word_pairs, n_art=n_art)

    # do the other steps

    ready_final = ready_step_1

    return ready_final