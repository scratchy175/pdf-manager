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
        self.textPagesToRotate.setValidator(QRegExpValidator(QRegExp("[1-9]\\d*((\\,|\\-)[1-9]\\d*)+")))
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

    def update_button_status(self):
        self.button_exec.setEnabled(self.check_select_status() and (self.checkboxPages.isChecked() or self.textPagesToRotate.text() != ""))

    def rotate(self):
        outpath = QFileDialog.getSaveFileName(self, "Sélectionner le fichier de sortie", "", "PDF(*.pdf)")[0]
        if outpath == "":
            return
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
                pageSet = set(())

                for page in index:
                    if "-" in page:
                        start, end = page.split("-")

                        for i in range(int(start), int(end) + 1):
                            pageSet.add(i)
                    else:
                        pageSet.add(int(page))

                sortedList = sorted(pageSet)

                try:
                    for page in range(len(sortedList)):
                        pageNum = checkIndexPage(sortedList, page, readInput.numPages)

                        if page == 0 and int(sortedList[0]) > 1:
                            for j in range(0, pageNum - 1):
                                output_writer.addPage(readInput.getPage(j))

                        output_writer.addPage(readInput.getPage(pageNum - 1).rotateClockwise(rotation))

                        if page == len(sortedList) - 1:
                            if pageNum < readInput.numPages:
                                for j in range(pageNum, readInput.numPages):
                                    output_writer.addPage(readInput.getPage(j))
                        else:
                            printUntilNext(readInput, output_writer, sortedList, pageNum, page)
                except PageValueError:
                    QMessageBox.warning(self, "Numéro de page invalide", "Veuillez entrer des numéros de page valide")
                    error = 1

            if error != 1:
                outputStream = open(outpath, "wb")
                output_writer.write(outputStream)
                outputStream.close()
                QMessageBox.information(self, "Pivotement", "Fichier pivoté avec succès !")


def printUntilNext(read_input, output_writer, sorted_list, end, i):
    nextPage = checkIndexPage(sorted_list, i + 1, read_input.numPages)

    if end < nextPage:
        for j in range(end, nextPage - 1):
            output_writer.addPage(read_input.getPage(j))


def checkIndexPage(sorted_list, i, max_page):
    page = int(sorted_list[i])

    if 0 < page <= max_page:
        return page
    else:
        raise PageValueError


class PageValueError(Exception):
    pass
