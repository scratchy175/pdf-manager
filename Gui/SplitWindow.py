import os

from PyPDF2 import PdfFileReader, PdfFileWriter
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QFileDialog, QGridLayout, QMessageBox, QRadioButton

from Gui.GeneralWindow import CustomLineEdit, GeneralWindow
from utils import *


class SplitWindow(GeneralWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Découper ou Extraire")
        self.setMaximumHeight(0)
        self.center()

        layout = QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(50, 50, 50, 50)
        self.setup_select(layout, 0)
        self.setup_back_exec(layout, 7, self.exec)

        self.radioButtonSplit = QRadioButton("Découpage du fichier", self)
        self.radioButtonSplit.toggled.connect(self.radioButtonChanged)

        self.textSplit = CustomLineEdit("Pages à découper (ex: 3,6)", False)
        self.textSplit.textChanged.connect(self.update_button_status)
        self.textSplit.setValidator(QRegExpValidator(QRegExp("([1-9]\\d*,)+")))
        self.textSplit.setMaximumWidth(100)

        self.radioButtonExtract = QRadioButton("Extraction de pages", self)
        self.radioButtonExtract.toggled.connect(self.radioButtonChanged)

        self.textExtract = CustomLineEdit("Pages à extraire (ex: 1-5,7,9-12)", False)
        self.textExtract.textChanged.connect(self.update_button_status)
        self.textExtract.setValidator(QRegExpValidator(QRegExp("(([1-9]\\d*,)|([1-9]\\d*-[1-9]\\d*,))+")))
        self.textExtract.setMaximumWidth(100)

        self.splitAll = QRadioButton("Découper toutes les pages", self)
        self.splitAll.toggled.connect(self.radioButtonChanged)

        layout.addWidget(self.splitAll, 3, 0)
        layout.addWidget(self.radioButtonSplit, 4, 0)
        layout.addWidget(self.textSplit, 4, 1)
        layout.addWidget(self.radioButtonExtract, 5, 0)
        layout.addWidget(self.textExtract, 5, 1)
        layout.setRowMinimumHeight(2, 20)
        layout.setRowMinimumHeight(6, 20)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(6, 1)
        layout.setColumnMinimumWidth(0, 10)

        self.update_button_status()

    def update_button_status(self):
        self.button_exec.setEnabled((self.check_select_status()) and
                                    ((self.radioButtonSplit.isChecked() and self.textSplit.text() != "" and self.textSplit.text()[-1].isdigit()) or
                                    (self.radioButtonExtract.isChecked() and self.textExtract.text() != "" and self.textExtract.text()[-1].isdigit()) or self.splitAll.isChecked()))

    def radioButtonChanged(self):
        self.update_button_status()
        self.textSplit.setEnabled(self.radioButtonSplit.isChecked())
        self.textExtract.setEnabled(self.radioButtonExtract.isChecked())
        if self.radioButtonSplit.isChecked():
            self.textExtract.clear()
        elif self.radioButtonExtract.isChecked():
            self.textSplit.clear()
        else:
            self.textSplit.clear()
            self.textExtract.clear()

    def exec(self):
        readInput = PdfFileReader(self.textSelect.text(), "rb")
        outpath = QFileDialog.getSaveFileName(self, "Sélectionner le fichier de sortie", "", "PDF(*.pdf)")[0]
        if outpath == "":
            return
        if self.radioButtonSplit.isChecked():
            self.split(readInput, outpath)
        elif self.radioButtonExtract.isChecked():
            self.extract(readInput, outpath)
        else:
            self.splitAllPages(readInput, outpath)

    def split(self, readInput, outpath):
        nbpages = readInput.getNumPages()
        listPages = setupList(self.textSplit)
        listPages.insert(0, 0)
        listPages.append(nbpages)
        if checkIndex(self, listPages, nbpages):
            return
        for i in range(len(listPages) - 1):
            output = PdfFileWriter()

            for j in range(listPages[i], listPages[i + 1]):
                output.addPage(readInput.getPage(j))

            root = os.path.splitext(outpath)[0]
            with open(root + str(i) + ".pdf", "wb") as outputStream:
                output.write(outputStream)
        QMessageBox.information(self, "Découpage", "Fichier découpé avec succès !")

    def extract(self, readInput, outpath):
        output = PdfFileWriter()
        nbpages = readInput.getNumPages()
        listPages = setupList(self.textExtract)
        if checkIndex(self, listPages, nbpages):
            return 
        for i in range(len(listPages)):
            output.addPage(readInput.getPage(listPages[i]))
        with open(outpath, "wb") as outputStream:
            output.write(outputStream)
        QMessageBox.information(self, "Extraction", "Pages extraites avec succès !")

    def splitAllPages(self, readInput, outpath):   
        for i in range(readInput.getNumPages()):
            output = PdfFileWriter()
            output.addPage(readInput.getPage(i))
            root = os.path.splitext(outpath)[0]
            with open(root + str(i) + ".pdf", "wb") as outputStream:
                output.write(outputStream)
        QMessageBox.information(self, "Découpage", "Fichier découpé avec succès !")