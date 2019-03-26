"""Group Example's main file.

Should contain initialize- and create-functions.
"""

import os
import tarfile
from datetime import datetime
from urllib.request import urlretrieve

from PIL import Image

from group_picasso.libs.arbitrary_image_stylization.arbitrary_image_stylization_with_weights import code_entry_point
from group_picasso.libs.markov_img_gen.imggen import MarkovChain


class RandomImageCreator:

    def __init__(self, *args, **kwargs):
        """Initialize any data structures, objects, etc. needed by the system so that the system is fully prepared
        when create-function is called.

        Only keyword arguments are supported in config.json
        """

        print("Group Example initialize.")

        # Each creator should have domain specified: title, poetry, music, image, etc.
        self.domain = 'image'
        self.folder = os.path.dirname(os.path.realpath(__file__))
        self.model_url = "https://storage.googleapis.com/download.magenta.tensorflow.org/models/" \
                         + "arbitrary_style_transfer.tar.gz"
        self.content_img = "images/content/statue_of_liberty_sq.jpg"
        self.style_img = "images/styles/zigzag_colorful.jpg"

    def generate(self, *args, **kwargs):
        """Random image generator.
        """

        model_url_basename = os.path.basename(self.model_url)
        model_folder = os.path.join(self.folder, "pre-trained_models/arbitrary_style_transfer")
        model_download_folder = os.path.dirname(model_folder)
        model_download_path = os.path.join(model_download_folder, model_url_basename)
        if not os.path.isdir(model_download_folder):
            os.makedirs(model_download_folder)
        if not os.path.isdir(model_folder):
            print("Downloading pre-trained model...")
            urlretrieve(self.model_url, model_download_path)
            print("Extracting pre-trained model...")
            tar = tarfile.open(model_download_path, "r:gz")
            tar.extractall(path=model_download_folder)
            tar.close()
            os.remove(model_download_path)

        content_img_path = os.path.join(self.folder, self.content_img)
        style_img_path = os.path.join(self.folder, self.style_img)
        content_img_name = os.path.splitext(os.path.basename(content_img_path))[0]
        style_img_name = os.path.splitext(os.path.basename(style_img_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        style_img_markov_path = os.path.join(self.folder, "images/tmp/{}.png".format(timestamp))
        tmp_img_path = os.path.join(self.folder, "images/tmp/{}_{}.jpg".format(content_img_name, timestamp))
        tmp_img_name = os.path.splitext(os.path.basename(tmp_img_path))[0]

        chain = MarkovChain(bucket_size=1)
        style_img = Image.open(style_img_path)
        print("Training Markov model...")
        chain.train(style_img)
        print("Generating markovified style...")
        style_img_markov = chain.generate(width=64, height=64)
        style_img_markov.save(style_img_markov_path)

        print("Combining styles...")
        code_entry_point([
            "arbitrary_image_stylization_with_weights",
            "--checkpoint",
            os.path.join(model_folder, "model.ckpt"),
            "--output_dir",
            os.path.join(self.folder, "images/tmp/"),
            "--style_images_paths",
            style_img_markov_path,
            "--content_images_paths",
            content_img_path,
            "--interpolation_weights",
            "[0.35]",
        ])
        code_entry_point([
            "arbitrary_image_stylization_with_weights",
            "--checkpoint",
            os.path.join(model_folder, "model.ckpt"),
            "--output_dir",
            os.path.join(self.folder, "images/artifacts/"),
            "--style_images_paths",
            style_img_path,
            "--content_images_paths",
            tmp_img_path,
        ])

        return os.path.join(self.folder, "images/artifacts/{}_{}.jpg".format(tmp_img_name, style_img_name))

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
