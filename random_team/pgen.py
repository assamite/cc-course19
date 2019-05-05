import os
from typing import List, Tuple
import random
import base64
from io import BytesIO
import uuid
import json

from bs4 import BeautifulSoup
from PIL import Image
import requests
import shutil
import cv2
import numpy as np

ANNOTATION_COLORS = np.flip(np.matrix([
    [0, 162, 232],
    [255, 242, 0],
    [237, 28, 36],
    [34, 177, 76]
]), axis=1)


# This file contains functions related to portrait generation

def select_style_image(emotion: str, word_pairs: List[Tuple[str, str]], use_existing_style: bool = True) -> str:
    """
    Selects style image based on emotion and word pairs
    :param emotion:
    :param word_pairs:
    :return: Style image
    """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    if use_existing_style is True:
        # Use pre-defined set of style images and human created semantic maps
        available_styles = os.listdir(os.path.join(dir_path, 'style_samples', 'styles'))
        available_sem_maps = os.listdir(os.path.join(dir_path, 'style_samples', 'semantic_maps'))
        available_style_names = set(available_styles) | set(available_sem_maps)
        
        # Choose randomly one style
        style_image = random.choice(list(available_style_names))
        used_keywords = [style_image]
    else:
        human_word_pairs = list(filter(lambda pair: pair[0] == 'human', word_pairs))
        (_, description) = random.choice(human_word_pairs)
        used_keywords = [description]
        # Build a URL and fetch HTML containing image search results
        url = "https://www.bing.com/images/search?q={}+art+-meme&qft=+filterui:face-face".format(description)
        html = requests.get(url).text
        
        # Parse HTML and find all image tags (drop two first and the last image tags)
        soup = BeautifulSoup(html, features="html.parser")
        images = soup.find_all('img')[2:-1]
        img_el = random.choice(images)
        
        # Download image thumbnails and save them to out/<description>.<extension>
        img_url = img_el.get('src')
        res = requests.get(img_url, stream=True)

        extension = res.headers['Content-Type'].split('/')[-1]

        out_file_path = os.path.join(dir_path, "out", '{}.{}'.format(description, extension))
        if not os.path.exists(os.path.dirname(out_file_path)):
            os.makedirs(os.path.dirname(out_file_path))
        with open(out_file_path, 'wb') as out_f:
            shutil.copyfileobj(res.raw, out_f)
            
        style_image = out_file_path

    return style_image, used_keywords


def create_annotation_by_changing_colors(path_to_image: str) -> str:
    """
    Creates an annotation by replacing each color of original image with closest (by euclidean distance) color from a list of annotation colors
    :param path_to_image: Path to original image
    :return: Path to created annotation
    """
    # Read image
    image = cv2.imread(path_to_image)
    # Replace image with a tensor for calculating distances to annotation colors
    tmp = np.repeat(image, len(ANNOTATION_COLORS), axis=1).reshape((image.shape[0], image.shape[1], len(ANNOTATION_COLORS), 3))
    # Convert tensor to matrix to make np.subtract working (it allows only subtracting an array from matrix rows)
    tmp = tmp.reshape((tmp.shape[0] * tmp.shape[1], len(ANNOTATION_COLORS) * 3))
    # Square all substations results
    tmp = np.square(np.ravel(np.subtract(tmp, ANNOTATION_COLORS.flatten()))).reshape((image.shape[0] * image.shape[1], len(ANNOTATION_COLORS), 3))
    # Calculate square roots
    tmp = np.sqrt(np.sum(tmp, axis=2))
    # Find minimal euclidean distance and use corresponding key from annotation colors
    annotation = np.ravel(ANNOTATION_COLORS[np.argmin(tmp, axis=1)]).reshape(image.shape).astype(np.uint8)
    # Create a path to a file with annotation
    # This file will be saved to the same folder as original image
    image_file_name = os.path.splitext(os.path.basename(path_to_image))[-2]
    path_to_annotation = "%s%s" % (os.path.join(os.path.dirname(path_to_image), "%s_sem" % image_file_name), os.path.splitext(os.path.basename(path_to_image))[-1])
    # Save image
    cv2.imwrite(path_to_annotation, annotation)
    # Return a path to an annotation file
    return path_to_annotation


def create_annotation(path_to_image: str, use_existing_style: bool = True) -> str:
    """
    Creates an annotation (semantic map) from a provided image
    :param path_to_image: Path to file with original image
    :return: Annotation
    """
    
    if use_existing_style is True:
        # Use existing sample annotation
        dir_path = os.path.dirname(os.path.realpath(__file__))
        style_name = os.path.basename(path_to_image)
        annotation_path = os.path.join(dir_path, 'style_samples', 'semantic_maps', style_name)
    else:
        annotation_path = create_annotation_by_changing_colors(path_to_image)

    return annotation_path


def create_portrait(face: str, face_annotation: str, style_image: str, style_image_annotation: str, emotion: str, keywords: List[str]) -> str:
    """
    Generates a portrait
    :param face:
    :param face_annotation:
    :param style_image:
    :param style_image_annotation:
    :return:
    """
    # Convert all images to 512x512 png images
    SIZE = 512

    def resize(image_path: str, size: int) -> Image:
        image = Image.open(image_path)
        width, height = image.size
        return image.resize((size, size))

    def to_base64(image: Image) -> str:
        buffered = BytesIO()
        image.save(buffered, format='PNG')
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str

    body = {
        "face_image": to_base64(resize(face, SIZE)),
        "face_sem_map": to_base64(resize(face_annotation, SIZE)),
        "style_image": to_base64(resize(style_image, SIZE)),
        "style_sem_map": to_base64(resize(style_image_annotation, SIZE))
    }

    URL = 'http://ec2-3-85-8-145.compute-1.amazonaws.com/doodle'
    res = requests.post(URL, data=json.dumps(body), timeout=15*60, stream=True)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    keyword_str = '-'.join(keywords)
    out_file_name = 'RESULT-{}.png'.format('-'.join([emotion, keyword_str, uuid.uuid4().hex]))
    out_file_path = os.path.join(dir_path, out_file_name)
    with open(out_file_path, 'wb') as out_f:
        shutil.copyfileobj(res.raw, out_f)
    return out_file_path


def evaluate_annotation(annotation: str, emotion: str, word_pairs: List[Tuple[str, str]]) -> float:
    """
    Somehow evaluates an annotation(???)
    :param annotation:
    :param emotion:
    :param word_pairs:
    :return:
    """
    return 1.0


def generate_portrait(face: str, emotion: str, word_pairs: List[Tuple[str, str]]):
    """
    Generates a portrait based on provided face
    :param face:
    :param emotion:
    :param word_pairs:
    :return:
    """
    style_image, used_keywords = select_style_image(emotion, word_pairs, use_existing_style=False)
    style_image_annotation = create_annotation(style_image, use_existing_style=False)
    face_annotation = create_annotation(face, use_existing_style=False)

    evaluate_annotation(face_annotation, emotion, word_pairs)
    evaluate_annotation(style_image_annotation, emotion, word_pairs)
    portrait = create_portrait(face, face_annotation, style_image, style_image_annotation, emotion, used_keywords)
    meta = dict(
        face=face,
        face_annotation=face_annotation,
        style_image=style_image,
        style_image_annotation=style_image_annotation,
        used_keywords=used_keywords,
    )
    return portrait, meta


def evaluate_portrait(portrait: str) -> float:
    """
    Evaluates a portrait
    :param portrait:
    :return:
    """
    return 1.0
