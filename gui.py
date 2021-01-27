import os
import sys

from PIL import Image

from functions import *

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel


class Image2ASCII(QWidget):
    """A PyQt5 GUI that converts an image file to ASCII art"""

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
        filename, _ = QFileDialog.getOpenFileName(self, 'Select an Image to Convert', os.getenv('HOME'),
                                                  'Images (*.png *.jpeg *.jpg)', options=options)
        if (not filename):
            return

        # Create PIL image object
        self.image = resize_image(Image.open(filename))

        # Set QLabel to a pixmap made of the PIL image object
        self.pixmap = pil2pixmap(self.image)
        self.picture.setPixmap(self.pixmap)

        # Reformat GUI
        self.resize(self.pixmap.width(), self.pixmap.height())
        self.convert_btn.setEnabled(True)

    @pyqtSlot()
    def convert(self, new_width=100):
        QApplication.setOverrideCursor(Qt.WaitCursor)

        # Convert image to ascii
        new_image_data = pixels_to_ascii(grayify(self.image))

        # Format string data
        pixel_count = len(new_image_data)
        ascii_image = "\n".join([new_image_data[index:(index+new_width)]
                                 for index in range(0, pixel_count, new_width)])

        # Get save file path/name
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save ASCII Art", os.getenv('HOME'), "Text File (*.txt)", options=options)

        if (not filename):
            QApplication.restoreOverrideCursor()
            return

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
