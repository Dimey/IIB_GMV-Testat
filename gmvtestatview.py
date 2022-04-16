import os
import sys
import subprocess  
import numpy as np 
from PyQt5 import QtGui, QtCore, QtWidgets, uic    
from gmvtestatcontroller import TestatController
from gmvtestatmodel import TestatModel
from gmvladeview import LadeView

class TestatView(QtWidgets.QMainWindow):
    def __init__(self):
        super(TestatView, self).__init__()
        ui_dir = TestatModel.resourcePath("ui")
        if os.name == 'nt':
            uic.loadUi(ui_dir + '/gmvtestat2_win.ui',self)
        else:
            uic.loadUi(ui_dir + '/gmvtestat2.ui',self)
            # uic.loadUi('/Users/dimitrihaas/Library/Mobile Documents/com~apple~CloudDocs/TU Darmstadt/MSc Computional Engineering/Semester 3/Hiwi 2021/IIB_GMV-Testat/gmvtestat2.ui', self)
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

    def folderDialog(self, caption):
        return QtWidgets.QFileDialog.getExistingDirectory(self, caption=caption)

    def fuelleBewertungsUebersicht(self, bewertungsuebersicht):
        self.BatchImportKpLaden_btn.setEnabled(True)
        self.BewertungsUebersicht_table.setRowCount(bewertungsuebersicht.shape[0])
        bewertungsuebersichtArray = bewertungsuebersicht.to_numpy()
        for idx, value in np.ndenumerate(bewertungsuebersichtArray):
            if isinstance(value, float):
                value = f'{value:g}'
            item = QtWidgets.QTableWidgetItem(str(value))
            if idx[1]<6:
                self.BewertungsUebersicht_table.setItem(idx[0],idx[1],item)

    def setzeBewertungsUebersichtZelle(self, row, column, newValue):
        item = QtWidgets.QTableWidgetItem(str(newValue))
        self.BewertungsUebersicht_table.setItem(row, column, item)

    def falscheListeFenster(self, listtyp):
        text = f'''Bitte wähle die {listtyp}-Liste aus!

        Hinweis:
        Der Dateiname muss \'{listtyp}\' enthalten.
        Die Groß-/Kleinschreibung ist dabei unerheblich.'''
        self.infoFenster(text)

    def zeigeLadenHaken(self, button):
        button.setText(u'Laden \u2714')

    def fuelleLabel(self, label, newValue):
        label.setText(f'{newValue}')

    def zeigeVerzeichnisPfad(self, pfad):
        self.pfad_lineEdit.setText(pfad)

    def fuelleLineEdit(self, lineEdit, newValue):
        if isinstance(newValue, str):
            lineEdit.setText(newValue)
        else:
            lineEdit.setText(f'{newValue:g}')

    def aktiviereUIElement(self, element, istAktiv):
        element.setEnabled(istAktiv)

    def aktiviereUIElementeNachAbgabenImport(self):
        self.grenze_label.setEnabled(True)
        self.grenze_spinBox.setEnabled(True)
        self.Speichern_btn.setEnabled(True)
        self.batchPDF_btn.setEnabled(True)

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
        self.bemerkung_plainTextEdit.setPlainText(geklickteZeile['Bemerkungen'])
        self.setzePunktestandLabel(geklickteZeile['Punkte'])

    def setzePunktestandLabel(self, punkte):
        if punkte != '':
            punkte = f'{float(punkte):g}'
        text = f'Gesamtpunktzahl: {punkte} / 30 P'
        self.gesamtpunktzahl_label.setText(text)

    def zeigeOrdnerImFinder(self, pfad):
        if os.name == 'nt':
            winpfad = pfad.replace("/", "\\")
            subprocess.call(f"explorer {winpfad}")
        else:
            subprocess.call(["open", "-R", pfad])

    def infoFenster(self, text):
        box = QtWidgets.QMessageBox(self)
        box.setWindowTitle('Info')
        box.setText(text)
        box.exec()

    def zeigeLadeView(self, title):
        self.ladeView = LadeView(title)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('macintosh')
    
    view = TestatView()
    model = TestatModel()
    controller = TestatController(model, view)
    sys.exit(app.exec())
