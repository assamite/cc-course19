""" Use assembling parameters to produce images """

import sys

from kolme_musaa import settings as s
from kolme_musaa.utils import get_unique_save_path_name, debug_log
from kolme_musaa.step_1.producer import resize_and_crop_to_square  # TODO: Consider moving this function
from PIL import Image

import numpy as np
import warnings
import math

eps = sys.float_info.epsilon

def assemble_images_from_params(assembling_parameters, image_path_1, image_path_2, wp):
    """

    Parameters
    ----------
    assembling_parameters: tuple
        The following parameters:
        im1_x - position x (0 = left, 1 = right)
        im1_y -  position y (0 = top, 1 = bottom)
        im2_theta - relative angle theta (0 = 0 deg, 1 = 359 deg)
        im2_dist - relative position d  (0 = 0px from center, 1=inf px)
        s1 - scale of image 1 (0 = 0px, 1=inf)
        s2 - scale of image 2 (0 = 0px, 1=inf)
        r1 - rotation of image 1 (0 = 0 deg, 1 = 359 deg)
        r2 - rotation of image 2 (0 = 0 deg, 1 = 359 deg)
        alpha of foreground image (0 = transparent, 1 = opaque)
        bg_color - color base for the canvas

        If a function is in range [0, inf] use f: x / (1 - x)
    image_path_1
    image_path_2

    Returns
    -------

    """

    # Retrieve parameters
    im1_x, im1_y, im2_theta, im2_dist, s1, s2, r1, r2, im2_alpha, bg_color = assembling_parameters

    debug_log(f"Parameters im1_x, im1_y, im2_theta, im2_dist, s1, s2, r1, r2, im2_alpha, bg_color: {assembling_parameters}")  # noqa

    if s1 > 0.7:
        debug_log(f"Warning, large scale image 1! s1={s1}")
        s1 = min(s1, 0.9)  # TODO: crop image in advance to avoid out of memory issues
    if s2 > 0.7:
        debug_log(f"Warning, large scale image 2! s2={s2}")
        s2 = min(s1, 0.9)

    # Define a function in range [0, inf[
    dist_fun = lambda x: x / (1 - x - eps)
    # Define a function in range ] -inf , +inf [  (logit)
    pos_fun = lambda x: math.log(eps + dist_fun(x))

    # Convert the parameters to actual values
    im1_position_x = pos_fun(im1_x) * s.__IMAGE_SIDE_SIZE__ + (s.__IMAGE_SIDE_SIZE__ / 2)
    im1_position_y = pos_fun(im1_y) * s.__IMAGE_SIDE_SIZE__ + (s.__IMAGE_SIDE_SIZE__ / 2)
    im2_angle_theta = im2_theta * 359
    im2_relative_distance = dist_fun(im2_dist) * s.__IMAGE_SIDE_SIZE__
    im1_scale = dist_fun(s1)
    im2_scale = dist_fun(s2)
    im1_rotation = r1 * 360 - 180
    im2_rotation = r2 * 360 - 180
    im2_alpha_channel = math.ceil(im2_alpha * 255)
    im2_position_x = im1_position_x + math.cos(math.radians(im2_angle_theta)) * im2_relative_distance
    im2_position_y = im1_position_y + math.sin(math.radians(im2_angle_theta)) * im2_relative_distance

    # Some debugging info for testing
    if s.__DEBUG_MODE__ == True and __name__ == "__main__":
        debug_log(f"Image 1 pos x: {im1_position_x}px",
                  '' if ((im1_position_x > 0) and (im1_position_x < s.__IMAGE_SIDE_SIZE__)) else ' (Center falls out of canvas)')
        debug_log(f"Image 1 pos y: {im1_position_y}px",
                  '' if im1_position_y > 0 and im1_position_y < s.__IMAGE_SIDE_SIZE__ else ' (Center falls out of canvas)')
        debug_log(f"Image 1 scale: {s.__IMAGE_SIDE_SIZE__}px x {im1_scale} = {s.__IMAGE_SIDE_SIZE__ * im1_scale}px")
        debug_log(f"Image 1 rotation: {im1_rotation}°")

        debug_log(f"Image 2 pos x: {im2_position_x}px ",
                  '' if im2_position_x > 0 and im2_position_x < s.__IMAGE_SIDE_SIZE__
                  else '(Center falls out of canvas)')
        debug_log(f"Image 2 pos y: {im2_position_y}px",
                  '' if im2_position_y > 0 and im2_position_y < s.__IMAGE_SIDE_SIZE__
                  else '(Center falls out of canvas)')
        debug_log(f"Image 2 scale: {s.__IMAGE_SIDE_SIZE__}px x {im2_scale} = {s.__IMAGE_SIDE_SIZE__ * im2_scale}px")
        debug_log(f"Image 2 rotation: {im2_rotation}°")
        debug_log(f"Image 2 relative distance from Image 1: {im2_relative_distance}px")
        debug_log(f"Image 2 angle with respect to Image 1: {im2_angle_theta}°")
        debug_log(f"Image 2 alpha channel (opacity): {im2_alpha_channel} = {im2_alpha_channel / 255 * 100}%")

    # Set a background color from the parameters
    bg_color_int = int(bg_color * ((256)**3 - 1))  # transform in a color
    b = math.ceil((bg_color_int) % 256)
    g = math.ceil(bg_color_int // 256 % 256)
    r = math.ceil(bg_color_int // 256**2)

    # Initialise the new image as a canvas
    canvas = Image.new(mode='RGBA', size=[s.__IMAGE_SIDE_SIZE__]*2, color=(r, g, b, 255))

    # Load images, convert to appropriate color space, crop and resize
    im1 = resize_and_crop_to_square(Image.open(image_path_1).convert('RGBA'), s.__IMAGE_SIDE_SIZE__)
    im2 = resize_and_crop_to_square(Image.open(image_path_2).convert('RGBA'), s.__IMAGE_SIDE_SIZE__)


    # Editing for image 1
    im1_w, im1_h = im1.size
    im1 = im1.resize(
        (max(1, math.ceil(im1_w * im1_scale)),
         max(1, math.ceil(im1_h * im1_scale)))
    )

    # A mask is needed to paste the images without borders
    rot1_mask = Image.new('L', im1.size, 255)
    im1 = im1.rotate(im1_rotation, expand=True)
    rot1_mask = rot1_mask.rotate(im1_rotation, expand=True)

    im1_w, im1_h = im1.size  # Update values after rotation
    canvas.paste(im1,
                 box=(math.ceil(im1_position_x - im1_w * 0.5), math.ceil(im1_position_y - im1_h * 0.5)),
                 mask=rot1_mask)


    # # Editing for image 2
    im2_w, im2_h = im2.size
    im2 = im2.resize(
        (max(1, math.ceil(im2_w * im2_scale)),
        max(1, math.ceil(im2_h * im2_scale)))
    )

    # A mask is needed to paste the images without borders
    rot2_mask = Image.new('L', im2.size, im2_alpha_channel)
    im2 = im2.rotate(im2_rotation, expand=True)
    rot2_mask = rot2_mask.rotate(im2_rotation, expand=True)

    im2_w, im2_h = im2.size  # Update values after rotation
    canvas.paste(im2,
                 box=(math.ceil(im2_position_x - im2_w * 0.5), math.ceil(im2_position_y - im2_h * 0.5)),
                 mask=rot2_mask)

    if s.__DEBUG_MODE__ == True and __name__ == "__main__":
        canvas.show()

    image_path = get_unique_save_path_name(directory=s.__STEP_1_EVAL_DIR__,
                                           basename=f"{wp[0]}_{wp[1]}",
                                           extension="png")
    canvas.save(image_path, 'PNG')
    return image_path



if __name__ == "__main__":
    import random, os
    p1 = os.path.join(s.__STEP_1_CACHE_DIR__, "activity", "570881.jpg")
    p2 = os.path.join(s.__STEP_1_CACHE_DIR__, "adorable", "623417.jpg")

    __FIXED__ = False

    l = lambda x: min(max(x, 0.000000000000000000001), 0.99999999999999999999999)

    if __FIXED__:
        assemble_images_from_params([
            0.5,  # pos x
            0.46,  # pos y
            0.222,  # theta
            0.31,  # dist
            0.5,  # s1
            0.5,  # s2
            0.5,  # rot 1
            0.5,  # rot 2
            0.6,  # alpha
            random.random()  # bg color
        ], p1, p2, ('activity', 'adorable'))
    else:
        assemble_images_from_params([
            l(random.gauss(0.46, 0.06)),  # pos x
            l(random.gauss(0.46, 0.06)),  # pos y
            random.random(),  # theta
            l(abs(random.gauss(0, 0.2))),  # dist
            l(random.gauss(0.45, 0.2)),  # s1
            l(random.gauss(0.45, 0.2)),  # s2
            l(abs(random.gauss(0.5, 0.12)) % 1),  # rot 1
            l(abs(random.gauss(0.5, 0.12)) % 1),  # rot 2
            l(1 - abs(random.gauss(0.0, 0.8))),  # alpha
            random.random()  # bg color
        ], p1, p2, ('activity', 'adorable'))