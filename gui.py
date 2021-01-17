import sys

from PIL import Image

from functions import *

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel


def pil2pixmap(img):
    """ Convert Pillow Object to Pixmap """
    if img.mode == "RGB":
        r, g, b = img.split()
        img = Image.merge("RGB", (b, g, r))
    elif img.mode == "RGBA":
        r, g, b, a = img.split()
        img = Image.merge("RGBA", (b, g, r, a))
    elif img.mode == "L":
        img = img.convert("RGBA")

    # Convert image to RGBA if not already done
    img2 = img.convert("RGBA")
    data = img2.tobytes("raw", "RGBA")
    qim = QImage(data, img.size[0], img.size[1], QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(qim)
    return pixmap


class Image2ASCII(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("icon.png"))

        self.setWindowTitle("ASCII Art")

        self.left = 500
        self.top = 200
        self.width = 400
        self.height = 300

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.prompt = QLabel(
            'Hi, select an image from\nyour personal files to convert')
        self.prompt.setAlignment(Qt.AlignCenter)

        self.picture = QLabel()
        self.picture.setAlignment(Qt.AlignCenter)

        self.select_btn = QPushButton("Select Image")
        self.select_btn.clicked.connect(self.getImage)

        self.convert_btn = QPushButton("Create ASCII Art")
        self.convert_btn.setEnabled(False)
        self.convert_btn.clicked.connect(self.convert)

        vbox = QVBoxLayout()

        vbox.addWidget(self.prompt)
        vbox.addWidget(self.picture)
        vbox.addWidget(self.select_btn)
        vbox.addWidget(self.convert_btn)

        self.setLayout(vbox)

    @pyqtSlot()
    def getImage(self):
        # Get image file from file dialogue
        options = QFileDialog.Options()
        self.path, _ = QFileDialog.getOpenFileName(self, 'Select an Image to Convert', '',
                                                   'Images (*.png *.jpeg *.jpg)', options=options)
        if (not self.path):
            return

        # Create PIL image object
        self.image = resize_image(Image.open(self.path))

        # Set QLabel to a pixmap made of the PIL image object
        self.pixmap = pil2pixmap(self.image)
        self.picture.setPixmap(self.pixmap)

        # Reformat GUI
        self.resize(self.pixmap.width(), self.pixmap.height())
        self.convert_btn.setEnabled(True)

    @pyqtSlot()
    def convert(self, new_width=100):
        QApplication.setOverrideCursor(Qt.WaitCursor)

        filename = self.path.split('/')[-1].split('.')[-2]

        # Convert image to ascii
        new_image_data = pixels_to_ascii(grayify(self.image))

        # Format string data
        pixel_count = len(new_image_data)
        ascii_image = "\n".join([new_image_data[index:(index+new_width)]
                                 for index in range(0, pixel_count, new_width)])
        # Save result
        save(filename, ascii_image)

        # Reformat GUI
        self.convert_btn.setEnabled(False)
        self.picture.setText("ASCII Art Saved!")

        QApplication.restoreOverrideCursor()


App = QApplication(sys.argv)
window = Image2ASCII()
window.show()
sys.exit(App.exec())
