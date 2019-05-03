import unittest

import random_team.pgen as pgen


class PGenTests(unittest.TestCase):
    def test_annotation_generation(self):
        pgen.create_annotation_by_changing_colors("face.png")


if __name__ == "__main__":
    unittest.main()
