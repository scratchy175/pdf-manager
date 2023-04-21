import os
from PyQt6.QtGui import QIcon, QScreen 
from PyQt6.QtWidgets import (QFileDialog, QLabel, QLineEdit,
                            QPushButton, QWidget, QApplication)


class GeneralWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        
        self.main_window = main_window
        self.setWindowIcon(QIcon("logo.png"))

    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def setup_back_exec(self, layout, row, func):
        self.button_exec = CustomButton("Exécuter", func)

        button_back = CustomButton("Retour", self.back)

        layout.addWidget(button_back, row, 0, 1, 2)
        layout.addWidget(self.button_exec, row, 4)

    def back(self):
        self.close()
        self.main_window.show()

    def setup_select(self, layout, row, update_button_status):
        labelSelect = QLabel(text="Fichier à traiter :")

        self.textSelect = CustomLineEdit("Sélectionner un fichier : [*.pdf]")
        self.textSelect.textChanged.connect(update_button_status)

        buttonSelect = CustomButton("Parcourir", self.select_file)

        layout.addWidget(labelSelect, row, 0, 1, 2)
        layout.addWidget(self.textSelect, row+1, 0, 1, 4)
        layout.addWidget(buttonSelect, row+1, 4)

    def select_file(self):
        browseFilePath, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier", "", "PDF(*.pdf)")

        if browseFilePath == "":
            return
        self.textSelect.setText(browseFilePath)

    def check_select_status(self):
        return self.textSelect.text() != "" and os.path.isfile(self.textSelect.text())
    

class CustomLineEdit(QLineEdit):
    def __init__(self, placeholder, enabled=True):
        super().__init__()
        self.placeholder = placeholder
        self.setPlaceholderText(self.placeholder)
        self.setMinimumSize(300, 30)
        self.setEnabled(enabled)


class CustomButton(QPushButton):
    def __init__(self, title, function):
        super().__init__()
        self.title = title
        self.function = function
        self.setText(self.title)
        self.clicked.connect(self.function)
        self.setFixedSize(100, 30)
