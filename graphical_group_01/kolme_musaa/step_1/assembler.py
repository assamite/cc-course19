""" Use assembling parameters to produce images """

from kolme_musaa import settings as s
from kolme_musaa.utils import get_unique_save_path_name
from PIL import Image
import numpy as np
import warnings


def assemble_images_from_params(assembling_parameters, image_path_1, image_path_2):
    image_tensor = np.random.randint(low=0, high=256, size=(s.__IMAGE_HEIGHT__,
                                                            s.__IMAGE_WIDTH__,
                                                            s.__COLOR_CHANNELS__))
    # print(f"(generate): received emotion={emotion}, word_pair={word_pair}")
    warnings.warn("Not using args yet, generate at random..")
    image = Image.fromarray(image_tensor, 'RGB')

    image_path = get_unique_save_path_name(directory=s.__STEP_1_EVAL_DIR__,
                                           basename="upote",
                                           extension="png")
    image.save(image_path, 'PNG')