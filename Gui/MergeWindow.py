from PyPDF2 import PdfFileMerger
from PyQt5.QtWidgets import (QListWidget, QGridLayout, QFileDialog,
                             QAbstractItemView, QMessageBox)
from PyQt5.QtCore import Qt, QUrl
from Gui.GeneralWindow import CustomButton, GeneralWindow


class MergeWindow(GeneralWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.paths = []
        self.fnames = []
        self.setWindowTitle("Fusionner")
        self.center()

        button_select_file = CustomButton("Ajouter", self.select_file)

        self.button_down = CustomButton("Descendre", self.down)

        self.button_up = CustomButton("Monter", self.up)

        self.button_remove = CustomButton("Supprimer", self.remove)

        self.button_remove_all = CustomButton("Supprimer tout", self.remove_all)

        self.list = QListWidget(self)
        self.list.itemSelectionChanged.connect(self.update_button_status)
        self.list.dragEnterEvent = self.dragEnterEvent
        self.list.dragMoveEvent = self.dragMoveEvent
        self.list.dropEvent = self.dropEvent
        self.list.setDragDropMode(QAbstractItemView.InternalMove)

        layout = QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.addWidget(button_select_file, 0, 0)
        layout.addWidget(self.button_down, 0, 1)
        layout.addWidget(self.button_up, 0, 2)
        layout.addWidget(self.button_remove, 0, 3)
        layout.addWidget(self.button_remove_all, 0, 4)
        layout.addWidget(self.list, 1, 0, 1, 5)
        self.setup_back_exec(layout, 3, self.merge)
        layout.setRowMinimumHeight(2, 20)

        self.update_button_status()

    def select_file(self):
        filePath, _ = QFileDialog.getOpenFileNames(self, "Sélectionner les fichiers à ajouter", "", "PDF(*.pdf)")

        if filePath == "":
            return
        for val in filePath:
            fname = QUrl(val).fileName()

            if val not in self.paths:
                self.addtolists(val, fname)
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
        self.fnames.pop(rowIndex)
        self.paths.pop(rowIndex)
        self.update_button_status()

    def remove_all(self):
        self.list.clear()
        self.fnames.clear()
        self.paths.clear()
        self.update_button_status()

    def update_button_status(self):
        self.button_up.setDisabled(not bool(self.list.selectedItems()) or self.list.currentRow() == 0)
        self.button_down.setDisabled(not bool(self.list.selectedItems()) or self.list.currentRow() == self.list.count() - 1)
        self.button_remove.setDisabled(not bool(self.list.selectedItems()) or self.list.count() == 0)
        self.button_remove_all.setDisabled(self.list.count() == 0)
        self.button_exec.setEnabled(self.list.count() >= 2)

    def merge(self):
        outpath = QFileDialog.getSaveFileName(self, "Sélectionner le fichier de sortie", "", "PDF(*.pdf)")[0]
        if outpath == "":
            return

        merger = PdfFileMerger(strict=False)

        for val in self.paths:
            merger.append(val, import_bookmarks=False)
        merger.write(outpath)
        merger.close()
        QMessageBox.information(self, "Fusion", "Fusion terminé avec succès !")

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
                        self.addtolists(path, fname)
                else:
                    event.ignore()

            self.update_button_status()
        elif event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            QListWidget.dropEvent(self.list, event)
            self.paths.insert(self.list.currentRow(), self.paths.pop(row))
            self.update_button_status()
        else:
            event.ignore()


    def addtolists(self, arg0, fname):
        self.paths.append(arg0)
        self.fnames.append(fname)
        self.list.addItem(fname)
