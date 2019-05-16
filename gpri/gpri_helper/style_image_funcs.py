import cv2
import numpy as np
import numpy.random as npr
import random


# colour distributions:
anger     = lambda x: np.array([1 - 0.001 * x, 1 - x, 0.001 * x]) * npr.beta(4, 1)
disgust   = lambda x: random.choice([[np.array([0.02 * x, 1 - x, 0.01 * x]) * npr.beta(4, 1)],
                                    [np.array([0.625 - 0.02 * x, 0.5 - 0.05 * x, 0.25 - 0.02 * x]) * npr.beta(4, 1)]])[0]
happiness = lambda x: np.array([1 - 0.02 * x, 1 - 0.02 * x, 1 - x]) * npr.beta(4, 1)
sadness   = lambda x: random.choice([[np.array([0.5 * x, 0.5 * x, 0.5 * x]) * npr.beta(4, 1)],
                                    [np.array([0.02 * x, 0.01 * x, 1 - x]) * npr.beta(4, 1)],
                                    [np.array([1 - 0.1 * x, 0.05 * x, 1 - 0.2 * x]) * npr.beta(4, 1)]])[0]
surprise  = lambda x: random.choice([[np.array([1 - 0.02 * x, 0.77 * x, 0.8 * x]) * npr.beta(4, 1)],
                                    [np.array([1 - 0.01 * x, 0.8 - 0.25 * x, 1 - x]) * npr.beta(4, 1)]])[0]
fear      = lambda x: random.choice([[np.array([0.55 - 0.001 * x, 0.02 * x, 0.02 * x]) * npr.beta(4, 1)],
                                    [np.array([0.06 * x, 0.06 * x, 0.06 * x]) * npr.beta(4, 1)]])[0]


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


def create_anger_image(dims, num_shapes, extent, variance, num_corners):
    """
    Create a style image.
    :param dims: Dimensions of the style image
    :param num_shapes: How many polygons should be drawn
    :param extent: How big the polygons should be in pixel
    :param variance: How much variance in size there can be
    :param num_corners: How many corners each polygon should have
    :return:
        Numpy array of the image
    """

    # sample polygons:
    polygons = [create_polygon(extent, variance, num_corners) for i in range(
        num_shapes)]

    # put polygons to random position in image:
    polygons = [(p + np.array(
        [npr.uniform(0, dims[0]), npr.uniform(0, dims[1])])).astype(np.int32)
                for p in polygons]
    colors = [anger(npr.beta(2, 1)) for i in range(num_shapes)]

    # create an empty canvas
    img = initiate_image(dims)

    # draw the polygons on the canvas
    draw_on_img(img, polygons, colors)

    return img


def create_disgust_image(dims, num_shapes, extent, variance, num_corners):
    """
    Create a style image.
    :param dims: Dimensions of the style image
    :param num_shapes: How many polygons and how many ellipses should be drawn
                       (the total number of drawn shapes is 2 * num_shapes)
    :param extent: How big the polygons should be in pixel
    :param variance: How much variance in size there can be
    :param num_corners: How many corners each polygon should have
    :return:
        Numpy array of the image
    """

    # create a blank canvas
    img = initiate_image(dims)

    # draw the colors
    colors = [disgust(npr.beta(2, 1)) for i in range(num_shapes)]

    # determine where to place the ellipses
    first_axis  = []
    second_axis = []
    for i in range(0, num_shapes):

        var = i % dims[0]

        first_axis.append(abs(int(npr.normal(var, variance, size = 1))))
        second_axis.append(abs(int(npr.normal(var, variance, size = 1))))

    first_axis  = np.array(first_axis)
    second_axis = np.array(second_axis)

    np.random.shuffle(first_axis)
    np.random.shuffle(second_axis)

    # draw the ellipses on the canvas
    for color, first, second in zip(colors, first_axis, second_axis):
        limits = npr.normal(extent, variance, size = 2)
        img = cv2.ellipse(img, (first, second),
                         (abs(int(limits[0])), abs(int(limits[1]))), 1, 0, 360, color, -1)

    # sample polygons:
    polygons = [create_polygon(extent, variance, num_corners) for i in range(
        num_shapes)]

    # put polygons to random position in image:
    polygons = [(p + np.array(
        [npr.uniform(0, dims[0]), npr.uniform(0, dims[1])])).astype(np.int32)
                for p in polygons]

    # draw the polygons on top of the canvas containing ellipses
    draw_on_img(img, polygons, colors)

    return img


