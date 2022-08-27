Création de l'exe:
```
v1:
pyinstaller --noconfirm --onedir --windowed --icon "C:/Users/yannt/pdf-manager/logo.ico" --name "PDFManager" --add-data "C:/Users/yannt/pdf-manager/Gui;Gui/" --hidden-import "PyPDF2" --hidden-import "PyQt5.QtWidgets" --add-data "C:/Users/yannt/pdf-manager/logo.png;."  "C:/Users/yannt/pdf-manager/Main.py"

v2:
pyinstaller --noconfirm --onefile --windowed --clean --icon "logo.ico" --name "PDFManager" --add-data "Gui;Gui/" --hidden-import "PyPDF2" --hidden-import "PyQt5.QtWidgets" --add-data "logo.png;." "Main.py"
```