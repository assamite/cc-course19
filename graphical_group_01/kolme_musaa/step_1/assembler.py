""" Use assembling parameters to produce images """

from kolme_musaa import settings as s
from kolme_musaa.utils import get_unique_save_path_name
from PIL import Image
import numpy as np
import warnings
import math


def assemble_images_from_params(assembling_parameters, image_path_1, image_path_2):
    """

    Parameters
    ----------
    assembling_parameters: tuple
        The following parameters:
        im1_x - position x (0 = left, 1 = right)
        im1_y -  position y (0 = top, 1 = bottom)
        im2_theta - relative angle theta (0 = 0 deg, 1 = 360 deg)
        im2_dist - relative position d  (0 = 0px from center, 1=inf px)
        s1 - scale of image 1 (0 = 0px, 1=inf)
        s2 - scale of image 2 (0 = 0px, 1=inf)
        r1 - rotation of image 1 (0 = 0 deg, 1 = 360 deg)
        r2 - rotation of image 2 (0 = 0 deg, 1 = 360 deg)
        alpha of foreground image (0 = transparent, 1 = opaque)
        bg_color - color base for the canvas

        If a function is in range [0, inf] use f: x / (1 - x)
    image_path_1
    image_path_2

    Returns
    -------

    """

    im1_x, im1_y, im2_theta, im2_dist, s1, s2, r1, r2, alpha, bg_color = assembling_parameters

    bg_color_int = int(bg_color * ((256)**3 - 1))  # transform in a color
    b = math.ceil((bg_color_int) % 256)
    g = math.ceil(bg_color_int // 256 % 256)
    r = math.ceil(bg_color_int // 256**2)

    canvas = Image.new(mode='RGBA', size=[s.__IMAGE_SIDE_SIZE__]*2, color=(r, g, b, 255))

    image_path = get_unique_save_path_name(directory=s.__STEP_1_EVAL_DIR__,
                                           basename="upote",
                                           extension="png")
    canvas.save(image_path, 'PNG')
    return image_path

if __name__ == "__main__":
    import random
    assemble_images_from_params([random.random() for _ in range(10)], "", "")