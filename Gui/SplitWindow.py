from genericpath import isdir

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Gui.GeneralWindow import GeneralWindow


class SplitGeneralWindow(GeneralWindow):
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
        self.center()



        self.buttonSelect = QPushButton("Selectionner", self)
        self.buttonSelect.move(600, 150)
        self.buttonSelect.setToolTip("Selectionner le fichier a traiter")
        self.buttonSelect.clicked.connect(self.browse_file)


        self.labelSelect = QLabel(self)
        self.labelSelect.setText("Fichier a traiter :")
        self.labelSelect.setGeometry(100, 450, 300, 30)
        self.labelSelect.move(100, 120)


        self.textSelect = QLineEdit(self)
        self.textSelect.setGeometry(100, 100, 500, 30)
        self.textSelect.setPlaceholderText("Sélectionner un fichier : [*.pdf]")
        self.textSelect.move(100, 150)

        self.textSelect.dragEnterEvent = self.dragEnterEvent
        self.textSelect.dragMoveEvent= self.dragMoveEvent
        self.textSelect.dropEvent = self.dropEventFile


        self.buttonSplit = QPushButton("Split", self)
        self.buttonSplit.move(600, 500)
        self.buttonSplit.setToolTip("Split le fichier PDF")
        self.buttonSplit.clicked.connect(self.split_pdf)

        self.checkboxSplit = QCheckBox("Découper les pages", self)
        self.checkboxSplit.setGeometry(100, 100, 200, 30)
        self.checkboxSplit.move(100, 300)
        self.checkboxSplit.setToolTip("Découper les pages")
        self.checkboxSplit.stateChanged.connect(self.checkboxchanged)

        self.checkboxExtract = QCheckBox("Extraire les pages", self)
        self.checkboxExtract.setGeometry(100, 100, 200, 30)
        self.checkboxExtract.move(100, 350)
        self.checkboxExtract.setToolTip("Extraire les pages")
        self.checkboxSplit.stateChanged.connect(self.checkboxchanged)

        self.textSplit = QLineEdit(self)
        self.textSplit.setGeometry(100, 100, 300, 30)
        self.textSplit.setPlaceholderText("Pages à découper (ex: 3,6)")
        self.textSplit.move(250, 300)

        self.textExtract = QLineEdit(self)
        self.textExtract.setGeometry(100, 100, 300, 30)
        self.textExtract.setPlaceholderText("Pages à extraire (ex: 1-5,7,9-12)")
        self.textExtract.move(250, 350)



        self.buttonBrowse = QPushButton("Parcourir", self)
        self.buttonBrowse.move(600, 450)
        self.buttonBrowse.setToolTip("Parcourir pour choisir le dossier de destination")
        self.buttonBrowse.clicked.connect(self.select_dir)


        self.label = QLabel(self)
        self.label.setText("Dossier de destination :")
        self.label.setGeometry(100, 450, 300, 30)
        self.label.move(100, 420)


        self.textBrowse = QLineEdit(self)
        self.textBrowse.setGeometry(100, 100, 500, 30)
        self.textBrowse.setPlaceholderText("Sélectionner un dossier")
        self.textBrowse.move(100, 450)

        self.textBrowse.dragEnterEvent = self.dragEnterEvent
        self.textBrowse.dragMoveEvent= self.dragMoveEvent
        self.textBrowse.dropEvent = self.dropEventDir

    def checkboxchanged(self):
        if self.checkboxSplit.isChecked():
            self.textSplit.setEnabled(True)
            #self.checkboxExtract.setChecked(False)
        else:
            self.textSplit.setEnabled(False)

        if self.checkboxExtract.isChecked():
            self.textExtract.setEnabled(True)
            #self.checkboxSplit.setChecked(False)
        else:
            self.textExtract.setEnabled(False)




    def select_dir(self):
        self.browseDirPath = QFileDialog.getExistingDirectory(self, "Selectioner un dossier", "", QFileDialog.ShowDirsOnly)
        if self.browseDirPath == "":
            return
        else:
            self.textBrowse.setText(self.browseDirPath)


    def browse_file(self):
        self.browseFilePath, _ = QFileDialog.getOpenFileName(self, "Selectioner un fichier", "", "PDF(*.pdf)")

        if self.browseFilePath == "":
            return
        else:
            self.textSelect.setText(self.browseFilePath)

    def split_pdf(self):
        pass


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEventFile(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            urls = event.mimeData().urls()
            path = urls[0].toLocalFile()
            if len(urls) == 1:
                if path and path.endswith(".pdf"):

                    self.textSelect.setText(path)
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEventDir(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            urls = event.mimeData().urls()
            path = urls[0].toLocalFile()
            if len(urls) == 1:
                if isdir(path):
                    self.textBrowse.setText(path)
            else:
                event.ignore()
        else:
            event.ignore()