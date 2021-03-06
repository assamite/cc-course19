import os
import random

from PIL import Image
from evaluation1 import EmotionEvaluator


class StyleFilter:
    def __init__(self):
        self.folder = os.path.dirname(os.path.realpath(__file__))
        self.dataset_name = "train"
        self.dataset_folder = os.path.join(self.folder, "images/dataset/" + self.dataset_name)
        self.style_folder = os.path.join(self.folder, "images/styles")
        self.emotion_evaluator = EmotionEvaluator()
        self.emotions = ["anger", "disgust", "fear", "happiness", "sadness", "surprise"]
        self.limits = {"anger": .5, "disgust": .92, "fear": .99, "happiness": .6, "sadness": .75, "surprise": .45}
        Image.MAX_IMAGE_PIXELS = None

    def filter_styles(self):
        style_filenames = os.listdir(self.dataset_folder)
        random.shuffle(style_filenames)
        for style_filename in style_filenames:
            style_path = os.path.join(self.dataset_folder, style_filename)
            try:
                max_emotion, score = self.emotion_evaluator.emotions_by_colours(style_path)
            except IndexError:
                print("Error: {}".format(os.path.basename(style_path)))
                continue
            if score >= self.limits[max_emotion]:
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
                dest_filename = self.dataset_name + "_{}_".format(int(score * 100)) + style_filename
                dest_path = os.path.join(dest_folder, dest_filename)
                img.save(dest_path)


if __name__ == "__main__":
    style_filter = StyleFilter()
    style_filter.filter_styles()
