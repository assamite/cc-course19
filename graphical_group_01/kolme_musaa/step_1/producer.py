""" Produces assembling parameters from word pairs """

import random
import os

from PIL import Image

import kolme_musaa.settings as s
from kolme_musaa.utils import debug_log

def produce_assembling_parameters(word_pair):
    """

    Parameters
    ----------
    word_pair

    Returns
    -------

    """

    w1 = word_pair[0]
    w2 = word_pair[1]

    w1_path = os.path.join(s.__STEP_1_CACHE_DIR__, w1)
    w2_path = os.path.join(s.__STEP_1_CACHE_DIR__, w2)

    w1_id = random.choice(os.listdir(w1_path))
    w2_id = random.choice(os.listdir(w2_path))

    im1_path = os.path.join(w1_path, w1_id)
    im2_path = os.path.join(w2_path, w2_id)

    debug_log(f"Image 1 ({w1}): {im1_path}")
    debug_log(f"Image 2 ({w2}): {im2_path}")

    im1 = Image.open(im1_path)
    im2 = Image.open(im2_path)

    # Now we have the images but we need to resize them to a 128x128 square
    im1 = resize_and_crop_to_square(im1, s.__IMAGE_SIDE_SIZE_NN__)
    im2 = resize_and_crop_to_square(im2, s.__IMAGE_SIDE_SIZE_NN__)

    return estimate_best_parameters(im1, im2), im1_path, im2_path


def resize_and_crop_to_square(image, side):
    """

    Parameters
    ----------
    image
    side

    Returns
    -------

    """
    cur_width, cur_height = image.size

    if cur_width < cur_height:
        # We scale down image so that width = side and later we cut down
        w, h = int(side), int(cur_height / (cur_width / side))
        image = image.resize((w, h))

    else: # cur_width >= cur_height
        # We scale down image so that height = side and later we cut down
        w, h = int(cur_width / (cur_height / side)), int(side)
        image = image.resize((w, h))

    # Now crop down to be a square
    h_margin = int((h - side) / 2)
    v_margin = int((w - side) / 2)

    image = image.crop((
        v_margin,           # left
        h_margin,           # top
        v_margin + side,    # right
        h_margin + side     # bottom
    ))

    debug_log(f"Resized image size: {image.size}")

    return image


def estimate_best_parameters(im1, im2):
    """

    Parameters
    ----------
    im1
    im2

    Returns
    -------
    tuple
        The following parameters:
        im1_x - position x (0 = left, 1 = right)
        im1_x -  position y (0 = top, 1 = bottom)
        im2_theta - relative angle theta (0 = 0 deg, 1 = 360 deg)
        im2_dist - relative position d  (0 = 0px from center, 1=inf px)
        s1 - scale of image 1 (0 = 0px, 1=inf)
        s2 - scale of image 2 (0 = 0px, 1=inf)
        r1 - rotation of image 1 (0 = 0 deg, 1 = 360 deg)
        r2 - rotation of image 2 (0 = 0 deg, 1 = 360 deg)
        alpha of foreground image (0 = transparent, 1 = opaque)

        If a function is in range [0, inf] use f: x / (1 - x)
    """


    # TODO: estimate best parameters

    l = lambda x: min(max(x, 0.000000000000000000001), 0.99999999999999999999999)

    return [
        l(random.gauss(0.5, 0.35)),  # pos x
        l(random.gauss(0.5, 0.35)),  # pos y
        random.random(),  # theta
        l(abs(random.gauss(0, 0.3))),  # dist
        l(random.gauss(0.55, 0.35)),  # s1
        l(random.gauss(0.55, 0.35)),  # s2
        l(abs(random.gauss(0.5, 2)) % 1),  # rot 1
        l(abs(random.gauss(0.5, 2)) % 1),  # rot 2
        l(1 - random.gauss(0.0, 0.8)),  # alpha
        random.random() # bg color
    ]


if __name__ == "__main__":
    produce_assembling_parameters(("animal", "adorable"))
