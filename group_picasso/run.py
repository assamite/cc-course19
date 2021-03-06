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

from group_picasso.evaluation1 import EmotionEvaluator
from group_picasso.evaluation2 import DistanceEvaluator
from group_picasso.libs.arbitrary_image_stylization.arbitrary_image_stylization_with_weights import code_entry_point
from group_picasso.markov import MarkovChain
from group_picasso.search_handler import SearchImage


class RandomImageCreator:

    def __init__(self):
        """Initialize any data structures, objects, etc. needed by the system so that the system is fully prepared
        when create-function is called.

        Only keyword arguments are supported in config.json
        """
        self.domain = 'image'
        self.folder = os.path.dirname(os.path.realpath(__file__))
        self.root_style_folder = os.path.join(self.folder, "images/styles")
        self.picasso_path = os.path.join(self.folder, "images/picasso.jpg")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(self.folder, "cc-course19-f3aafd62afc9.json")
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
            print("Couldn't locate pre-trained model!")
            return [self.__get_default_artifact_with_meta(emotion) for _ in range(number_of_artifacts)]

        artifacts_paths_with_meta = []
        n_tries = 10
        for i in range(number_of_artifacts):
            for j in range(n_tries):
                print("Artifact #{} (attempt {}/{}):".format(i + 1, j + 1, n_tries))
                if not self.__generate_content(emotion, word_pairs):
                    print("Couldn't find good enough content!")
                    artifacts_paths_with_meta.append(self.__get_default_artifact_with_meta(emotion))
                    break
                if self.__generate_artifact(emotion):
                    artifacts_paths_with_meta.append(self.__get_artifact_with_meta(emotion))
                    break
                if j == n_tries - 1:
                    print("Couldn't generate good enough artifact!")
                    artifacts_paths_with_meta.append(self.__get_default_artifact_with_meta(emotion))
        return artifacts_paths_with_meta

    def __get_default_artifact_with_meta(self, emotion):
        return self.picasso_path, {"evaluation": self.__evaluate_artifact_with_emotion(self.picasso_path, emotion)}

    def __get_artifact_with_meta(self, emotion):
        return self.artifact_path, {"evaluation": self.__evaluate_artifact_with_emotion(self.artifact_path, emotion)}

    def __generate_content(self, emotion, word_pairs):
        search_image = SearchImage()
        print("Generating content...")
        n_tries = 20
        for i in range(n_tries):
            search_query, animal = search_image.get_query(emotion, word_pairs)
            content_path = search_image.get_image(search_query)

            # content_path = os.path.join(self.folder, "images/content/otter_2.jpg")
            # animal = self.__get_basename(content_path).split("_")[0]

            print("Animal is {}!".format(animal))
            if self.__evaluate_content_with_vision(animal, content_path):
                self.content_path = content_path
                return True
            print("Changing content...")
        return False

    def __evaluate_content_with_vision(self, animal, content_path):
        print("Evaluating content \"{}\" with vision...".format(self.__get_basename(content_path)))
        with io.open(content_path, "rb") as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)
        response = self.client.label_detection(image=image)
        labels = response.label_annotations
        for label in labels:
            # print("\t{} {}".format(label.description.lower(), label.score))
            for word in label.description.split():
                if word.lower() == animal.lower() and label.score > .9:
                    print("Content OK!")
                    return True
        return False

    def __generate_artifact(self, emotion):
        print("Generating artifacts with different styles...")

        style_folder = os.path.join(self.root_style_folder, emotion)
        style_filenames = os.listdir(style_folder)

        # style_path = os.path.join(self.folder, "images/example_styles/Camille_Mauclair.jpg")

        n_tries = 10
        artifacts = []
        for i in range(n_tries):
            style_filename = random.choice(style_filenames)
            style_path = os.path.join(style_folder, style_filename)

            style_name = self.__get_basename(style_path)
            print("Step {}/{}: using style {}...".format(i + 1, n_tries, style_name))
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            markovified_path = os.path.join(self.folder, "images/tmp/{}.png".format(timestamp))
            tmp_path = os.path.join(self.folder,
                                    "images/tmp/{}_{}.jpg".format(self.__get_basename(self.content_path), timestamp))
            artifact_path = os.path.join(self.folder, "images/artifacts/{}_{}.jpg".format(self.__get_basename(tmp_path),
                                                                                          self.__get_basename(
                                                                                              style_path)))
            self.__generate_markovified(markovified_path, style_path)
            self.__transfer_style(markovified_path, tmp_path, style_path)
            [os.remove(path) for path in [markovified_path, tmp_path]]
            artifact_score = self.__evaluate_artifact_with_emotion(artifact_path, emotion)

            if artifact_score > 0:
                artifacts.append({"path": artifact_path, "style_name": style_name, "emotion_score": artifact_score})

        distance_evaluator = DistanceEvaluator()
        artifacts = distance_evaluator.difference(dlist=artifacts, grayscale=True)

        print("Scores:")
        keys = ["style_name", "emotion_score", "distance_score"]
        best_artifact = None
        for artifact in artifacts:
            if best_artifact is None or artifact["emotion_score"] + artifact["distance_score"] > \
                    best_artifact["emotion_score"] + best_artifact["distance_score"]:
                best_artifact = artifact
            print(dict((key, artifact[key]) for key in artifact.keys() if key in keys))
        print()

        if best_artifact:
            if best_artifact:
                print("Enough {} with style {}: emotion score is {} and distance score is {}!".format(
                    emotion,
                    best_artifact["style_name"],
                    best_artifact["emotion_score"],
                    best_artifact["distance_score"]
                ))
                self.artifact_path = best_artifact["path"]
            return True
        else:
            print("Not enough emotion!")
            return False

    @staticmethod
    def __get_basename(path):
        return os.path.splitext(os.path.basename(path))[0]

    @staticmethod
    def __generate_markovified(markovified_path, style_path):
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

    @staticmethod
    def __evaluate_artifact_with_emotion(artifact_path, emotion):
        """Evaluate image.
        """
        emotion_evaluator = EmotionEvaluator()
        max_emotion, score = emotion_evaluator.emotions_by_colours(artifact_path)
        if max_emotion == emotion:
            return score
        else:
            return 0
