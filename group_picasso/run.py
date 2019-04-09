"""Group Example's main file.

Should contain initialize- and create-functions.
"""
import glob
import io
import os
from datetime import datetime

from PIL import Image
from google.cloud import vision

from group_picasso.libs.arbitrary_image_stylization.arbitrary_image_stylization_with_weights import code_entry_point
from group_picasso.markov import MarkovChain


class RandomImageCreator:

    def __init__(self, *args, **kwargs):
        """Initialize any data structures, objects, etc. needed by the system so that the system is fully prepared
        when create-function is called.

        Only keyword arguments are supported in config.json
        """
        # Each creator should have domain specified: title, poetry, music, image, etc.
        self.domain = 'image'
        self.folder = os.path.dirname(os.path.realpath(__file__))
        self.picasso_path = os.path.join(self.folder, "images/picasso.jpg")
        # self.content_img_path = os.path.join(self.folder, "images/content/dog.jpg")
        # self.content_img_path = os.path.join(self.folder, "images/content/colva_beach_sq.jpg")
        # self.content_img_path = os.path.join(self.folder, "images/content/eiffel_tower.jpg")
        # self.content_img_path = os.path.join(self.folder, "images/content/golden_gate_sq.jpg")
        self.content_img_path = os.path.join(self.folder, "images/content/statue_of_liberty_sq.jpg")
        # self.style_img_path = os.path.join(self.folder, "images/styles/homer.png")
        # self.style_img_path = os.path.join(self.folder, "images/styles/black_zigzag.jpg")
        # self.style_img_path = os.path.join(self.folder, "images/styles/bricks_sq.jpg")
        # self.style_img_path = os.path.join(self.folder, "images/styles/Camille_Mauclair.jpg")
        # self.style_img_path = os.path.join(self.folder, "images/styles/clouds-over-bor-1940_sq.jpg")
        # self.style_img_path = os.path.join(self.folder, "images/styles/La_forma.jpg")
        # self.style_img_path = os.path.join(self.folder, "images/styles/piano-keyboard-sketch_sq.jpg")
        # self.style_img_path = os.path.join(self.folder, "images/styles/pink_zigzag.jpg")
        # self.style_img_path = os.path.join(self.folder, "images/styles/red_texture_sq.jpg")
        # self.style_img_path = os.path.join(self.folder, "images/styles/Theo_van_Doesburg_sq.jpg")
        # self.style_img_path = os.path.join(self.folder, "images/styles/towers_1916_sq.jpg")
        self.style_img_path = os.path.join(self.folder, "images/styles/zigzag_colorful.jpg")
        self.content_img_name = os.path.splitext(os.path.basename(self.content_img_path))[0]
        self.style_img_name = os.path.splitext(os.path.basename(self.style_img_path))[0]
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(self.folder, "cc-course19-03de99f05112.json")
        self.client = vision.ImageAnnotatorClient()

    def generate(self, *args, **kwargs):
        """Random image generator.
        """
        if not glob.glob(os.path.join(self.folder, "model.ckpt*")):
            print("Pre-trained model not found...")
            return self.picasso_path

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        markov_style_img_path = os.path.join(self.folder, "images/tmp/{}.png".format(timestamp))
        tmp_img_name = "{}_{}".format(self.content_img_name, timestamp)
        tmp_img_path = os.path.join(self.folder, "images/tmp/{}.jpg".format(tmp_img_name))
        artifact_img_path = os.path.join(self.folder,
                                         "images/artifacts/{}_{}.jpg".format(tmp_img_name, self.style_img_name))

        self.generate_markov_style(markov_style_img_path)
        self.generate_artifact(markov_style_img_path, tmp_img_path)

        self.print_img_labels(self.content_img_path)
        self.print_img_props(artifact_img_path)

        return artifact_img_path

    def generate_markov_style(self, markov_style_img_path):
        chain = MarkovChain(bucket_size=16)
        style_img = Image.open(self.style_img_path)
        chain.train(style_img)
        style_img_markov = chain.generate()
        style_img_markov.save(markov_style_img_path)

    def generate_artifact(self, markov_style_img_path, tmp_img_path):
        code_entry_point([
            "arbitrary_image_stylization_with_weights",
            "--checkpoint",
            os.path.join(self.folder, "model.ckpt"),
            "--output_dir",
            os.path.join(self.folder, "images/tmp/"),
            "--style_images_paths",
            markov_style_img_path,
            "--content_images_paths",
            self.content_img_path,
            "--interpolation_weights",
            "[0.4]",
        ])
        code_entry_point([
            "arbitrary_image_stylization_with_weights",
            "--checkpoint",
            os.path.join(self.folder, "model.ckpt"),
            "--output_dir",
            os.path.join(self.folder, "images/artifacts/"),
            "--style_images_paths",
            self.style_img_path,
            "--content_images_paths",
            tmp_img_path,
            "--interpolation_weights",
            "[0.8]",
        ])

    def print_img_labels(self, img_path):
        with io.open(img_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)
        response = self.client.label_detection(image=image, max_results=100)
        labels = response.label_annotations
        print('Labels:')
        for label in labels:
            print("{}: {}".format(label.description, label.score))

    def print_img_props(self, img_path):
        with io.open(img_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)
        response = self.client.image_properties(image=image)
        props = response.image_properties_annotation
        print('Properties:')
        for color in props.dominant_colors.colors:
            print('fraction: {}'.format(color.pixel_fraction))
            print('\tr: {}'.format(color.color.red))
            print('\tg: {}'.format(color.color.green))
            print('\tb: {}'.format(color.color.blue))

    def evaluate(self, image):
        """Evaluate image.
        """
        return 0

    def create(self, emotion, word_pairs, number_of_artifacts=10, **kwargs):
        """Create artifacts in the group's domain.

        The given inputs can be parsed and deciphered by the system using any methods available.

        The function should return a list in the form of:

            [
                (artifact1, {"evaluation": 0.76, 'foo': 'bar'}),
                (artifact2, {"evaluation": 0.89, 'foo': 'baz'}),
                # ...
                (artifactn, {"evaluation": 0.29, 'foo': 'bax'})
            ]

        :param str emotion:
            One of "the six basic emotions": anger, disgust, fear, happiness, sadness or surprise.
            The emotion should be perceivable in the output(s).
        :param list word_pairs:
            List of 2-tuples, the word pairs associated with the output(s). The word_pairs are (noun, property) pairings
            where each pair presents a noun and its property which may be visible in the output. (Think of more creative
            ways to present the pairings than literal meaning.)
        :param int number_of_artifacts:
            Number of artifacts returned
        :returns:
            List with *number_of_artifacts* elements. Each element should be (artifact, metadata) pair, where metadata
            should be a dictionary holding at least 'evaluation' keyword with float value.
        """
        img = self.generate()
        return [(img, {"evaluation": self.evaluate(img)})]
