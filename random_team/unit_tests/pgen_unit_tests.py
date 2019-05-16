import unittest

import cv2
import skimage.color as clr
# import skimage.future.graph as grh
import skimage.segmentation as sgm
import sklearn.cluster as cls
import numpy as np


import random_team.pgen as pgen


class PGenTests(unittest.TestCase):
    def test_annotation_generation(self):
        pgen.create_annotation_by_changing_colors("face1.png")
        cv2.imwrite("style.png", cv2.imread("compassionate.jpeg"))
        pgen.create_annotation_by_changing_colors("style.png")

    def test_segmentation(self):
        face = cv2.imread("face.png")
        labels = sgm.slic(face, n_segments=500, compactness=5)
        print(labels)
        out1 = clr.label2rgb(labels, face, kind="avg")
        labels = sgm.slic(out1, n_segments=200, compactness=5)
        out1 = clr.label2rgb(labels, out1, kind="avg")
        cv2.imshow("Test", out1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # g = grh.rag_mean_color(face, labels, mode='similarity')
        # labels2 = grh.cut_normalized(labels, g)
        # out2 = clr.label2rgb(labels2, face, kind='avg')
        # cv2.imshow("Test", out2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def test_clustering(self):
        face = cv2.imread("face1.png")
        labels = sgm.slic(face, n_segments=400, compactness=30)
        out1 = clr.label2rgb(labels, face, kind="avg")
        model = cls.KMeans(n_clusters=4)
        pixels = out1.reshape(face.shape[0] * face.shape[1], 3)
        model.fit(pixels)
        print(model.labels_)
        ANNOTATION_COLORS = np.flip(np.matrix([
            [0, 162, 232],
            [255, 242, 0],
            [237, 28, 36],
            [34, 177, 76]
        ]), axis=1).astype(np.uint8)
        face_sem = ANNOTATION_COLORS[model.labels_.reshape((face.shape[0], face.shape[1]))]
        print(face_sem)
        print(face_sem.shape)
        cv2.imshow("Test", face_sem)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite("res_sem.png", face_sem)


if __name__ == "__main__":
    unittest.main()
