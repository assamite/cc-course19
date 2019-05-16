# This is a stub file containing functions related to facial generation

# According to StyleGAN documentation this code
# fmt = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
# should produce some image / images
# this images are used to produce some result
# these images should be used with
# Gs.run(latents, None, truncation_psi=0.7, randomize_noise=True, output_transform=fmt)
import os
from typing import List, Tuple
from .faceChooser import emotionFaceChooser


def select_image(emotion: str, word_pairs: List[Tuple[str, str]], feedback_data) -> str:
    """
    Selects an image which will be used as an input for StyleGAN
    :param feedback_data: Some feedback information obtained as a result of evaluation
    :param emotion: Emotion, provided as input
    :param word_pairs: Word pairs, provided as input
    :return: Returns a base image which matches the emotion
    """
    face_path = emotionFaceChooser(emotion)
    return face_path


def create_noise_vector(emotion: str, word_pairs: List[Tuple[str, str]], feedback_data) -> None:
    """
    Create latent features/noise vector based on provided input as a result of evaluation
    :param feedback_data: Some feedback information
    :param emotion: Emotion, provided as input
    :param word_pairs: Word pairs, provided as input
    :return: Noise vector (used value for latents variable)
    """
    return None


def generate_face(latents: None, fmt: str, output_folder: str) -> str:
    """
    Produces images based on latent vector and selected images
    It is assumed, that StyleGAN is used in this method
    :param latent: Noise (latent) vector
    :param fmt: Selected images
    :return: Faces produced by StyleGAN
    """
    # return Gs.run(latents, None, truncation_psi=0.7, randomize_noise=True, output_transform=fmt)
    #return os.path.join(output_folder, "dummy.jpg")
    return fmt


def evaluate_emotion(face_image: str) -> float:
    """
    This function evaluates provided face_image

    Evaluates emotion at the provided faces
    :param face_image: Face image
    :return: Some evaluation estimate
    """
    return 1.0