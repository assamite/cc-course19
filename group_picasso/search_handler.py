import os
from glob import glob
import requests
import xmltodict
import random
from google_images_download import google_images_download as gim


# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class SearchImage:
    images = []
    output = 'images'
    image_dir = 'search'

    def _extract_keyword(self, word):
        site = 'http://ngrams.ucd.ie/therex3/common-nouns/category.action?'
        args = ['cate=' + word + '%3Aanimal', 'xml=true']
        url = site + '&'.join(args)
        animals = []

        res = requests.get(url)
        parsed = xmltodict.parse(res.content)

        for a in parsed['CategoryData']['Members']['Member']:
            x = a['#text'].split('_')
            x = x[0] if len(x) == 1 else x[1]
            animals.append(x)

        return animals

    def _build_query(self, emotion, keywords, n=5):
        search_keys = []

        for pair in keywords:
            if pair[0] == 'animal':
                animals = self._extract_keyword(pair[1])

                samples = random.choices(animals, k=n)
                # samples = random.choices(categories, k=n)

                search_keys += [(s, emotion + ' ' + pair[1] + ' ' + s) for s in samples]

        return search_keys

    def _get_images(self, search_key):
        response = gim.googleimagesdownload()

        old_files = glob(os.path.join(BASE_DIR, self.output, self.image_dir, '*'))

        for f in old_files:
            os.remove(f)

        image_paths = response.download({
            'keywords': search_key + ' animal creature',
            'limit': 20,
            'format': 'jpg',
            'size': 'medium',
            'output_directory': os.path.join(BASE_DIR, self.output),
            'image_directory': self.image_dir,
            'language': 'English',
            'safe_search': True
        })
        res = image_paths[search_key + ' animal creature']
        return [img_path for img_path in res if img_path.endswith('.jpg') or img_path.endswith('.jpeg')]

    def get_query(self, emotion, word_pairs):
        search_keys = self._build_query(emotion, word_pairs)
        animal, search_key = random.choice(search_keys)
        return search_key, animal

    def get_emotion(self):
        return self.emotion

    def get_image(self, search_key):
        images = self._get_images(search_key)

        return random.choice(images)
