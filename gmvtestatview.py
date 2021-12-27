from PyQt5 import QtGui, QtCore, QtWidgets, uic
import sys
import subprocess       
from gmvtestatcontroller import TestatController
from gmvtestatmodel import TestatModel
import numpy as np

class TestatView(QtWidgets.QMainWindow):
    def __init__(self):
        super(TestatView, self).__init__()
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
        self.krit4_lineEdit.setValidator(eingabeChecker)
        self.krit5_lineEdit.setValidator(eingabeChecker)
        self.krit6_lineEdit.setValidator(eingabeChecker)
        self.krit7_lineEdit.setValidator(eingabeChecker)
        self.krit8_lineEdit.setValidator(eingabeChecker)
        self.krit9_lineEdit.setValidator(eingabeChecker)
        self.abzug1_lineEdit.setValidator(eingabeChecker)
        self.abzug2_lineEdit.setValidator(eingabeChecker)

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
            filter = f'{ext}-Dateien k(*.{ext}) ;; Alle Dateien (*)')

    def folderDialog(self):
        return QtWidgets.QFileDialog.getExistingDirectory(self, caption='Öffne den Ordner mit den Moodle-Abgaben')

    def fuelleBewertungsUebersicht(self, bewertungsuebersicht):
        self.aktiviereBestehensgrenzeRegler(True)
        self.aktiviereSpeichernUndBatchImportBtn(True)
        self.BewertungsUebersicht_table.setRowCount(bewertungsuebersicht.shape[0])
        bewertungsuebersichtArray = bewertungsuebersicht.to_numpy()
        for idx, value in np.ndenumerate(bewertungsuebersichtArray):
            item = QtWidgets.QTableWidgetItem(str(value))
            if idx[1]<6:
                self.BewertungsUebersicht_table.setItem(idx[0],idx[1],item)

    def setzeBewertungsUebersichtZelle(self, row, column, newValue):
        item = QtWidgets.QTableWidgetItem(str(newValue))
        self.BewertungsUebersicht_table.setItem(row, column, item)

    def falscheListeFenster(self, listtyp):
        box = QtWidgets.QMessageBox(self)
        box.setWindowTitle('Fehler: Falscher Dateiname.')
        box.setText(f'Bitte wähle die {listtyp}-Liste aus!\n\n'
                    f'Hinweis:\nDer Dateiname (inkl. Pfad) muss \'{listtyp}\' enthalten.\n'
                    f'Die Groß-/Kleinschreibung ist dabei unerheblich.')
        box.exec()

    def zeigeLadenHaken(self, button):
        button.setText(u'Laden \u2714')

    def fuelleLabel(self, label, newValue):
        label.setText(f'{newValue}')

    def fuelleLineEdit(self, lineEdit, newValue):
        if isinstance(newValue, str):
            lineEdit.setText(newValue)
        else:
            lineEdit.setText(f'{newValue:g}')

    def aktiviereBewertungsdetails(self, istAktiv):
        self.bewertungsdetails_groupBox.setEnabled(istAktiv)
        self.idCheck_btn.setEnabled(False)

    def aktiviereBestehensgrenzeRegler(self, istAktiv):
        self.grenze_label.setEnabled(istAktiv)
        self.grenze_spinBox.setEnabled(istAktiv)

    def aktiviereSpeichernUndBatchImportBtn(self, istAktiv):
        self.Speichern_btn.setEnabled(istAktiv)
        self.BatchImportKpLaden_btn.setEnabled(istAktiv)

    def fuelleBewertungsDetails(self, geklickteZeile):
        self.fuelleLineEdit(self.krit1_lineEdit, geklickteZeile["Kriterium 1"])
        self.fuelleLineEdit(self.krit2_lineEdit, geklickteZeile["Kriterium 2"])
        self.fuelleLineEdit(self.krit3_lineEdit, geklickteZeile["Kriterium 3"])
        self.fuelleLineEdit(self.krit4_lineEdit, geklickteZeile["Kriterium 4"])
        self.fuelleLineEdit(self.krit5_lineEdit, geklickteZeile["Kriterium 5"])
        self.fuelleLineEdit(self.krit6_lineEdit, geklickteZeile["Kriterium 6"])
        self.fuelleLineEdit(self.krit7_lineEdit, geklickteZeile["Kriterium 7"])
        self.fuelleLineEdit(self.krit8_lineEdit, geklickteZeile["Kriterium 8"])
        self.fuelleLineEdit(self.krit9_lineEdit, geklickteZeile["Kriterium 9"])
        self.fuelleLineEdit(self.abzug1_lineEdit, geklickteZeile["Abzug 1"])
        self.fuelleLineEdit(self.abzug2_lineEdit, geklickteZeile["Abzug 2"])

        self.bemerkung_lineEdit.setText(str(geklickteZeile["Bemerkungen"]))
        self.setzePunktestandLabel(geklickteZeile['Punkte'])

    def setzePunktestandLabel(self, punkte):
        text = f'<html><head/><body><p><span style=" font-size:14pt; font-weight:600;">Gesamtpunktzahl: {punkte} / 30.0 P</span></p></body></html>'
        self.gesamtpunktzahl_label.setText(text)

    def zeigeOrdnerImFinder(self, pfad):
        subprocess.call(["open", "-R", pfad])

    def pdfStatusFenster(self, pdfStatus):
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('macintosh')
    
    view = TestatView()
    model = TestatModel()
    controller = TestatController(model, view)
    sys.exit(app.exec())