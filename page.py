"""Functionality to create 'a page' from combined outputs of the groups.
"""
from PIL import Image, ImageDraw, ImageFont


PAGE_TEMPLATE = ('word', 'image', 'image', 'image', 'image', 'poetry')

# A4 width and height with the correct DPI
DPI = 60
A4W, A4H = int(8.27 * DPI), int(11.7 * DPI)

# The magic numbers for relative placings depending on DPI.
TITLE_TOP_BORDER = int(DPI * (8.0/6))

IMG_MAX_DIM = int(DPI * 2 * (10.0/6))
IMG_LEFT_BORDER = int(0.5 * (A4W - (IMG_MAX_DIM * 2)))
IMG_TOP_BORDER = int(TITLE_TOP_BORDER * 1.5625)

POEM_TOP_BORDER = int((IMG_TOP_BORDER + IMG_MAX_DIM + IMG_MAX_DIM) * 1.0857142857142856)


def draw_image(pos, imagepath, page):
    """Draw image on the page.

    Fails silently if *imagepath* can not be opened.
    """
    try:
        print("Trying to open and paste image '{}' to the page.".format(imagepath))
        image = Image.open(imagepath)
        w, h = image.width, image.height
        ratio = IMG_MAX_DIM / w if w > h else IMG_MAX_DIM / h
        new_w, new_h = int(ratio * w), int(ratio * h)
        image = image.resize((new_w, new_h))
        page.paste(image, box=pos)
        print("Image '{}' pasted successfully.".format(imagepath))
    except:
        draw = ImageDraw.Draw(page)
        print("Image '{}' not found".format(imagepath))
        draw.text(pos, "Image not found", fill=(0, 0, 0))


def create_page(title, poem, imagepath1="", imagepath2="", imagepath3="", imagepath4="", savepath='page.jpg'):
    """Create page from the groups outputs.

    Current implementation places all groups' outputs on the same page.

    :param title: Output from group "tittles"
    :param poem: Output from group "roses"
    :param imagepath1: Output from group "random_team"
    :param imagepath2: Output from group "group_picasso"
    :param imagepath3: Output from group "graphical_group_01"
    :param imagepath4: Output from group "gpri"
    :param savepath: Path where to save the image. Defaults to: `page.jpg`
    :return: None
    """
    print("Creating a new page...")
    page = Image.new('RGB', (A4W, A4H), 'white')
    draw = ImageDraw.Draw(page)

    # Load default font so that it is found from every platform.
    font = ImageFont.load_default()

    # Draw title
    print("Placing title '{}' to the page.".format(title))
    title_width, title_height = draw.textsize(title, font=font)
    title_left_border = 0.5 * (A4W - title_width)
    draw.text((title_left_border, TITLE_TOP_BORDER), title, fill=(0, 0, 0))

    # Draw images
    draw_image((IMG_LEFT_BORDER, IMG_TOP_BORDER), imagepath1, page)
    draw_image((IMG_LEFT_BORDER+IMG_MAX_DIM, IMG_TOP_BORDER), imagepath2, page)
    draw_image((IMG_LEFT_BORDER, IMG_TOP_BORDER+IMG_MAX_DIM), imagepath3, page)
    draw_image((IMG_LEFT_BORDER+IMG_MAX_DIM, IMG_TOP_BORDER+IMG_MAX_DIM), imagepath4, page)

    # Draw poem
    print("Placing poem '{}' to the page.".format(("{}...".format(poem[:30])).replace("\n", " ")))
    poem_width, poem_height = draw.textsize(poem, font=font)
    poem_left_border = 0.5 * (A4W - poem_width)
    draw.text((poem_left_border, POEM_TOP_BORDER), poem, fill=(0, 0, 0))

    # Save image.
    page.save(savepath)
    print("Page saved to '{}'".format(savepath))


if __name__ == "__main__":
    create_page("This is a test title",
                "Roses are red,\nviolets are blue,\nI am a dummy,\nmaybe you are too?",
                "picasso.jpg",
                "babylon_drawing.jpg",
                "babylon_drawing.jpg",
                "picasso.jpg")
