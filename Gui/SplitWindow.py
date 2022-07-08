from PyPDF2 import PdfReader, PdfFileWriter
from PyQt5.QtWidgets import QRadioButton, QGridLayout, QMessageBox, QFileDialog
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from Gui.GeneralWindow import CustomLineEdit, GeneralWindow
import os


class SplitWindow(GeneralWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Découper ou Extraire")
        self.center()

        layout = QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(50, 50, 50, 50)
        self.setup_select(layout, 0)
        self.setup_back_exec(layout, 6, self.split)

        self.radioButtonSplit = QRadioButton("Découpage du fichier", self)
        self.radioButtonSplit.setToolTip("Découpage du fichier")
        self.radioButtonSplit.toggled.connect(self.radioButtonChanged)

        self.textSplit = CustomLineEdit("Pages à découper (ex: 3,6)", False)
        self.textSplit.textChanged.connect(self.update_button_status)
        self.textSplit.setValidator(QRegExpValidator(QRegExp("([1-9]\\d*,)+")))
        self.textSplit.setMaximumWidth(100)

        self.radioButtonExtract = QRadioButton("Extraction de pages", self)
        self.radioButtonExtract.setToolTip("Extraction de pages")
        self.radioButtonExtract.toggled.connect(self.radioButtonChanged)

        self.textExtract = CustomLineEdit("Pages à extraire (ex: 1-5,7,9-12)", False)
        self.textExtract.textChanged.connect(self.update_button_status)
        self.textExtract.setValidator(QRegExpValidator(QRegExp("(([1-9]\\d*,)|([1-9]\\d*-[1-9]\\d*,))+")))
        self.textExtract.setMaximumWidth(100)

        layout.addWidget(self.radioButtonSplit, 3, 0)
        layout.addWidget(self.textSplit, 3, 1)
        layout.addWidget(self.radioButtonExtract, 4, 0)
        layout.addWidget(self.textExtract, 4, 1)
        layout.setRowMinimumHeight(2, 20)
        layout.setRowMinimumHeight(5, 20)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(5, 1)
        layout.setColumnMinimumWidth(0, 10)

        self.update_button_status()

    def update_button_status(self):
        self.button_exec.setEnabled((self.check_select_status()) and
                                    ((self.radioButtonSplit.isChecked() and self.textSplit.text() != "" and self.textSplit.text()[-1].isdigit()) or
                                    (self.radioButtonExtract.isChecked() and self.textExtract.text() != "" and self.textExtract.text()[-1].isdigit())))

    def radioButtonChanged(self):
        self.update_button_status()
        self.textSplit.setEnabled(self.radioButtonSplit.isChecked())
        self.textExtract.setEnabled(self.radioButtonExtract.isChecked())
        if self.radioButtonSplit.isChecked():
            self.textExtract.clear()
        elif self.radioButtonExtract.isChecked():
            self.textSplit.clear()

    def split(self):
        outpath = QFileDialog.getSaveFileName(self, "Sélectionner le fichier de sortie", "", "PDF(*.pdf)")[0]
        if outpath == "":
            return

        readInput = PdfReader(self.textSelect.text())

        try:
            if self.radioButtonSplit.isChecked():
                index = self.textSplit.text().split(",")
                sortedlist = sorted(set(index))
                sortedlist.insert(0, str(0))
                sortedlist.append(str(readInput.getNumPages()))

                for i in range(len(sortedlist) - 1):
                    output = PdfFileWriter()

                    for j in range(int(sortedlist[i]), int(sortedlist[i + 1])):
                        output.addPage(readInput.getPage(j))

                    root = os.path.splitext(outpath)[0]
                    outputStream = open(root + str(i) + ".pdf", "wb")
                    output.write(outputStream)
                    outputStream.close()

                QMessageBox.information(self, "Découpage", "Fichier découpé avec succès")

            elif self.radioButtonExtract.isChecked():
                output = PdfFileWriter()
                index = self.textExtract.text().split(",")
                for i in range(len(index)):
                    if "-" in index[i]:
                        start, end = index[i].split("-")
                        for j in range(int(start), int(end) + 1):
                            output.addPage(readInput.getPage(j - 1))
                    else:
                        output.addPage(readInput.getPage(int(index[i]) - 1))
                outputStream = open(outpath, "wb")
                output.write(outputStream)
                outputStream.close()
                QMessageBox.information(self, "Extraction", "Fichier(s) extrait(s) avec succès.")
        except IndexError:
            QMessageBox.warning(self, "Erreur", "Erreur lors du découpage.")
