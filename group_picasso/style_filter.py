import os
import shutil

from evaluation1 import EmotionEvaluator


class StyleFilter:
    def __init__(self):
        self.folder = os.path.dirname(os.path.realpath(__file__))
        self.style_folder = os.path.join(self.folder, "images/styles")
        self.emotion_evaluator = EmotionEvaluator()
        self.limits = {"anger": .4, "disgust": .4, "fear": .8, "happiness": .4, "sadness": .4, "surprise": .4}

    def filter_styles(self):
        for emotion in ["anger", "disgust", "fear", "happiness", "sadness", "surprise"]:
            folder = os.path.join(self.style_folder, emotion)
            if os.path.exists(folder) and os.path.isdir(folder):
                shutil.rmtree(folder)
            os.mkdir(folder)

        data_paths = [os.path.join(self.style_folder, f) for f in os.listdir(self.style_folder)]
        data_paths = [i for i in data_paths if os.path.isfile(i)]
        for style_filename in data_paths:
            style_path = os.path.join(self.style_folder, style_filename)
            max_emotion, score = self.emotion_evaluator.emotions_by_colours(style_path)
            print("Style {}: {} {}...".format(style_filename, max_emotion, score))
            if score > self.limits[max_emotion]:
                dest_folder = os.path.join(self.style_folder, max_emotion)
                shutil.copy(style_path, dest_folder)


if __name__ == "__main__":
    style_filter = StyleFilter()
    style_filter.filter_styles()
