import os
from os import path

from PyPDF2 import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Gui.GeneralWindow import GeneralWindow


class RotateWindow(QMainWindow, GeneralWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowIcon(QIcon("logo.png"))
        self.setWindowTitle("Pivoter")
        self.setFixedSize(600, 450)
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

        labelPages = QLabel(self)
        labelPages.setText("Pages à pivoter :")
        labelPages.setGeometry(100, 450, 300, 30)
        labelPages.move(50, 100)

        self.checkboxPages = QCheckBox("Toutes", self)
        self.checkboxPages.setGeometry(100, 100, 200, 30)
        self.checkboxPages.move(50, 130)
        self.checkboxPages.setToolTip("Toutes les pages")
        self.checkboxPages.stateChanged.connect(self.checkboxAllPages)

        self.textPagesToRotate = QLineEdit(self)
        self.textPagesToRotate.setGeometry(100, 100, 300, 30)
        self.textPagesToRotate.setPlaceholderText("Pages à pivoter (ex: 1-5,7,9-12)")
        self.textPagesToRotate.move(130, 130)
        self.textPagesToRotate.setEnabled(False)

        labelRotate = QLabel(self)
        labelRotate.setText("Rotation :")
        labelRotate.setGeometry(100, 450, 300, 30)
        labelRotate.move(50, 180)

        self.checkboxRotateRight = QRadioButton("Pivoter de 90° à droite", self)
        self.checkboxRotateRight.setGeometry(100, 100, 200, 30)
        self.checkboxRotateRight.move(50, 210)
        self.checkboxRotateRight.setToolTip("Sélectionner la rotation à droite")

        self.checkboxRotateLeft = QRadioButton("Pivoter de 90° à gauche", self)
        self.checkboxRotateLeft.setGeometry(100, 100, 200, 30)
        self.checkboxRotateLeft.move(50, 240)
        self.checkboxRotateLeft.setToolTip("Sélectionner la rotation à gauche")

        self.checkboxRotateInversed = QRadioButton("Pivoter de 180°", self)
        self.checkboxRotateInversed.setGeometry(100, 100, 200, 30)
        self.checkboxRotateInversed.move(50, 270)
        self.checkboxRotateInversed.setToolTip("Sélectionner la rotation de 180°")

        label = QLabel(self)
        label.setText("Dossier de destination :")
        label.setGeometry(60, 450, 300, 30)
        label.move(50, 320)

        self.textBrowse = QLineEdit(self)
        self.textBrowse.setGeometry(100, 100, 400, 30)
        self.textBrowse.setPlaceholderText("Sélectionner un dossier")
        self.textBrowse.move(50, 350)
        self.textBrowse.dragEnterEvent = self.dragEnterEvent
        self.textBrowse.dragMoveEvent = self.dragMoveEvent
        self.textBrowse.dropEvent = self.dropEventDir

        buttonBrowse = QPushButton("Parcourir", self)
        buttonBrowse.move(450, 350)
        buttonBrowse.setToolTip("Sélectionner un dossier de destination")
        buttonBrowse.clicked.connect(self.select_dir)

        self.button_rotate = QPushButton("Exécuter", self)
        self.button_rotate.move(self.geometry().width() - self.button_rotate.geometry().width() - 10,
                                self.geometry().height() - 40)
        self.button_rotate.setToolTip("Pivoter les pages sélectionnées")
        self.button_rotate.clicked.connect(self.rotate)

        button_back = QPushButton("< Retour", self)
        button_back.move(10, self.geometry().height() - 40)
        button_back.setToolTip("Retourner au menu principal")
        button_back.clicked.connect(self.showMain)

        self.set_button_connections()
        self.checkboxPages.setChecked(True)
        self.checkboxRotateRight.setChecked(True)

    def showMain(self):
        self.main_window.show()
        self.close()

    def set_button_connections(self):
        self.textSelect.textChanged.connect(self.update_button_status)
        self.textPagesToRotate.textChanged.connect(self.update_button_status)

    def checkboxAllPages(self):
        self.update_button_status()
        self.textPagesToRotate.setDisabled(self.checkboxPages.isChecked())

    def update_button_status(self):
        self.button_rotate.setEnabled((self.textSelect.text() != "" and path.isfile(self.textSelect.text())) and
                                      (self.checkboxPages.isChecked() or self.textPagesToRotate.text() != "") and
                                      (self.textBrowse.text() != "" and path.isdir(self.textBrowse.text())))

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

    def rotate(self):
        output_writer = PdfFileWriter()
        rotation = 0
        error = 0

        if self.checkboxRotateLeft.isChecked():
            rotation = -90
        elif self.checkboxRotateRight.isChecked():
            rotation = 90
        elif self.checkboxRotateInversed.isChecked():
            rotation = 180

        if rotation == 0:
            QMessageBox.information(self, "Pivotement", "Pas de rotation à effectuer")
            return

        with open(self.textSelect.text(), "rb") as inputStream:
            readInput = PdfFileReader(inputStream)

            if self.checkboxPages.isChecked():
                for i in list(range(0, readInput.numPages)):
                    output_writer.addPage(readInput.getPage(i).rotateClockwise(rotation))
            else:
                index = self.textPagesToRotate.text().split(",")

                for i in range(len(index)):
                    try:
                        if "-" in index[i]:
                            start, end = index[i].split("-")
                            start = checkPage(start, readInput.numPages)
                            end = checkPage(end, readInput.numPages)

                            if i == 0 and start > 1:
                                for j in range(0, start - 1):
                                    output_writer.addPage(readInput.getPage(j))

                            for j in range(start, end + 1):
                                output_writer.addPage(readInput.getPage(j - 1).rotateClockwise(rotation))

                            if i == len(index) - 1:
                                if end < readInput.numPages:
                                    for j in range(end, readInput.numPages):
                                        output_writer.addPage(readInput.getPage(j))
                            else:
                                printUntilNext(readInput, output_writer, index, end, i)
                        else:
                            pageNum = checkIndexPage(index, i, readInput.numPages)

                            if i == 0 and int(index[0]) > 1:
                                for j in range(0, pageNum - 1):
                                    output_writer.addPage(readInput.getPage(j))

                            output_writer.addPage(readInput.getPage(pageNum - 1).rotateClockwise(rotation))

                            if i == len(index) - 1:
                                if pageNum < readInput.numPages:
                                    for j in range(pageNum, readInput.numPages):
                                        output_writer.addPage(readInput.getPage(j))
                            else:
                                printUntilNext(readInput, output_writer, index, pageNum, i)
                    except PageValueError:
                        QMessageBox.warning(self, "Numéro de page invalide", "Veuillez entrer des numéros de page valide")
                        error = 1

            if error != 1:
                outputStream = open(self.textBrowse.text() + "/PDFManager_Rotate.pdf", "wb")
                output_writer.write(outputStream)
                outputStream.close()
                QMessageBox.information(self, "Pivotement", "Fichier pivoté avec succès !")


def printUntilNext(read_input, output_writer, index, end, i):
    if "-" in index[i + 1]:
        nextStart, nextEnd = index[i + 1].split("-")
        nextStart = checkPage(nextStart, read_input.numPages)

        if end < nextStart - 1:
            for j in range(end, nextStart - 1):
                output_writer.addPage(read_input.getPage(j))
    else:
        nextPage = checkIndexPage(index, i + 1, read_input.numPages)

        if end < nextPage:
            for j in range(end, nextPage - 1):
                output_writer.addPage(read_input.getPage(j))


def checkPage(page, max_page):
    int_page = int(page)

    if 0 < int_page <= max_page:
        return int_page
    else:
        raise PageValueError


def checkIndexPage(index, i, max_page):
    page = int(index[i])

    if 0 < page <= max_page:
        return page
    else:
        raise PageValueError


class PageValueError(Exception):
    pass
