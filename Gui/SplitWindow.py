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
        self.setFixedSize(700, 360)
        self.center()

        labelSelect = QLabel(self)
        labelSelect.setText("Fichier à traiter :")
        labelSelect.setGeometry(100, 450, 300, 30)
        labelSelect.move(50, 20)

        self.textSelect = QLineEdit(self)
        self.textSelect.setGeometry(100, 100, 500, 30)
        self.textSelect.setPlaceholderText("Sélectionner un fichier : [*.pdf]")
        self.textSelect.move(50, 50)

        self.textSelect.dragEnterEvent = self.dragEnterEvent
        self.textSelect.dragMoveEvent = self.dragMoveEvent
        self.textSelect.dropEvent = self.dropEventFile

        buttonSelect = QPushButton("Parcourir", self)
        buttonSelect.move(550, 50)
        buttonSelect.setToolTip("Sélectionner le fichier à traiter")
        buttonSelect.clicked.connect(self.browse_file)

        self.checkboxSplit = QCheckBox("Découpage du fichier", self)
        self.checkboxSplit.setGeometry(100, 100, 200, 30)
        self.checkboxSplit.move(50, 130)
        self.checkboxSplit.setToolTip("Découpage du fichier")
        self.checkboxSplit.stateChanged.connect(self.checkboxchangedS)

        self.textSplit = QLineEdit(self)
        self.textSplit.setGeometry(100, 100, 300, 30)
        self.textSplit.setPlaceholderText("Pages à découper (ex: 3,6)")
        self.textSplit.move(200, 130)
        self.textSplit.setEnabled(False)

        self.checkboxExtract = QCheckBox("Extraction de pages", self)
        self.checkboxExtract.setGeometry(100, 100, 200, 30)
        self.checkboxExtract.move(50, 160)
        self.checkboxExtract.setToolTip("Extraction de pages")
        self.checkboxExtract.stateChanged.connect(self.checkboxchangedE)

        self.textExtract = QLineEdit(self)
        self.textExtract.setGeometry(100, 100, 300, 30)
        self.textExtract.setPlaceholderText("Pages à extraire (ex: 1-5,7,9-12)")
        self.textExtract.move(200, 160)
        self.textExtract.setEnabled(False)

        label = QLabel(self)
        label.setText("Dossier de destination :")
        label.setGeometry(60, 450, 300, 30)
        label.move(50, 220)

        self.textBrowse = QLineEdit(self)
        self.textBrowse.setGeometry(100, 100, 500, 30)
        self.textBrowse.setPlaceholderText("Sélectionner un dossier")
        self.textBrowse.move(50, 250)
        self.textBrowse.dragEnterEvent = self.dragEnterEvent
        self.textBrowse.dragMoveEvent = self.dragMoveEvent
        self.textBrowse.dropEvent = self.dropEventDir

        buttonBrowse = QPushButton("Parcourir", self)
        buttonBrowse.move(550, 250)
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
        self.textSplit.textChanged.connect(self.update_button_status)
        self.textExtract.textChanged.connect(self.update_button_status)
        self.textBrowse.textChanged.connect(self.update_button_status)

    def checkboxchangedS(self):
        self.update_button_status()

        if self.checkboxSplit.isChecked():
            self.checkboxExtract.setChecked(False)
            self.textSplit.setEnabled(True)
        else:
            self.textSplit.clear()
            self.textSplit.setEnabled(False)

    def checkboxchangedE(self):
        self.update_button_status()

        if self.checkboxExtract.isChecked():
            self.textExtract.setEnabled(True)
            self.checkboxSplit.setChecked(False)
        else:
            self.textExtract.clear()
            self.textExtract.setEnabled(False)

    def select_dir(self):
        selectDirPath = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier", "", QFileDialog.ShowDirsOnly)

        if selectDirPath == "":
            return
        else:
            self.textBrowse.setText(selectDirPath)
            self.update_button_status()

    def browse_file(self):
        browseFilePath, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier", "", "PDF(*.pdf)")

        if browseFilePath == "":
            return
        else:
            self.textSelect.setText(browseFilePath)
            self.update_button_status()

    def update_button_status(self):
        self.buttonSplit.setDisabled(self.textBrowse.text() == "" or self.textSelect.text() == "" or self.textSplit.text() == "" and self.textExtract.text() == "")

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
                if os.path.isdir(path):
                    self.textBrowse.setText(path)
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

        if self.checkboxSplit.isChecked():
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
