""" Use assembling parameters to produce images """

from kolme_musaa import settings as s
from kolme_musaa.utils import get_unique_save_path_name
from PIL import Image
import numpy as np
import warnings


def assemble_images_from_params(assembling_parameters, image_path_1, image_path_2):

    image_tensor = np.random.randint(low=0, high=256, size=(s.__IMAGE_SIDE_SIZE__,
                                                            s.__IMAGE_SIDE_SIZE__,
                                                            s.__COLOR_CHANNELS__))
    # print(f"(generate): received emotion={emotion}, word_pair={word_pair}")
    image = Image.fromarray(image_tensor, 'RGB')

    image_path = get_unique_save_path_name(directory=s.__STEP_1_EVAL_DIR__,
                                           basename="upote",
                                           extension="jpg")
    image.save(image_path, 'JPEG')