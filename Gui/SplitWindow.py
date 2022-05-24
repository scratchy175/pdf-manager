from PyPDF2 import PdfFileMerger
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class SplitWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "Split PDF"
        top = 400
        left = 400
        width = 800
        height = 600

        self.setWindowIcon(QIcon("logo.png"))
        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)