from Gui.MergeWindow import *
from Gui.RotateWindow import RotateWindow
from Gui.SplitWindow import *
from Gui.GeneralWindow import GeneralWindow


class MainWindow(GeneralWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        title = "PDF Manager"

        self.setWindowIcon(QIcon("logo.png"))
        self.setWindowTitle(title)
        self.setFixedSize(250, 120)
        self.center()

        button_merge = QPushButton("Fusionner", self)
        button_merge.clicked.connect(self.merge_window)

        button_split = QPushButton("Découper / Extraire", self)
        button_split.clicked.connect(self.split_window)

        button_rotate = QPushButton("Pivoter", self)
        button_rotate.clicked.connect(self.rotate_window)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(button_merge)
        layout.addWidget(button_split)
        layout.addWidget(button_rotate)

    def merge_window(self):
        merge = MergeWindow(self)
        merge.show()
        self.close()

    def split_window(self):
        split = SplitWindow(self)
        split.show()
        self.close()

    def rotate_window(self):
        rotate = RotateWindow(self)
        rotate.show()
        #self.close()
