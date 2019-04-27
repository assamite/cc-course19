""" Main file for step 1 """
import warnings
import os
from PIL import Image
import numpy as np

from . import assembler, classifier, downloader, producer
from kolme_musaa import settings as s
from kolme_musaa.utils import get_unique_save_path_name, debug_log

def execute(word_pairs:list, n_art:int):
    """Generates artifacts to be evaluated.

    New images are saved under __STEP_1_EVAL_DIR__.
     eval dir
    Parameters
    ----------
    word_pairs: list
        List of pairs of words.
    n_art: int
        Number of artifacts to be produced.

    """
    threshold = 0.5

    downloader.download(word_pairs=word_pairs)

    ready_list = list()

    while len(ready_list) < n_art:

        # Amount of artifacts left to produce
        artifacts_left = n_art - len(ready_list)
        debug_log(f"Should now produce {artifacts_left} artifact.. [Ready: {len(ready_list)}, Target: {n_art}]")

        for i in range(artifacts_left):
            assembling_parameters, image_path_1, image_path_2 = producer.produce_assembling_parameters(word_pair=word_pairs[i % len(word_pairs)])
            assembler.assemble_images_from_params(assembling_parameters, image_path_1, image_path_2)

        evals = classifier.evaluate_all()

        # Decide on evaluation

        for image_path, image_dict in evals:
            im_eval = image_dict["evaluation"]
            if im_eval > threshold:
                debug_log(f"{image_path} good with {im_eval} > {threshold}")
                ready_image_path = get_unique_save_path_name(s.__RESOURCES_STEP_1_READY__,
                                                             "upote_ready",
                                                             "png")
                os.rename(image_path, ready_image_path)
                ready_list.append((ready_image_path, image_dict))
            else:
                debug_log(f"{image_path} bad with {im_eval} <= {threshold}")
                debug_log(f"Deleting {image_path}..")
                os.remove(image_path)

    # end of while

    return ready_list








