import unittest
from .search_handler import SearchImage


class TestSearchImage(unittest.TestCase):
    def setUp(self):
        self.search_image = SearchImage()

        self.word_pairs = ('anger',
                           [('activity', 'meeting'),
                            ('animal', 'slow'),
                            ('animal', 'prehistoric'),
                            ('animal', 'adorable'),
                            ('location', 'garden'),
                            ('weather', 'rain'),
                            ('human', 'deceptive'),
                            ('human', 'caring'),
                            ('human', 'compassionate'),
                            ('human', 'barbaric'),
                            ('human', 'brutal'),
                            ('human', 'ruthless')])

    def test_get_query(self):
        search_query, animal = self.search_image.get_query(self.word_pairs)
        print(search_query, animal)
        self.assertIsInstance(animal, str)
        self.assertIsInstance(search_query, str)

    def test_get_emotion(self):
        _, _ = self.search_image.get_query(self.word_pairs)
        emotion = self.search_image.get_emotion()
        self.assertEqual(emotion, 'anger')

    def test_get_image(self):
        search_query, animal = self.search_image.get_query(self.word_pairs)
        image = self.search_image.get_image(search_query)
        print(image)

        self.assertIsInstance(image, str)


if __name__ == '__main__':
    unittest.main()
