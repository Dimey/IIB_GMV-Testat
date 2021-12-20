from PyQt5 import QtGui, QtCore, QtWidgets, uic
import sys
import subprocess       
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
        # Setze feste Fenstergröße
        self.setFixedSize(800,990);
        # Verhindere nicht-numerische Eingaben
        eingabeChecker = QtGui.QDoubleValidator()
        eingabeChecker.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.krit1_lineEdit.setValidator(eingabeChecker)
        self.krit2_lineEdit.setValidator(eingabeChecker)
        self.krit3_lineEdit.setValidator(eingabeChecker)
        
        # Setze die Einstellungen für Spaltbreiten der Bewertungsübersicht
        header = self.BewertungsUebersicht_table.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)

        # Färbe Eingebefelder
        self.abzug1_lineEdit.setStyleSheet("background-color: rgb(255, 126, 121);")
        self.abzug2_lineEdit.setStyleSheet("background-color: rgb(255, 126, 121);")

    def fileDialog(self, ext):
        return QtWidgets.QFileDialog.getOpenFileName(self, 
            f'Öffne die {ext}-Datei', 
            filter = f'{ext}-Dateien (*.{ext}) ;; Alle Dateien (*)')

    def folderDialog(self):
        return QtWidgets.QFileDialog.getExistingDirectory(self, caption='Öffne den Ordner mit den Moodle-Abgaben')

    def zeigeBewertungsUebersicht(self, bewertungsuebersicht):
        self.BewertungsUebersicht_table.setRowCount(bewertungsuebersicht.shape[0])
        bewertungsuebersichtArray = bewertungsuebersicht.to_numpy()
        for idx, value in np.ndenumerate(bewertungsuebersichtArray):
            item = QtWidgets.QTableWidgetItem(str(value))
            if idx[1]<6:
                self.BewertungsUebersicht_table.setItem(idx[0],idx[1],item)

    def falscheListeFenster(self, listtyp):
        box = QtWidgets.QMessageBox(self)
        box.setWindowTitle('Fehler: Falscher Dateiname.')
        box.setText(f'Bitte wähle die {listtyp}-Liste aus!\n\n'
                    f'Hinweis:\nDer Dateiname (inkl. Pfad) muss \'{listtyp}\' enthalten.\n'
                    f'Die Groß-/Kleinschreibung ist dabei unerheblich.')
        box.exec()

    def zeigeLadenHaken(self, button):
        button.setText(u'Laden \u2714')

    def zeigeAnzahl(self, label, anzahl):
        label.setText(f'{anzahl}')

    def aktiviereBewertungsdetails(self, istAktiv):
        self.bewertungsdetails_groupBox.setEnabled(istAktiv)
        self.diffTool_btn.setEnabled(False)

    def fuelleBewertungsDetails(self, geklickteZeile):
        self.krit1_lineEdit.setText(str(geklickteZeile["Kriterium 1"]))
        self.krit2_lineEdit.setText(str(geklickteZeile["Kriterium 2"]))
        self.krit3_lineEdit.setText(str(geklickteZeile["Kriterium 3"]))
        self.krit4_lineEdit.setText(str(geklickteZeile["Kriterium 4"]))
        self.krit5_lineEdit.setText(str(geklickteZeile["Kriterium 5"]))
        self.krit6_lineEdit.setText(str(geklickteZeile["Kriterium 6"]))
        self.krit7_lineEdit.setText(str(geklickteZeile["Kriterium 7"]))
        self.krit8_lineEdit.setText(str(geklickteZeile["Kriterium 8"]))
        self.krit9_lineEdit.setText(str(geklickteZeile["Kriterium 9"]))
        self.bemerkung_lineEdit.setText(str(geklickteZeile["Bemerkungen"]))
        self.setzePunktestandLabel(str(geklickteZeile['Punkte']))

    def setzePunktestandLabel(self, punkte):
        self.gesamtpunktzahl_label.setText(f"Gesamtpunktzahl: {punkte} / 30.0")

    def zeigeOrdnerImFinder(self, pfad):
        subprocess.call(["open", "-R", pfad])

    def pdfStatusFenster(self, pdfStatus):
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('macintosh')
    
    view = GMVTestat()
    model = TestatData()
    controller = TestatController(model, view)
    sys.exit(app.exec())