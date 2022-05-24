from PyPDF2 import PdfFileMerger
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MergeWindows(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "Fusion"
        top = 400
        left = 400
        width = 800
        height = 600

        self.setWindowIcon(QIcon("logo.png"))
        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)

        button_select_file = QPushButton("Ajouter", self)
        #button_select_file.setGeometry(200,100, 60, 35)
        button_select_file.move(500, 100)
        button_select_file.setToolTip("This is a <b>QPushButton</b> widget")
        button_select_file.clicked.connect(self.select_file)
    
        self.list = QListWidget(self)
        self.list.move(100, 150)
        self.list.setToolTip("This is a <b>QListWidget</b> widget")
        self.list.setGeometry(100, 150, 300, 300)
        self.list.setAcceptDrops(True)
        self.list.setDragEnabled(True)
        self.list.setDragDropMode(QAbstractItemView.InternalMove)

        self.button_down = QPushButton("Down", self)
        self.button_down.move(100, 450)
        self.button_down.setToolTip("This is a <b>QPushButton</b> widget")
        self.button_down.clicked.connect(self.down)

        self.button_up = QPushButton("Up", self)
        self.button_up.move(200, 450)
        self.button_up.setToolTip("This is a <b>QPushButton</b> widget")
        self.button_up.clicked.connect(self.up)

        self.button_remove = QPushButton("Remove", self)
        self.button_remove.move(300, 450)
        self.button_remove.setToolTip("This is a <b>QPushButton</b> widget")
        self.button_remove.clicked.connect(self.remove)

        self.button_remove_all = QPushButton("Remove All", self)
        self.button_remove_all.move(400, 450)
        self.button_remove_all.setToolTip("This is a <b>QPushButton</b> widget")
        self.button_remove_all.clicked.connect(self.remove_all)

        self.button_merge = QPushButton("Fusionner", self)
        self.button_merge.move(500, 450)
        self.button_merge.setToolTip("This is a <b>QPushButton</b> widget")
        self.button_merge.clicked.connect(self.merge)

        self.buttonBrowse = QPushButton("Parcourir", self)
        self.buttonBrowse.move(600, 450)
        self.buttonBrowse.setToolTip("This is a <b>QPushButton</b> widget")
        self.buttonBrowse.clicked.connect(self.browse_file)


        self.updateButtonStatus()
        self.setButtonConnections()


        self.label = QLabel(self)
        self.label.setText("Fichier à créer")
        self.label.move(100, 50)

        self.textBox = QLineEdit(self)
        self.textBox.move(100, 100)
        self.textBox.setGeometry(100, 100, 300, 30)
        self.textBox.setPlaceholderText("Sélectionner un fichier : [*.pdf]")

    def select_file(self):
        self.filePath, _ = QFileDialog.getOpenFileNames(self, "Sélectionner les fichiers à ajouter", "", "PDF(*.pdf);;All Files(*.*) ")
        
        if self.filePath == "":
            return
        else:
            print(self.filePath)
            for val in self.filePath:
                fname = QUrl(val).fileName()
                self.list.addItem(fname)
    
    def down(self):
        rowIndex = self.list.currentRow()
        if rowIndex < self.list.count() - 1:
            item = self.list.takeItem(rowIndex)
            self.list.insertItem(rowIndex + 1, item)
            self.list.setCurrentItem(item)
    
    def up(self):
        rowIndex = self.list.currentRow()
        if rowIndex > 0:
            item = self.list.takeItem(rowIndex)
            self.list.insertItem(rowIndex - 1, item)
            self.list.setCurrentItem(item)

    def remove(self):
        rowIndex = self.list.currentRow()
        self.list.takeItem(rowIndex)

    def remove_all(self):
        self.list.clear()

    def setButtonConnections(self):
        self.list.itemSelectionChanged.connect(self.updateButtonStatus)


    def updateButtonStatus(self):
        self.button_up.setDisabled(not bool(self.list.selectedItems()) or self.list.currentRow() == 0)
        self.button_down.setDisabled(not bool(self.list.selectedItems()) or self.list.currentRow() == self.list.count() - 1)
        self.button_remove.setDisabled(not bool(self.list.selectedItems()) or self.list.count() == 0)
        self.button_remove_all.setDisabled(not bool(self.list.selectedItems()) or self.list.count() == 0)

    def merge(self):
        #print(self.saveFilePath)
        merger = PdfFileMerger()
        for val in self.filePath:
            merger.append(val, import_bookmarks=False)
        
        merger.write(self.textBox.text())
        merger.close()

    def browse_file(self):
        self.browseFilePath, _ = QFileDialog.getSaveFileName(self, "Selectioner un fichier", "", "PDF(*.pdf);;All Files(*.*) ")
 
        if self.browseFilePath == "":
            return
        else:
            self.textBox.setText(self.browseFilePath)