def create_fear_image(dims, num_shapes, extent, variance, num_corners):
    """
    Create a style image.
    :param dims: Dimensions of the style image
    :param num_shapes: Number of polygons to be blurred
                       (total number of polygons drawn is around num_shapes * 1.1)
    :param extent: How big the polygons should be in pixel
    :param variance: How much variance in size there can be
    :param num_corners: How many corners each polygon should have
    :return:
        Numpy array of the image
    """

    # sample polygons:
    polygons = [create_polygon(extent, variance, num_corners) for i in range(
        num_shapes)]

    # put polygons to random position in image:
    polygons = [(p + np.array(
        [npr.uniform(0, dims[0]), npr.uniform(0, dims[1])])).astype(np.int32)
                for p in polygons]
    colors = [fear(npr.beta(2, 1)) for i in range(num_shapes)]

    # create a blank canvas
    img = initiate_image(dims)

    # draw the shapes on it
    draw_on_img(img, polygons, colors)

    # blur the image
    img = cv2.GaussianBlur(img, (3, 3), cv2.BORDER_DEFAULT)

    # sample some new polygons
    reduced_num_polygons = int(num_shapes / 10)
    polygons_focused = [create_polygon(extent, variance, num_corners) for i in range(
        reduced_num_polygons)]
    polygons_focused = [(p + np.array(
        [npr.uniform(0, dims[0]), npr.uniform(0, dims[1])])).astype(np.int32)
                for p in polygons_focused]

    # draw some new colors
    colors_focused = [fear(npr.beta(2, 1)) for i in range(reduced_num_polygons)]

    # paint the newly drawn polygons on top of the blurred ones
    draw_on_img(img, polygons_focused, colors_focused)

    return img


def create_happiness_image(dims, num_shapes, extent, variance):
    """
    Create a style image.
    :param dims: Dimensions of the style image
    :param num_shapes: How many polygons should be drawn
    :param extent: How big the polygons should be in pixel
    :param variance: How much variance in size there can be
    :return:
        Numpy array of the image
    """

    # create a blank canvas
    img = initiate_image(dims)

    # draw the colors
    colors = [happiness(npr.beta(2, 1)) for i in range(num_shapes)]

    # determine where to place the shapes
    first_axis  = []
    second_axis = []

    for i in range(0, num_shapes):

        var = i % dims[0]

        first_axis.append(abs(int(npr.normal(var, variance, size = 1))))
        second_axis.append(abs(int(npr.normal(var, variance, size = 1))))

    first_axis  = np.array(first_axis)
    second_axis = np.array(second_axis)

    np.random.shuffle(first_axis)
    np.random.shuffle(second_axis)

    # draw ellipses on the canvas
    for color, first, second in zip(colors, first_axis, second_axis):
        limits = npr.normal(extent, variance, size = 2)
        img = cv2.ellipse(img, (first, second),
                         (abs(int(limits[0])), abs(int(limits[1]))), 1, 0, 360, color, -1)

    return img


def create_sadness_image(dims, num_shapes, variance):
    """
    Create a style image.
    :param dims: Dimensions of the style image
    :param num_shapes: How many polygons should be drawn
    :param variance: How much variance in size there can be
    :return:
        Numpy array of the image
    """

    # create a blank canvas
    img = initiate_image(dims)

    # draw the colors
    colors = [sadness(npr.beta(2, 1)) for i in range(num_shapes)]

    # determine where to put the shapes
    first_axis  = []
    second_axis = []
    third_axis  = []
    forth_axis  = []

    for i in range(0, num_shapes):

        var = i % dims[0]

        first_axis.append(abs(int(npr.normal(var, variance, size = 1))))
        second_axis.append(abs(int(npr.normal(var, variance, size = 1))))
        third_axis.append(abs(int(npr.normal(var, variance, size = 1))))
        forth_axis.append(abs(int(npr.normal(var, variance, size = 1))))

    first_axis  = np.array(first_axis)
    second_axis = np.array(second_axis)
    third_axis  = np.array(third_axis)
    forth_axis  = np.array(forth_axis)
    np.random.shuffle(first_axis)
    np.random.shuffle(second_axis)
    np.random.shuffle(third_axis)
    np.random.shuffle(forth_axis)

    # draw on the canvas
    for color, first, second, third, forth in zip(colors, first_axis, second_axis, third_axis, forth_axis):
        img = cv2.rectangle(img,(first, second),(third, forth), color,-1)

    return img


def create_surprise_image(dims, num_shapes, extent, variance, num_corners):
    """
    Create a style image.
    :param dims: Dimensions of the style image
    :param num_shapes: How many polygons should be drawn
    :param extent: How big the polygons should be in pixel
    :param variance: How much variance in size there can be
    :param num_corners: How many corners each polygon should have
    :return:
        Numpy array of the image
    """

    # sample polygons:
    polygons = [create_polygon(extent, variance, num_corners) for i in range(
        num_shapes)]

    # put polygons to random position in image:
    polygons = [(p + np.array(
        [npr.uniform(0, dims[0]), npr.uniform(0, dims[1])])).astype(np.int32)
                for p in polygons]
    colors = [surprise(npr.beta(2, 1)) for i in range(num_shapes)]

    # create a blank canvas
    img = initiate_image(dims)

    # draw on it
    draw_on_img(img, polygons, colors)

    return img
