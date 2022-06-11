from PyPDF2 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Gui.GeneralWindow import GeneralWindow


class RotateWindow(QMainWindow, GeneralWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowIcon(QIcon("logo.png"))
        self.setWindowTitle("Pivoter")
        self.setFixedSize(600, 530)
        self.center()

        labelSelect = QLabel(self)
        labelSelect.setText("Fichier à traiter :")
        labelSelect.setGeometry(100, 450, 300, 30)
        labelSelect.move(50, 20)

        self.textSelect = QLineEdit(self)
        self.textSelect.setGeometry(100, 100, 500, 30)
        self.textSelect.setPlaceholderText("Sélectionner un fichier : [*.pdf]")
        self.textSelect.move(50, 50)

        buttonSelect = QPushButton("Parcourir", self)
        buttonSelect.move(550, 50)
        buttonSelect.setToolTip("Sélectionner le fichier à traiter")
        buttonSelect.clicked.connect(self.browse_file)

        labelSelect = QLabel(self)
        labelSelect.setText("Pages à pivoter :")
        labelSelect.setGeometry(100, 450, 300, 30)
        labelSelect.move(50, 100)

        self.checkboxPages = QCheckBox("Toutes", self)
        self.checkboxPages.setGeometry(100, 100, 200, 30)
        self.checkboxPages.move(50, 150)
        self.checkboxPages.setToolTip("Toutes les pages")
        self.checkboxPages.stateChanged.connect(self.checkboxAllPages)

        self.textPagesToRotate = QLineEdit(self)
        self.textPagesToRotate.setGeometry(100, 100, 300, 30)
        self.textPagesToRotate.setPlaceholderText("Pages à pivoter (ex: 1-5,7,9-12)")
        self.textPagesToRotate.move(100, 150)
        self.textPagesToRotate.setEnabled(False)

        self.checkboxRotateRight = QCheckBox("Pivoter à droite", self)
        self.checkboxRotateRight.setGeometry(100, 100, 200, 30)
        self.checkboxRotateRight.move(50, 130)
        self.checkboxRotateRight.setToolTip("Sélectionner le pivot à droite")
        self.checkboxRotateRight.stateChanged.connect(self.checkboxRotation)

        self.checkboxRotateLeft = QCheckBox("Pivoter à gauche", self)
        self.checkboxRotateLeft.setGeometry(100, 100, 200, 30)
        self.checkboxRotateLeft.move(50, 130)
        self.checkboxRotateLeft.setToolTip("Sélectionner le pivot à gauche")
        self.checkboxRotateLeft.stateChanged.connect(self.checkboxRotation)

        self.checkboxRotatePersonnalised = QCheckBox("Pivot personnalisé", self)
        self.checkboxRotatePersonnalised.setGeometry(100, 100, 200, 30)
        self.checkboxRotatePersonnalised.move(50, 130)
        self.checkboxRotatePersonnalised.setToolTip("Sélectionner un pivot personnalisé")
        self.checkboxRotatePersonnalised.stateChanged.connect(self.checkboxRotation)

        self.textRotate = QLineEdit(self)
        self.textRotate.setGeometry(100, 100, 300, 30)
        self.textRotate.setPlaceholderText("Choisir le pivot en degré (ex: 180)")
        self.textRotate.move(200, 160)
        self.textRotate.setEnabled(False)

        self.button_rotate = QPushButton("Exécuter", self)
        self.button_rotate.move(self.geometry().width() - self.button_rotate.geometry().width() - 10, self.geometry().height() - 40)
        self.button_rotate.setToolTip("Pivoter les pages sélectionnées")
        self.button_rotate.clicked.connect(self.rotate)

        button_back = QPushButton("< Retour", self)
        button_back.move(10, self.geometry().height() - 40)
        button_back.setToolTip("Retourner au menu principal")
        button_back.clicked.connect(self.showMain)

        self.set_button_connections()
        self.checkboxRotateRight.setChecked(True)

    def showMain(self):
        self.main_window.show()
        self.close()

    def set_button_connections(self):
        self.textSelect.textChanged.connect(self.update_button_status)
        self.textPagesToRotate.textChanged.connect(self.update_button_status)
        self.textRotate.textChanged.connect(self.update_button_status)

    def checkboxAllPages(self):
        self.update_button_status()

        if self.checkboxRotateRight.isChecked():
            self.textPagesToRotate.setEnabled(False)
            self.checkboxRotateLeft.setChecked(False)
            self.checkboxRotatePersonnalised.setChecked(False)
        elif self.checkboxRotateLeft.isChecked():
            self.textPagesToRotate.setEnabled(False)
            self.checkboxRotateRight.setChecked(False)
            self.checkboxRotatePersonnalised.setChecked(False)
        else:
            self.checkboxRotateLeft.setChecked(False)
            self.checkboxRotateRight.setChecked(False)
            self.textPagesToRotate.setEnabled(True)

    def checkboxRotation(self):
        self.update_button_status()

        if self.checkboxPages.isChecked():
            self.textPagesToRotate.setEnabled(True)
        else:
            self.textPagesToRotate.setEnabled(False)

    def update_button_status(self):
        self.button_rotate.setDisabled(self.textSelect == "" or (self.checkboxRotatePersonnalised.isChecked() and self.textRotate == "") or (self.checkboxPages.isChecked() and self.textPagesToRotate == ""))

    def browse_file(self):
        browseFilePath, _ = QFileDialog.getSaveFileName(self, "Sélectionner un fichier", "", "PDF(*.pdf);;All Files(*.*) ")

        if browseFilePath == "":
            return
        else:
            self.textSelect.setText(browseFilePath)
            self.update_button_status()

    def rotate(self):
        output_writer = PdfFileWriter()
        rotation = 0

        if self.checkboxRotateLeft.isChecked():
            rotation = -90
        elif self.checkboxRotateRight.isChecked():
            rotation = 90
        elif self.checkboxRotatePersonnalised.isChecked():
            rotation = self.textRotate

        if rotation == 0:
            QMessageBox.information(self, "Pivotement", "Pas de rotation à effectuer")
            return

        with open(self.textSelect.text(), "rb") as inputStream:
            readInput = PdfFileReader(inputStream)

            if self.checkboxPages.isChecked():
                for i in list(range(0, readInput.numPages)):
                    output_writer.addPage(getRotatedPage(readInput, rotation, i))
            else:
                index = self.textPagesToRotate.text().split(",")

                for i in range(len(index)):
                    if "-" in index[i]:
                        start, end = index[i].split("-")

                        for j in range(int(start), int(end) + 1):
                            output_writer.addPage(getRotatedPage(readInput, rotation, j - 1))
                    else:
                        output_writer.addPage(getRotatedPage(readInput, rotation, int(index[i]) - 1))

            outputStream = open(self.textSelect.text() + "/PDFManager_Rotate.pdf", "wb")
            output_writer.write(outputStream)
            outputStream.close()

        QMessageBox.information(self, "Pivotement", "Fichier pivoté avec succès !")


def getRotatedPage(read_input, rotation, i):
    if rotation > 0:
        page = read_input.getPage(i).rotateClockwise(rotation)
    else:
        page = read_input.getPage(i).rotateCounterClockwise(rotation)

    return page
