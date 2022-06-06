from Gui.MergeWindow import *
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
        self.setFixedSize(250, 100)
        self.center()

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        button_merge = QPushButton("Merge", self)
        grid_layout.addWidget(button_merge)
        button_merge.clicked.connect(self.merge_window)

        button_split = QPushButton("Split", self)
        grid_layout.addWidget(button_split)
        button_split.clicked.connect(self.split_window)

    def merge_window(self):
        self.merge = MergeWindow()
        self.merge.show()
        self.close()

    def split_window(self):
        self.split = SplitGeneralWindow()
        self.split.show()
        self.close()
