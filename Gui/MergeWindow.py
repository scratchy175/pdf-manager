from PyPDF2 import PdfFileMerger
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MergeWindows(QMainWindow):
    def __init__(self):
        super().__init__()

        self.paths = []
        self.fnames = []

        title = "Fusionner des fichiers PDF"
        top = 400
        left = 400
        width = 800
        height = 600

        self.setWindowIcon(QIcon("logo.png"))
        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)

        button_select_file = QPushButton("Ajouter", self)
        #button_select_file.setGeometry(200,100, 60, 35)
        button_select_file.move(100, 50)
        button_select_file.setToolTip("Ajouter un fichier à la liste")
        button_select_file.clicked.connect(self.select_file)
    
        self.list = QListWidget(self)
        self.list.setGeometry(100, 150, 500, 300)
        self.list.move(100, 100)

        self.list.dragEnterEvent = self.dragEnterEvent
        self.list.dragMoveEvent= self.dragMoveEvent
        self.list.dropEvent = self.dropEvent
        
        self.list.setDragDropMode(QAbstractItemView.InternalMove)


        self.button_down = QPushButton("Descendre", self)
        self.button_down.move(200, 50)
        self.button_down.setToolTip("Descendre le fichier sélectionné")
        self.button_down.clicked.connect(self.down)

        self.button_up = QPushButton("Monter", self)
        self.button_up.move(300, 50)
        self.button_up.setToolTip("Remonter le fichier sélectionné")
        self.button_up.clicked.connect(self.up)

        self.button_remove = QPushButton("Supprimer", self)
        self.button_remove.move(400, 50)
        self.button_remove.setToolTip("Supprimer le fichier sélectionné")
        self.button_remove.clicked.connect(self.remove)

        self.button_remove_all = QPushButton("Supprimer tout", self)
        self.button_remove_all.move(500, 50)
        self.button_remove_all.setToolTip("Supprimer tous les fichiers de la liste")
        self.button_remove_all.clicked.connect(self.remove_all)

        self.button_merge = QPushButton("Fusionner", self)
        self.button_merge.move(100, 500)
        self.button_merge.setToolTip("Fusionner les fichiers sélectionnés")
        self.button_merge.clicked.connect(self.merge)

        self.buttonBrowse = QPushButton("Parcourir", self)
        self.buttonBrowse.move(600, 450)
        self.buttonBrowse.setToolTip("Parcourir pour choisir le fichier de destination")
        self.buttonBrowse.clicked.connect(self.browse_file)


        self.updateButtonStatus()
        self.setButtonConnections()


        self.label = QLabel(self)
        self.label.setText("Fichier de destination :")
        self.label.setGeometry(100, 450, 300, 30)
        self.label.move(100, 420)

        self.textBox = QLineEdit(self)
        self.textBox.setGeometry(100, 100, 500, 30)
        self.textBox.setPlaceholderText("Sélectionner un fichier : [*.pdf]")
        self.textBox.move(100, 450)

    def select_file(self):
        self.filePath, _ = QFileDialog.getOpenFileNames(self, "Sélectionner les fichiers à ajouter", "", "PDF(*.pdf)")
        
        if self.filePath == "":
            return
        else:
            print(self.filePath)
            for val in self.filePath:
                fname = QUrl(val).fileName()
                if val not in self.paths:
                    self.paths.append(val)
                    self.fnames.append(fname)
                    self.list.addItem(fname)
            self.updateButtonStatus()
    
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
        self.updateButtonStatus()

    def remove_all(self):
        self.list.clear()
        self.updateButtonStatus()

    def setButtonConnections(self): #tester ca
        self.list.itemSelectionChanged.connect(self.updateButtonStatus)


    def updateButtonStatus(self):
        self.button_up.setDisabled(not bool(self.list.selectedItems()) or self.list.currentRow() == 0)
        self.button_down.setDisabled(not bool(self.list.selectedItems()) or self.list.currentRow() == self.list.count() - 1)
        self.button_remove.setDisabled(not bool(self.list.selectedItems()) or self.list.count() == 0)
        self.button_remove_all.setDisabled(self.list.count() == 0)
        self.button_merge.setDisabled(self.list.count() == 0 or self.textBox.text() == "")

    def merge(self):
        merger = PdfFileMerger()
        for val in self.paths:
            merger.append(val, import_bookmarks=False)
        
        merger.write(self.textBox.text())
        merger.close()
        QMessageBox.information(self, "Fusion", "Fusion terminé avec succès !")

    def browse_file(self):
        self.browseFilePath, _ = QFileDialog.getSaveFileName(self, "Selectioner un fichier", "", "PDF(*.pdf);;All Files(*.*) ")
 
        if self.browseFilePath == "":
            return
        else:
            self.textBox.setText(self.browseFilePath)
            self.updateButtonStatus()




    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()

        elif event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            QListWidget.dragEnterEvent(self.list, event)
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        
        elif event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            QListWidget.dragMoveEvent(self.list, event)
            
        else:
            event.ignore()

    def dropEvent(self, event):
        item  = self.list.currentItem()
        row = self.list.row(item)
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()


            for url in event.mimeData().urls():
                if url.isLocalFile() and url.toLocalFile().endswith(".pdf"):
                    path = url.toLocalFile()
                    fname = QUrl(url).fileName()
                    if path not in self.paths:
                        self.paths.append(path)
                        self.fnames.append(fname)
                        self.list.addItem(fname)
                else:
                    event.ignore()
            self.updateButtonStatus()
            

        elif event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            QListWidget.dropEvent(self.list, event)
            self.paths.insert(self.list.currentRow(), self.paths.pop(row))
            self.updateButtonStatus()             
        else:
            event.ignore()