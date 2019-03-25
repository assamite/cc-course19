"""Functionality to read and sample the word pair inputs.
"""
import os
import operator
import xml.etree.ElementTree as ET
import random
import re


ACTIVITY_FILE = os.path.join(os.path.dirname(__file__), "resources", "activity.xml")
ANIMAL_FILE = os.path.join(os.path.dirname(__file__), "resources", "domestic_animal.xml")
LOCATIONS_FILE = os.path.join(os.path.dirname(__file__), "resources", "locations.xml")
WEATHER_FILE = os.path.join(os.path.dirname(__file__), "resources", "meteorological_phenomenon.xml")
PROPERTIES_OF_CATEGORIES_FILE = os.path.join(os.path.dirname(__file__), "resources", "properties_of_categories.txt")

# Different input sets sorted with decreasing weight, e.g. for animal modifiers:
# [('wild', 127340), ('small', 62952), ('large', 45976), ('domestic', 44201), ...,('fictitious', 1), ('aqueous', 1)]
# Populated with :func:`read_input_sets`.
ACTIVITIES = None
ANIMAL_MODIFIERS = None
LOCATIONS = None
WEATHERS = None

# Dictionary of categories and their properties
# key: category name, value: list of properties
CATEGORIES = None

EMOTIONS = ['anger', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']


def parse_xml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    return root


def get_thesaurus_rex_xml_childs(root, tag):
    childs = []
    for child in root:
        if child.tag == tag:
            for c in child:
                childs.append((c.text.strip(), int(c.attrib['weight'])))
    return sorted(childs, key=operator.itemgetter(1), reverse=True)


def get_properties_of_categories(filepath):
    categories = {}
    with open(filepath) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line) > 0:
                category, properties = line.split(maxsplit=1)
                properties = re.sub(r'[\[\],]', '', properties)
                categories[category.lower()] = properties.split()
                #print(category.lower(), categories[category.lower()])
                #print(category, properties)
    return categories


def read_input_sets():
    global ACTIVITIES, ANIMAL_MODIFIERS, LOCATIONS, WEATHERS, CATEGORIES
    ACTIVITIES = get_thesaurus_rex_xml_childs(parse_xml(ACTIVITY_FILE), "Members")
    ANIMAL_MODIFIERS = get_thesaurus_rex_xml_childs(parse_xml(ANIMAL_FILE), "Modifiers")
    LOCATIONS = get_thesaurus_rex_xml_childs(parse_xml(LOCATIONS_FILE), "Members")
    WEATHERS = get_thesaurus_rex_xml_childs(parse_xml(WEATHER_FILE), "Members")
    CATEGORIES = get_properties_of_categories(PROPERTIES_OF_CATEGORIES_FILE)


def get_input(use_samples=True):
    """Create a custom sample input.

    :param bool use_samples:
        If true, uses smaller set of possible input properties by calling
        :func:`resources.sample_inputs.build_sample_input`.

    :returns: Full input (emotion and word_pairs) given to each group's create-function.
    """
    if use_samples:
        from resources import sample_inputs
        return sample_inputs.build_sample_input()

    global ACTIVITIES, ANIMAL_MODIFIERS, LOCATIONS, WEATHERS, CATEGORIES, EMOTIONS
    if ACTIVITIES is None:
        read_input_sets()

    word_pairs = []
    word_pairs.extend([('activity', x[0]) for x in random.sample(ACTIVITIES, 1)])
    word_pairs.extend([('animal', x[0]) for x in random.sample(ANIMAL_MODIFIERS, 3)])
    word_pairs.extend([('location', x[0]) for x in random.sample(LOCATIONS, 1)])
    word_pairs.extend([('weather', x[0]) for x in random.sample(WEATHERS, 1)])

    human_properties = 6
    category1 = random.choice(list(CATEGORIES.keys()))
    n1 = len(CATEGORIES[category1])
    n1 = n1 if n1 < 3 else 3
    n2 = human_properties - n1
    another_category_found = False
    while not another_category_found:
        category2 = random.choice(list(CATEGORIES.keys()))
        if category1 != category2 and len(CATEGORIES[category2]) >= n2:
            another_category_found = True
    #print("Using {} ({}) and {} ({})".format(category1, n1, category2, n2))
    word_pairs.extend([('human', x) for x in random.sample(CATEGORIES[category1], n1)])
    word_pairs.extend([('human', x) for x in random.sample(CATEGORIES[category2], n2)])
    emotion = random.choice(EMOTIONS)
    return emotion, word_pairs



if __name__ == "__main__":
    emotion, word_pairs = get_input(False)
    print(emotion, word_pairs)