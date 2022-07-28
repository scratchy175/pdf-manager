Création de l'exe:
```
pyinstaller --noconfirm --onedir --windowed --icon "C:/Users/yannt/pdf-manager/logo.ico" --name "PDFManager" --add-data "C:/Users/yannt/pdf-manager/Gui;Gui/" --hidden-import "PyPDF2" --hidden-import "PyQt5.QtWidgets" --add-data "C:/Users/yannt/pdf-manager/logo.png;."  "C:/Users/yannt/pdf-manager/Main.py"
```