import os
from PyPDF2 import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Gui.GeneralWindow import GeneralWindow


class SplitWindow(QMainWindow, GeneralWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowIcon(QIcon("logo.png"))
        self.setWindowTitle("Découper ou Extraire")
        self.setFixedSize(800, 600)
        self.center()
        self.layout2 = QGridLayout()

        self.buttonSelect = QPushButton("Sélectionner", self)
        self.buttonSelect.move(600, 150)
        self.buttonSelect.setToolTip("Sélectionner le fichier à traiter")
        self.buttonSelect.clicked.connect(self.browse_file)


        self.labelSelect = QLabel(self)
        self.labelSelect.setText("Fichier à traiter :")
        self.labelSelect.setGeometry(100, 450, 300, 30)
        self.labelSelect.move(100, 120)


        self.textSelect = QLineEdit(self)
        self.textSelect.setGeometry(100, 100, 500, 30)
        self.textSelect.setPlaceholderText("Sélectionner un fichier : [*.pdf]")
        self.textSelect.move(100, 150)

        self.textSelect.dragEnterEvent = self.dragEnterEvent
        self.textSelect.dragMoveEvent= self.dragMoveEvent
        self.textSelect.dropEvent = self.dropEventFile


        self.buttonSplit = QPushButton("Exécuter", self)
        self.buttonSplit.move(100, 500)
        self.buttonSplit.setToolTip("Exécution")
        self.buttonSplit.clicked.connect(self.split)

        self.checkboxSplit = QCheckBox("Découpage du fichier", self)
        self.checkboxSplit.setGeometry(100, 100, 200, 30)
        self.checkboxSplit.move(100, 300)
        self.checkboxSplit.setToolTip("Découpage du fichier")
        self.checkboxSplit.stateChanged.connect(self.checkboxchangedS)

        self.checkboxExtract = QCheckBox("Extraction de pages", self)
        self.checkboxExtract.setGeometry(100, 100, 200, 30)
        self.checkboxExtract.move(100, 350)
        self.checkboxExtract.setToolTip("Extraction de pages")
        self.checkboxExtract.stateChanged.connect(self.checkboxchangedE)

        self.textSplit = QLineEdit(self)
        self.textSplit.setGeometry(100, 100, 300, 30)
        self.textSplit.setPlaceholderText("Pages à découper (ex: 3,6)")
        self.textSplit.move(250, 300)
        self.textSplit.setEnabled(False)
        self.textSplit.textChanged.connect(self.update_button_status)

        self.textExtract = QLineEdit(self)
        self.textExtract.setGeometry(100, 100, 300, 30)
        self.textExtract.setPlaceholderText("Pages à extraire (ex: 1-5,7,9-12)")
        self.textExtract.move(250, 350)
        self.textExtract.setEnabled(False)
        self.textExtract.textChanged.connect(self.update_button_status)


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
        self.textBrowse.textChanged.connect(self.update_button_status)

        self.textBrowse.dragEnterEvent = self.dragEnterEvent
        self.textBrowse.dragMoveEvent= self.dragMoveEvent
        self.textBrowse.dropEvent = self.dropEventDir

        self.update_button_status()


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
        self.selectDirPath = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier", "", QFileDialog.ShowDirsOnly)
        if self.selectDirPath == "":
            return
        else:
            self.textBrowse.setText(self.selectDirPath)
            self.update_button_status()


    def browse_file(self):
        self.browseFilePath, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier", "", "PDF(*.pdf)")

        if self.browseFilePath == "":
            return
        else:
            self.textSelect.setText(self.browseFilePath)
            self.update_button_status()


    def update_button_status(self):
        #self.buttonSplit.setDisabled(self.textBrowse.text() == "" or self.textSelect.text() == "" or not self.checkboxSplit.isChecked() and not self.checkboxExtract.isChecked())
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
                if os.isdir(path):
                    self.textBrowse.setText(path)
            else:
                event.ignore()
        else:
            event.ignore()

    
    def split(self):
        try:
            input = PdfFileReader(self.textSelect.text())
        except:
            QMessageBox.critical(self, "Erreur", "Fichier invalide")
            return
        if self.checkboxSplit.isChecked():
            index = self.textSplit.text().split(",")
            index.insert(0,0)
            index.append(input.getNumPages())
            for i in range(len(index)-1):
                output = PdfFileWriter()
                for j in range(int(index[i]),int(index[i+1])):
                    output.addPage(input.getPage(j))
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
                        output.addPage(input.getPage(j-1))
                else:
                    output.addPage(input.getPage(int(index[i])-1))
            outputStream = open(self.textBrowse.text() + "/PDFManager_Extract" + ".pdf", "wb")
            output.write(outputStream)
            outputStream.close()
            QMessageBox.information(self, "Extraction", "Fichier(s) extrait(s) avec succès.")