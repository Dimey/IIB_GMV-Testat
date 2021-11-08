from PyQt5 import QtWidgets, uic
import sys       
from gmvtestatcontroller import TestatController
from gmvtestatmodel import TestatData
import numpy as np

class GMVTestat(QtWidgets.QMainWindow):
    def __init__(self):
        super(GMVTestat, self).__init__()
        uic.loadUi('gmvtestat.ui', self)
        self.konfigUI()
        
        self.show()
        
    def konfigUI(self):
        #TODO: 'Verschönern' durch setsectionresizemode
        pass

    def fileDialog(self, ext):
        return QtWidgets.QFileDialog.getOpenFileName(self, f'Öffne die {ext}-Datei', filter = f'{ext}-Dateien (*.{ext}) ;; Alle Dateien (*)')

    def folderDialog(self):
        return QtWidgets.QFileDialog.getExistingDirectory(self, caption='Öffne den Ordner mit den Moodle-Abgaben')

    def zeigeBewertungsUebersicht(self, bewertungsuebersicht):
        self.BewertungsUebersicht_table.setRowCount(bewertungsuebersicht.shape[0])
        bewertungsuebersichtArray = bewertungsuebersicht.to_numpy()
        for idx, value in np.ndenumerate(bewertungsuebersichtArray):
            item = QtWidgets.QTableWidgetItem(str(value))
            self.BewertungsUebersicht_table.setItem(idx[0],idx[1],item)

    def falscheListeFenster(self, listtyp):
        box = QtWidgets.QMessageBox(self)
        box.setWindowTitle('Fehler: Falscher Dateiname.')
        box.setText(f'Bitte wähle die {listtyp}-Liste aus!\n\nHinweis:\nDer Dateiname (inkl. Pfad) muss \'{listtyp}\' enthalten.\nDie Groß-/Kleinschreibung ist dabei unerheblich.')
        box.exec()

    def zeigeLadenHaken(self, button):
        QtWidgets.QPushButton.setText(button, u'Laden \u2714')

    def zeigeAnzahl(self, label, liste):
        QtWidgets.QLabel.setText(label, f'{liste.shape[0]}')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('macintosh')
    view = GMVTestat()
    model = TestatData()
    controller = TestatController(model, view)
    sys.exit(app.exec())