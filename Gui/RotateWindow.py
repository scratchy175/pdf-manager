from PyPDF2 import PdfFileReader, PdfFileWriter
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (QGridLayout, QLabel, QCheckBox,
                             QRadioButton, QFileDialog, QMessageBox)
from Gui.GeneralWindow import CustomLineEdit, GeneralWindow


class RotateWindow(GeneralWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pivoter")
        self.center()

        layout = QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(50, 50, 50, 50)
        self.setup_select(layout, 0)
        self.setup_back_exec(layout, 11, self.rotate)

        labelPages = QLabel(self)
        labelPages.setText("Pages à pivoter :")

        self.checkboxPages = QCheckBox("Toutes", self)
        self.checkboxPages.setToolTip("Toutes les pages")
        self.checkboxPages.stateChanged.connect(self.checkboxAllPages)

        self.textPagesToRotate = CustomLineEdit("Pages à pivoter (ex: 1-5,7,9-12)", False)
        self.textPagesToRotate.setValidator(QRegExpValidator(QRegExp("(([1-9]\\d*,)|([1-9]\\d*-[1-9]\\d*,))+")))
        self.textPagesToRotate.textChanged.connect(self.update_button_status)
        self.textPagesToRotate.setMaximumWidth(100)

        labelRotate = QLabel(self)
        labelRotate.setText("Rotation :")

        self.checkboxRotateRight = QRadioButton("Pivoter de 90° à droite", self)
        self.checkboxRotateRight.setToolTip("Sélectionner la rotation à droite")

        self.checkboxRotateLeft = QRadioButton("Pivoter de 90° à gauche", self)
        self.checkboxRotateLeft.setToolTip("Sélectionner la rotation à gauche")

        self.checkboxRotateInversed = QRadioButton("Pivoter de 180°", self)
        self.checkboxRotateInversed.setToolTip("Sélectionner la rotation de 180°")

        self.checkboxPages.setChecked(True)
        self.checkboxRotateRight.setChecked(True)

        layout.addWidget(labelPages, 3, 0)
        layout.addWidget(self.checkboxPages, 4, 0)
        layout.addWidget(self.textPagesToRotate, 4, 1)
        layout.addWidget(labelRotate, 6, 0)
        layout.addWidget(self.checkboxRotateRight, 7, 0, 1, 3)
        layout.addWidget(self.checkboxRotateLeft, 8, 0, 1, 3)
        layout.addWidget(self.checkboxRotateInversed, 9, 0, 1, 3)
        layout.setRowMinimumHeight(2, 20)
        layout.setRowMinimumHeight(5, 20)
        layout.setRowMinimumHeight(10, 20)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(5, 1)
        layout.setRowStretch(10, 1)
        layout.setColumnMinimumWidth(0, 10)

    def checkboxAllPages(self):
        self.textPagesToRotate.setDisabled(self.checkboxPages.isChecked())
        self.update_button_status()
        if self.checkboxPages.isChecked():
            self.textPagesToRotate.clear()

    def update_button_status(self):
        self.button_exec.setEnabled(self.check_select_status() and (self.checkboxPages.isChecked() or (self.textPagesToRotate.text() != "" and self.textPagesToRotate.text()[-1].isdigit())))

    def rotate(self):
        readInput = PdfFileReader(self.textSelect.text())
        output_writer = PdfFileWriter()
        if readInput.isEncrypted:
            QMessageBox.warning(self, "Fichier encrypté", "Le fichier est encrypté, impossible de le pivoter")
            return
        nbpages = readInput.getNumPages()
        rotation = self.selectedRotation()
        outpath = QFileDialog.getSaveFileName(self, "Sélectionner le fichier de sortie", "", "PDF(*.pdf)")[0]
        if outpath == "":
            return
        if self.checkboxPages.isChecked():
            for i in range(nbpages):
                output_writer.addPage(readInput.getPage(i).rotate(rotation))
        else:
            listPages = self.setupPagesToRotate()
            self.checkIndex(listPages, nbpages)
            for i in range(nbpages):
                if i+1 in listPages:
                    output_writer.addPage(readInput.getPage(i).rotate(rotation))
                else:
                    output_writer.addPage(readInput.getPage(i))
        with open(outpath, "wb") as outputStream:
            output_writer.write(outputStream)
        QMessageBox.information(self, "Pivotement", "Fichier pivoté avec succès !")

    def selectedRotation(self):
        if self.checkboxRotateLeft.isChecked(): 
            return -90
        elif self.checkboxRotateRight.isChecked():
            return 90
        elif self.checkboxRotateInversed.isChecked():
            return 180

    def setupPagesToRotate(self):
        index = self.textPagesToRotate.text().split(",")
        setPagesToRotate = set()
        for val in index:
            if "-" in val:
                start, end = val.split("-")
                for j in range(int(start), int(end) + 1):
                    setPagesToRotate.add(j)
            else:
                setPagesToRotate.add(int(val))
        return setPagesToRotate

    def checkIndex(self, listPages, nbpages):
        if max(listPages) > nbpages:
            QMessageBox.warning(self, "Numéro de page invalide", "Veuillez entrer des numéros de page valide")
            return
