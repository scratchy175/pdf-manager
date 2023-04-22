# PDFManager

## Description

PDFManager est un logiciel permettant de gérer des fichiers PDF.

## Fonctionnalités

- Fusionner des fichiers PDF
- Séparer des pages d'un fichier PDF
- Extraire des pages d'un fichier PDF
- Tourner des pages d'un fichier PDF

## Version exécutable

### Création du fichier .exe
```bash
pyinstaller --noconfirm --onedir --windowed --clean --icon "logo.ico" --name "PDFManager" --add-data "Gui;Gui/" --copy-metadata pikepdf --add-data "logo.png;." "Main.py"
```

## Version python

### Tout en un
```bash
make setup
```

### Création et activation de l'environnement virtuel
```bash
make activate
```

### Installation des dépendances
```bash
make install
```

### Lancement du programme
```bash
make run
```