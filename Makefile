
run:
	python Main.py

setup: install

# Installer les dépendances
install: activate
	pip install -r requirements.txt

# Activer l'environnement virtuel
activate: venv
	. venv/bin/activate

# Créer un environnement virtuel
venv:
	python -m venv venv

exe:
	pyinstaller --noconfirm --onedir --windowed --clean --icon "logo.ico" --name "PDFManager" --add-data "Gui;Gui/" --copy-metadata pikepdf --add-data "logo.png;." "Main.py"

clean:
	rm -rf build
	rm -rf dist
	rm -rf __pycache__
	rm -rf venv
	rm -rf *.spec
	
