from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Gui.MergeWindow import *
from Gui.SplitWindow import *

# creating class for window
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
 
 
        title = "PDF Manager"
 
        top = 400
        left = 400
        width = 800
        height = 600
 
        self.setWindowIcon(QIcon("logo.png"))

        # setting title of window
        self.setWindowTitle(title)
 
        # setting geometry
        self.setGeometry(top, left, width, height)
 
        # creating canvas
        self.image = QImage(self.size(), QImage.Format_RGB32)
 
        # setting canvas color to white
        self.image.fill(Qt.white)

 
        button_merge = QPushButton("Merge", self)
        button_merge.move(100, 100)
        button_merge.setToolTip("This is a <b>QPushButton</b> widget")
        button_merge.clicked.connect(self.merge_window)

        button_split = QPushButton("Split", self)
        button_split.move(100, 150)
        button_split.setToolTip("split PDF")
        button_split.clicked.connect(self.split_window)
     

    def merge_window(self):
        self.merge = MergeWindows()
        self.merge.show()
        self.close()

    def split_window(self):
        self.split = SplitWindow()
        self.split.show()
        self.close()