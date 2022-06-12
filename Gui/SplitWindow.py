import os
from PyPDF2 import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Gui.GeneralWindow import GeneralWindow


class SplitWindow(QMainWindow, GeneralWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowIcon(QIcon("logo.png"))
        self.setWindowTitle("Découper ou Extraire")
        self.setFixedSize(600, 320)
        self.center()

        labelSelect = QLabel(self)
        labelSelect.setText("Fichier à traiter :")
        labelSelect.setGeometry(100, 450, 300, 30)
        labelSelect.move(50, 20)

        self.textSelect = QLineEdit(self)
        self.textSelect.setGeometry(100, 100, 400, 30)
        self.textSelect.setPlaceholderText("Sélectionner un fichier : [*.pdf]")
        self.textSelect.move(50, 50)

        self.textSelect.dragEnterEvent = self.dragEnterEvent
        self.textSelect.dragMoveEvent = self.dragMoveEvent
        self.textSelect.dropEvent = self.dropEventFile

        buttonSelect = QPushButton("Parcourir", self)
        buttonSelect.move(450, 50)
        buttonSelect.setToolTip("Sélectionner le fichier à traiter")
        buttonSelect.clicked.connect(self.browse_file)

        self.radioButtonSplit = QRadioButton("Découpage du fichier", self)
        self.radioButtonSplit.setGeometry(100, 100, 200, 30)
        self.radioButtonSplit.move(50, 100)
        self.radioButtonSplit.setToolTip("Découpage du fichier")
        self.radioButtonSplit.toggled.connect(self.radioButtonChanged)

        self.textSplit = QLineEdit(self)
        self.textSplit.setGeometry(100, 100, 300, 30)
        self.textSplit.setPlaceholderText("Pages à découper (ex: 3,6)")
        self.textSplit.move(200, 100)
        self.textSplit.setEnabled(False)

        self.radioButtonExtract = QRadioButton("Extraction de pages", self)
        self.radioButtonExtract.setGeometry(100, 100, 200, 30)
        self.radioButtonExtract.move(50, 130)
        self.radioButtonExtract.setToolTip("Extraction de pages")
        self.radioButtonExtract.toggled.connect(self.radioButtonChanged)

        self.textExtract = QLineEdit(self)
        self.textExtract.setGeometry(100, 100, 300, 30)
        self.textExtract.setPlaceholderText("Pages à extraire (ex: 1-5,7,9-12)")
        self.textExtract.move(200, 130)
        self.textExtract.setEnabled(False)

        label = QLabel(self)
        label.setText("Dossier de destination :")
        label.setGeometry(60, 450, 300, 30)
        label.move(50, 180)

        self.textBrowse = QLineEdit(self)
        self.textBrowse.setGeometry(100, 100, 400, 30)
        self.textBrowse.setPlaceholderText("Sélectionner un dossier")
        self.textBrowse.move(50, 210)
        self.textBrowse.dragEnterEvent = self.dragEnterEvent
        self.textBrowse.dragMoveEvent = self.dragMoveEvent
        self.textBrowse.dropEvent = self.dropEventDir

        buttonBrowse = QPushButton("Parcourir", self)
        buttonBrowse.move(450, 210)
        buttonBrowse.setToolTip("Sélectionner un dossier de destination")
        buttonBrowse.clicked.connect(self.select_dir)

        button_back = QPushButton("< Retour", self)
        button_back.move(10, self.geometry().height() - 40)
        button_back.setToolTip("Retourner au menu principal")
        button_back.clicked.connect(self.showMain)

        self.buttonSplit = QPushButton("Exécuter", self)
        self.buttonSplit.move(self.geometry().width() - self.buttonSplit.geometry().width() - 10, self.geometry().height() - 40)
        self.buttonSplit.setToolTip("Exécution")
        self.buttonSplit.clicked.connect(self.split)

        self.set_button_connections()
        self.update_button_status()

    def showMain(self):
        self.main_window.show()
        self.close()

    def set_button_connections(self):
        self.textSelect.textChanged.connect(self.update_button_status)
        self.textSplit.textChanged.connect(self.update_button_status)
        self.textExtract.textChanged.connect(self.update_button_status)
        self.textBrowse.textChanged.connect(self.update_button_status)

    def radioButtonChanged(self):
        self.update_button_status()
        self.textSplit.setEnabled(self.radioButtonSplit.isChecked())
        self.textExtract.setEnabled(self.radioButtonExtract.isChecked())

    def browse_file(self):
        browseFilePath, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier", "", "PDF(*.pdf)")

        if browseFilePath == "":
            return
        else:
            self.textSelect.setText(browseFilePath)
            self.update_button_status()

    def select_dir(self):
        selectDirPath = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier", "", QFileDialog.ShowDirsOnly)

        if selectDirPath == "":
            return
        else:
            self.textBrowse.setText(selectDirPath)
            self.update_button_status()

    def update_button_status(self):
        self.buttonSplit.setEnabled((self.textSelect.text() != "" and os.path.isfile(self.textSelect.text())) and
                                    (self.textBrowse.text() != "" and os.path.isdir(self.textBrowse.text())) and
                                    (self.radioButtonSplit.isChecked() and self.textSplit.text() != "") or
                                    (self.radioButtonExtract.isChecked() and self.textExtract.text() != ""))

    def dropEventFile(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            urls = event.mimeData().urls()
            filePath = urls[0].toLocalFile()

            if len(urls) == 1:
                if filePath and filePath.endswith(".pdf"):
                    self.textSelect.setText(filePath)
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEventDir(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            urls = event.mimeData().urls()
            pathDir = urls[0].toLocalFile()

            if len(urls) == 1:
                if os.path.isdir(pathDir):
                    self.textBrowse.setText(pathDir)
            else:
                event.ignore()
        else:
            event.ignore()

    def split(self):
        try:
            readInput = PdfReader(self.textSelect.text())
        except:
            QMessageBox.critical(self, "Erreur", "Fichier invalide")
            return

        if self.radioButtonSplit.isChecked():
            index = self.textSplit.text().split(",")
            index.insert(0, str(0))
            index.append(str(readInput.getNumPages()))

            for i in range(len(index) - 1):
                output = PdfFileWriter()

                for j in range(int(index[i]), int(index[i + 1])):
                    output.addPage(readInput.getPage(j))

                outputStream = open(self.textBrowse.text() + "/PDFManager_Split_" + str(i) + ".pdf", "wb")
                output.write(outputStream)
                outputStream.close()

            QMessageBox.information(self, "Découpage", "Fichier découpé avec succès")
        else:
            output = PdfFileWriter()
            index = self.textExtract.text().split(",")

            for i in range(len(index)):
                if "-" in index[i]:
                    start, end = index[i].split("-")

                    for j in range(int(start), int(end) + 1):
                        output.addPage(readInput.getPage(j - 1))
                else:
                    output.addPage(readInput.getPage(int(index[i]) - 1))

            outputStream = open(self.textBrowse.text() + "/PDFManager_Extract" + ".pdf", "wb")
            output.write(outputStream)
            outputStream.close()
            QMessageBox.information(self, "Extraction", "Fichier(s) extrait(s) avec succès.")
