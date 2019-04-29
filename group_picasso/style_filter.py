import os
import random
import shutil

from PIL import Image
from evaluation1 import EmotionEvaluator


class StyleFilter:
    def __init__(self):
        self.folder = os.path.dirname(os.path.realpath(__file__))
        self.dataset_folder = os.path.join(self.folder, "images/dataset/test")
        self.style_folder = os.path.join(self.folder, "images/styles")
        self.emotion_evaluator = EmotionEvaluator()
        self.emotions = ["anger", "disgust", "fear", "happiness", "sadness", "surprise"]
        self.limits = {"anger": .4, "disgust": .7, "fear": .85, "happiness": .4, "sadness": .5, "surprise": .4}

    def filter_styles(self):
        for emotion in self.emotions:
            emotion_folder = os.path.join(self.style_folder, emotion)
            if os.path.exists(emotion_folder) and os.path.isdir(emotion_folder):
                shutil.rmtree(emotion_folder)
            os.mkdir(emotion_folder)

        style_filenames = os.listdir(self.dataset_folder)
        random.shuffle(style_filenames)
        for style_filename in style_filenames:
            style_path = os.path.join(self.dataset_folder, style_filename)
            max_emotion, score = self.emotion_evaluator.emotions_by_colours(style_path)
            if score > self.limits[max_emotion]:
                print("Style {}: {} {}...".format(style_filename, max_emotion, score))

                img = Image.open(style_path)
                if img.mode is not "RGB":
                    img = img.convert("RGB")
                width, height = img.size
                coef = min(width, height) / 256
                if width > height:
                    img = img.resize((round(width / coef), 256))
                else:
                    img = img.resize((256, round(height / coef)))

                dest_folder = os.path.join(self.style_folder, max_emotion)
                dest_path = os.path.join(dest_folder, style_filename)
                img.save(dest_path)


if __name__ == "__main__":
    style_filter = StyleFilter()
    style_filter.filter_styles()
