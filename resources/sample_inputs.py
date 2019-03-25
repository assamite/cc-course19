import random

EMOTIONS = ['anger', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']

SAMPLE_INPUTS = [['happiness', [('cat', 'black'), ('weather', 'rainy')]],
                 ['fear', [('cat', 'hungry'), ('account', 'empty')]],
                 ]

SAMPLE_ACTIVITIES = ['war', 'fishing', 'horticulture', 'dance', 'lecture', 'meeting', 'robbery']
SAMPLE_ANIMAL_MODIFIERS = ['slow', 'adorable', 'mythical', 'social', 'venomous', 'unusual', 'flying', 'hooved', 'prehistoric']
SAMPLE_LOCATIONS = ['cemetery', 'battlefield', 'garden', 'monument', 'data_center']
SAMPLE_WEATHERS = ['rain', 'fog', 'snow', 'typhoon', 'autumn_frost', 'sunshine']
SAMPLE_HUMAN_MODIFIERS = ['liberal', 'creative', 'evil', 'brutal', 'barbaric', 'deceptive', 'ruthless', 'caring', 'compassionate']


def build_sample_input():
    """Build and return full input from sample sets.
    """
    word_pairs = []
    word_pairs.extend([('activity', x) for x in random.sample(SAMPLE_ACTIVITIES, 1)])
    word_pairs.extend([('animal', x) for x in random.sample(SAMPLE_ANIMAL_MODIFIERS, 3)])
    word_pairs.extend([('location', x) for x in random.sample(SAMPLE_LOCATIONS, 1)])
    word_pairs.extend([('weather', x) for x in random.sample(SAMPLE_WEATHERS, 1)])
    word_pairs.extend([('human', x) for x in random.sample(SAMPLE_HUMAN_MODIFIERS, 6)])
    emotion = random.choice(EMOTIONS)
    return emotion, word_pairs


if __name__ == "__main__":
    print(build_sample_input())
