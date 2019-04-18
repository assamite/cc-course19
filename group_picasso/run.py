"""Group Example's main file.

Should contain initialize- and create-functions.
"""
import glob
import io
import os
import random
from datetime import datetime

from PIL import Image
from google.cloud import vision

from group_picasso.libs.arbitrary_image_stylization.arbitrary_image_stylization_with_weights import code_entry_point
from group_picasso.markov import MarkovChain


class RandomImageCreator:

    def __init__(self):
        """Initialize any data structures, objects, etc. needed by the system so that the system is fully prepared
        when create-function is called.

        Only keyword arguments are supported in config.json
        """
        self.domain = 'image'
        self.folder = os.path.dirname(os.path.realpath(__file__))
        self.picasso_path = os.path.join(self.folder, "images/picasso.jpg")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(self.folder, "cc-course19-03de99f05112.json")
        self.client = vision.ImageAnnotatorClient()
        self.content_path = None
        self.artifact_path = None

    def create(self, emotion, word_pairs, number_of_artifacts=10):
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
        if not glob.glob(os.path.join(self.folder, "model.ckpt*")):
            return self.__get_default_artifact_with_meta(emotion)

        for i in range(5):
            if not self.__generate_content(word_pairs):
                return self.__get_default_artifact_with_meta(emotion)

            if self.__generate_artifact(emotion):
                return self.__get_artifact_with_meta(emotion)

        return self.__get_default_artifact_with_meta(emotion)

    def __get_default_artifact_with_meta(self, emotion):
        return [(self.picasso_path, {"evaluation": self.__evaluate_artifact_emotion(self.picasso_path, emotion)})]

    def __get_artifact_with_meta(self, emotion):
        return [(self.artifact_path, {"evaluation": self.__evaluate_artifact_emotion(self.artifact_path, emotion)})]

    def __generate_content(self, word_pairs):
        print("Generating content...")
        for i in range(10):
            print("Attempt {}".format(i + 1))

            # search_query, animal = search_query_generator.generate(word_pairs)
            # content_path = content_downloader.get_content(search_query)

            animal = "dog"
            content_path = os.path.join(self.folder, "images/content/dog.jpg")

            print("Animal is {}...".format(animal))

            if self.__evaluate_content_vision(content_path, animal):
                self.content_path = content_path
                return True
        return False

    def __evaluate_content_vision(self, content_path, animal):
        print("Evaluating content with vision...")
        with io.open(content_path, "rb") as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)
        response = self.client.label_detection(image=image)
        labels = response.label_annotations
        for label in labels:
            for word in label.description.split():
                print("{} {}".format(word.lower(), label.score))
                if word.lower() == animal.lower():
                    print("Content OK!")
                    return True
        return False

    def __generate_artifact(self, emotion):
        for i in range(10):
            # style_path = image_selector.select(emotion)

            style_name = random.choice(os.listdir(os.path.join(self.folder, "images/styles")))
            style_path = os.path.join(self.folder, "images/styles/{}".format(style_name))

            print("Trying with style {}...".format(self.__get_basename(style_path)))

            for i in range(5):
                print("Attempt {}...".format(i + 1))
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
                markovified_path = os.path.join(self.folder, "images/tmp/{}.png".format(timestamp))
                tmp_path = os.path.join(self.folder,
                                        "images/tmp/{}_{}.jpg".format(self.__get_basename(self.content_path),
                                                                      timestamp))
                artifact_path = os.path.join(self.folder,
                                             "images/artifacts/{}_{}.jpg".format(self.__get_basename(tmp_path),
                                                                                 self.__get_basename(style_path)))

                self.__generate_markovified(markovified_path, style_path)
                self.__transfer_style(markovified_path, tmp_path, style_path)

                if self.__evaluate_artifact_vision(artifact_path) and self.__evaluate_artifact_emotion(artifact_path,
                                                                                                       emotion) > .5:
                    self.artifact_path = artifact_path
                    return True
        return False

    def __get_basename(self, path):
        return os.path.splitext(os.path.basename(path))[0]

    def __generate_markovified(self, markovified_path, style_path):
        chain = MarkovChain(bucket_size=16)
        style_img = Image.open(style_path)
        chain.train(style_img)
        style_img_markov = chain.generate()
        style_img_markov.save(markovified_path)

    def __transfer_style(self, markovified_path, tmp_path, style_path):
        code_entry_point([
            "arbitrary_image_stylization_with_weights",
            "--checkpoint",
            os.path.join(self.folder, "model.ckpt"),
            "--output_dir",
            os.path.join(self.folder, "images/tmp/"),
            "--style_images_paths",
            markovified_path,
            "--content_images_paths",
            self.content_path,
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
            style_path,
            "--content_images_paths",
            tmp_path,
            "--interpolation_weights",
            "[0.8]",
        ])

    def __evaluate_artifact_vision(self, artifact_path):
        print("Evaluating artifact with vision...")
        with io.open(artifact_path, "rb") as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)
        response = self.client.label_detection(image=image)
        labels = response.label_annotations
        for label in labels:
            for word in label.description.split():
                print("{} {}".format(word.lower(), label.score))
                if word.lower() in ["character", "dog", "canidae", "carnivore", "akita", "toy"]:
                    print("Style OK!")
                    return True
        return False

    def __evaluate_artifact_emotion(self, artifact_path, emotion):
        """Evaluate image.
        """
        return 1.0
