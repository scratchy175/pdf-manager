from PyPDF2 import PdfFileMerger
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Gui.GeneralWindow import GeneralWindow


class MergeWindow(QMainWindow, GeneralWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.paths = []
        self.fnames = []
        self.setWindowIcon(QIcon("logo.png"))
        self.setWindowTitle("Fusionner")
        self.setFixedSize(600, 530)
        self.center()

        button_select_file = QPushButton("Ajouter", self)
        button_select_file.move(50, 20)
        button_select_file.setToolTip("Ajouter un fichier à la liste")
        button_select_file.clicked.connect(self.select_file)

        self.button_down = QPushButton("Descendre", self)
        self.button_down.move(150, 20)
        self.button_down.setToolTip("Descendre le fichier sélectionné")
        self.button_down.clicked.connect(self.down)

        self.button_up = QPushButton("Monter", self)
        self.button_up.move(250, 20)
        self.button_up.setToolTip("Remonter le fichier sélectionné")
        self.button_up.clicked.connect(self.up)

        self.button_remove = QPushButton("Supprimer", self)
        self.button_remove.move(350, 20)
        self.button_remove.setToolTip("Supprimer le fichier sélectionné")
        self.button_remove.clicked.connect(self.remove)

        self.button_remove_all = QPushButton("Supprimer tout", self)
        self.button_remove_all.move(450, 20)
        self.button_remove_all.setToolTip("Supprimer tous les fichiers de la liste")
        self.button_remove_all.clicked.connect(self.remove_all)

        self.list = QListWidget(self)
        self.list.setGeometry(100, 150, 500, 300)
        self.list.move(50, 70)

        self.list.dragEnterEvent = self.dragEnterEvent
        self.list.dragMoveEvent = self.dragMoveEvent
        self.list.dropEvent = self.dropEvent

        self.list.setDragDropMode(QAbstractItemView.InternalMove)

        label = QLabel(self)
        label.setText("Fichier de destination :")
        label.setGeometry(100, 450, 300, 30)
        label.move(50, 390)

        self.textBox = QLineEdit(self)
        self.textBox.setGeometry(100, 100, 400, 30)
        self.textBox.setPlaceholderText("Sélectionner un fichier : [*.pdf]")
        self.textBox.move(50, 420)

        button_browse = QPushButton("Parcourir", self)
        button_browse.move(450, 420)
        button_browse.setToolTip("Parcourir pour choisir le fichier de destination")
        button_browse.clicked.connect(self.browse_file)

        self.button_merge = QPushButton("Exécuter", self)
        self.button_merge.move(self.geometry().width() - self.button_merge.geometry().width() - 10, self.geometry().height() - 40)
        self.button_merge.setToolTip("Fusionner les fichiers sélectionnés")
        self.button_merge.clicked.connect(self.merge)

        button_back = QPushButton("< Retour", self)
        button_back.move(10, self.geometry().height() - 40)
        button_back.setToolTip("Retourner au menu principal")
        button_back.clicked.connect(self.showMain)

        self.set_button_connections()
        self.update_button_status()

    def showMain(self):
        self.main_window.show()
        self.close()

    def select_file(self):
        filePath, _ = QFileDialog.getOpenFileNames(self, "Sélectionner les fichiers à ajouter", "", "PDF(*.pdf)")

        if filePath == "":
            return
        else:
            for val in filePath:
                fname = QUrl(val).fileName()
                if val not in self.paths:
                    self.paths.append(val)
                    self.fnames.append(fname)
                    self.list.addItem(fname)
            self.update_button_status()

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
        self.update_button_status()

    def remove_all(self):
        self.list.clear()
        self.update_button_status()

    def set_button_connections(self):
        self.list.itemSelectionChanged.connect(self.update_button_status)

    def update_button_status(self):
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
        browseFilePath, _ = QFileDialog.getSaveFileName(self, "Sélectionner un fichier", "", "PDF(*.pdf);;All Files(*.*) ")

        if browseFilePath == "":
            return
        else:
            self.textBox.setText(browseFilePath)
            self.update_button_status()

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
        item = self.list.currentItem()
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

            self.update_button_status()
        elif event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            QListWidget.dropEvent(self.list, event)
            self.paths.insert(self.list.currentRow(), self.paths.pop(row))
            self.update_button_status()
        else:
            event.ignore()
