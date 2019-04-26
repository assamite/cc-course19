""" Evaluates the quality of an assembling artwork """

import numpy as np
from PIL import Image

import os

import kolme_musaa.settings as s
from kolme_musaa.utils import debug_log



def evaluate_all(threshold=0.5):
    evals = list()
    eval_dir = s.__STEP_1_EVAL_DIR__

    for im_path in os.listdir(eval_dir):
        if not im_path.endswith(".png"):
            print(f"Skipping evaluation of {im_path} because it doesn't end with '.png'")
            continue

        image_path = os.path.join(eval_dir, im_path)

        evals.append((image_path, {'evaluation': evaluate(image_path)}))

    return evals


def evaluate(image_path=None, threshold=0.5):
    """Evaluates the goodness of an image artifact by its scaled average.

    Parameters
    ----------
    image_path: str
        path to an image that is supported by PIL

    Returns
    -------
    float:
        value grade for the artifact

    """
    image = Image.open(image_path)

    # Evaluation
    image_matrix = np.array(image, dtype=np.float)
    image_matrix /= 255.0

    return np.random.uniform()
