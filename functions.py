"""
Filename: functions.py
Abstract: This python file contains all methods required, 
          in order, to convert an image file to an ASCII 
          art piece in a text file and a method to 
          convert a PIL image object to a Pixmap

          Converting an image to ASCII art:
          1. Resize the image to the desired width maintaing the original image's aspect ratio
          2. Convert the image to grayscale
          3. Convert each grayscale pixel to an ASCII character with a similar intensity
          4. Format and construct a new ascii art piece
"""

# importing image class from PIL package
from PIL import Image

# importing classes from PyQt5 package
from PyQt5.QtGui import QPixmap, QImage

# ascii characters used to build the output text
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]


def resize_image(image, new_width=100):
    """ resize image according to a new width """
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return(resized_image)


def grayify(image):
    """ convert each pixel to grayscale """
    grayscale_image = image.convert("L")
    return(grayscale_image)


def pixels_to_ascii(image):
    """ convert pixels to a string of ASCII characters """
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
    return(characters)


def save(filename, ascii_image):
    """ save ascii image to a text file """
    with open(filename, "w") as f:
        f.write(ascii_image)


def pil2pixmap(img):
    """ convert PIL object to Pixmap """
    if img.mode == "RGB":
        r, g, b = img.split()
        img = Image.merge("RGB", (b, g, r))
    elif img.mode == "RGBA":
        r, g, b, a = img.split()
        img = Image.merge("RGBA", (b, g, r, a))
    elif img.mode == "L":
        img = img.convert("RGBA")

    # convert image to RGBA if not already done
    img2 = img.convert("RGBA")
    data = img2.tobytes("raw", "RGBA")
    qim = QImage(data, img.size[0], img.size[1], QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(qim)
    return pixmap
