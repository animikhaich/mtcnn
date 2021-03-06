import unittest
from PIL import Image
import numpy as np
from mtcnn.exceptions import InvalidImage
from mtcnn import MTCNN

mtcnn = None


class TestMTCNN(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global mtcnn
        mtcnn = MTCNN()

    def test_detect_faces(self):
        """
        MTCNN is able to detect faces and landmarks on an image
        :return:
        """
        ivan = Image.open("ivan.jpg").convert('RGB')
        ivan = np.asarray(ivan)
        ivan = ivan[:, :, ::-1]  # Convert to BGR

        result = mtcnn.detect_faces(ivan)  # type: list

        self.assertEqual(len(result), 1)

        first = result[0]

        self.assertIn('box', first)
        self.assertIn('keypoints', first)
        self.assertTrue(len(first['box']), 1)
        self.assertTrue(len(first['keypoints']), 5)

        keypoints = first['keypoints']  # type: dict
        self.assertIn('nose', keypoints)
        self.assertIn('mouth_left', keypoints)
        self.assertIn('mouth_right', keypoints)
        self.assertIn('left_eye', keypoints)
        self.assertIn('right_eye', keypoints)

        self.assertEqual(len(keypoints['nose']), 2)
        self.assertEqual(len(keypoints['mouth_left']), 2)
        self.assertEqual(len(keypoints['mouth_right']), 2)
        self.assertEqual(len(keypoints['left_eye']), 2)
        self.assertEqual(len(keypoints['right_eye']), 2)

    def test_detect_faces_invalid_content(self):
        """
        MTCNN detects invalid images
        :return:
        """
        try:
            ivan = Image.open("example.py").convert('RGB')
            ivan = np.asarray(ivan)
            ivan = ivan[:, :, ::-1]  # Convert to BGR
        except:
            ivan = None

        with self.assertRaises(InvalidImage):
            result = mtcnn.detect_faces(ivan)  # type: list

    def test_detect_no_faces_on_no_faces_content(self):
        """
        MTCNN successfully reports an empty list when no faces are detected.
        :return:
        """
        ivan = Image.open("no-faces.jpg").convert('RGB')
        ivan = np.asarray(ivan)
        ivan = ivan[:, :, ::-1]  # Convert to BGR

        result = mtcnn.detect_faces(ivan)  # type: list
        self.assertEqual(len(result), 0)

    def test_mtcnn_multiple_instances(self):
        """
        Multiple instances of MTCNN can be created in the same thread.
        :return:
        """
        detector_1 = MTCNN(steps_threshold=[.2, .7, .7])
        detector_2 = MTCNN(steps_threshold=[.1, .1, .1])

        ivan = Image.open("ivan.jpg").convert('RGB')
        ivan = np.asarray(ivan)
        ivan = ivan[:, :, ::-1]  # Convert to BGR

        faces_1 = detector_1.detect_faces(ivan)
        faces_2 = detector_2.detect_faces(ivan)

        self.assertEqual(len(faces_1), 1)
        self.assertGreater(len(faces_2), 1)

    @classmethod
    def tearDownClass(cls):
        global mtcnn
        del mtcnn


if __name__ == '__main__':
    unittest.main()
