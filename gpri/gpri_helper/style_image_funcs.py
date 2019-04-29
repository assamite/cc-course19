import cv2
import numpy as np
import numpy.random as npr

emotion_mapping = {
    'anger': 0,
    'disgust': 1,
    'fear': 2,
    'happiness': 3,
    'sadness': 4,
    'surprise': 5
}

# colour distributions:
red = lambda x: np.array([1, 1 - x, 0]) * npr.beta(4, 1)


def initiate_image(dims):
    """
    Create a black, empty, canvas (i.e. numpy array).
    :param dims: The dimensions of the images, e.g. (128, 128)
    :return:
        Numpy array
    """
    img = np.zeros((dims[0], dims[1], 3))
    return img


def draw_on_img(img, polygons, colors):
    """

    :param img: The image array
    :param polygons: List of polygons to draw
    :param colors: List of colors for the polygons
    :return:
        None
    """
    for p, c in zip(polygons, colors):
        cv2.fillPoly(img, [p], c)


def create_polygon(extent, variance, num_corners):
    """
    Create polygons, which roughly resemble stars.
    :param extent: How big the star should approximately be
    :param variance: With how much variance the corner points can be sampled
    :param num_corners: How many corners/arms the star should have
    :return:
        Numpy array with cartesian coordinates of the star
    """
    # Create points in radial coordinates, the outer corners first
    rad_outer = npr.normal(extent, variance, size=num_corners)
    # And then the inner corners
    rad_inner = npr.normal(extent / 2, variance / 2, size=num_corners)
    phi = np.sort(npr.uniform(size=2 * num_corners) * 2 * np.pi)
    # Put the sampled numbers into the right order to have an array of polar coordinates
    outer_points = np.dstack((rad_outer, phi[::2]))
    inner_points = np.dstack((rad_inner, phi[1::2]))
    points_pol = np.vstack((outer_points, inner_points)).reshape((-1, 2),
                                                                 order='F')
    # Transform array to cartesian coordinates
    points_cart = np.dstack((points_pol[:, 0] * np.cos(points_pol[:, 1]),
                             points_pol[:, 0] * np.sin(points_pol[:, 1])))
    return points_cart.astype(np.int32)


def create_styleImage(dims, num_polygons, extent, variance, num_corners):
    """
    Create a style image.
    :param dims: Dimensions of the style image
    :param num_polygons: How many polygons should be drawn
    :param extent: How big the polygons should be in pixel
    :param variance: How much variance in size there can be
    :param num_corners: How many corners each polygon should have
    :return:
        Numpy array of the image
    """
    # Sample polygons:
    polygons = [create_polygon(extent, variance, num_corners) for i in range(
        num_polygons)]
    # Put polygons to random position in image:
    polygons = [(p + np.array(
        [npr.uniform(0, dims[0]), npr.uniform(0, dims[1])])).astype(np.int32)
                for p in polygons]
    colors = [red(npr.beta(2, 1)) for i in range(num_polygons)]
    img = initiate_image(dims)
    draw_on_img(img, polygons, colors)
    return img
