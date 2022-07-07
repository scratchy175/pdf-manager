from Gui.MergeWindow import MergeWindow
from Gui.RotateWindow import RotateWindow
from Gui.SplitWindow import SplitWindow
from Gui.GeneralWindow import GeneralWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QVBoxLayout


class MainWindow(GeneralWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        title = "PDF Manager"

        self.setWindowIcon(QIcon("logo.png"))
        self.setWindowTitle(title)
        self.setMinimumSize(600, 400)
        self.center()

        button_merge = QPushButton("Fusionner", self)
        button_merge.clicked.connect(self.merge_window)
        button_merge.setMinimumSize(200, 50)

        button_split = QPushButton("Découper / Extraire", self)
        button_split.clicked.connect(self.split_window)
        button_split.setMinimumSize(200, 50)

        button_rotate = QPushButton("Pivoter", self)
        button_rotate.clicked.connect(self.rotate_window)
        button_rotate.setMinimumSize(200, 50)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(100, 50, 100, 50)
        layout.addWidget(button_merge, 5)
        layout.addWidget(button_split, 5)
        layout.addWidget(button_rotate, 5)

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
