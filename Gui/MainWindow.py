from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QPushButton, QVBoxLayout

from Gui.GeneralWindow import GeneralWindow
from Gui.MergeWindow import MergeWindow
from Gui.RotateWindow import RotateWindow
from Gui.SplitWindow import SplitWindow


class MainWindow(GeneralWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        title = "PDF Manager"

        self.setWindowIcon(QIcon("logo.png"))
        self.setWindowTitle(title)
        self.setFixedSize(400, 200)
        
        self.center()

        button_merge = QPushButton("Fusionner", self)
        button_merge.clicked.connect(self.merge_window)
        button_merge.setFont(QFont("Roboto", 15))
        button_merge.setMinimumSize(200, 50)

        button_split = QPushButton("Découper / Extraire", self)
        button_split.clicked.connect(self.split_window)
        button_split.setFont(QFont("Roboto", 15))
        button_split.setMinimumSize(200, 50)

        button_rotate = QPushButton("Pivoter", self)
        button_rotate.clicked.connect(self.rotate_window)
        button_rotate.setFont(QFont("Roboto", 15))
        button_rotate.setMinimumSize(200, 50)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(button_merge)
        layout.addWidget(button_split)
        layout.addWidget(button_rotate)

    def merge_window(self):
        self.merge = MergeWindow(self)
        self.merge.show()
        self.close()

    def split_window(self):
        self.split = SplitWindow(self)
        self.split.show()
        self.close()

    def rotate_window(self):
        self.rotate = RotateWindow(self)
        self.rotate.show()
        self.close()
