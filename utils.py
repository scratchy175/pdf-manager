from PyQt5.QtWidgets import QMessageBox


def checkIndex(self, listPages, nbpages):
        if max(listPages) > nbpages:
            QMessageBox.warning(self, "Numéro de page invalide", "Veuillez entrer des numéros de page valide")
            return True

def setupList(entry):
        index = entry.text().split(",")
        setPagesToRotate = set()
        for val in index:
            if "-" in val:
                start, end = val.split("-")
                for j in range(int(start), int(end) + 1):
                    setPagesToRotate.add(j)
            else:
                setPagesToRotate.add(int(val))
        return sorted(list(setPagesToRotate))
