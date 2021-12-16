from functools import partial

class TestatController():
    def __init__(self, model, view):
        super(TestatController, self).__init__()
        self.view = view
        self.model = model
        
        self.initializeModel()
        self.initializeUI()
        
        # Connect signals and slots
        self.connectSignals()
        
    def initializeModel(self):  
        pass
        
    def initializeUI(self):
        # Setze Focus auf den Laden Button
        self.view.TucanListeLaden_btn.setFocus();
        
    def connectSignals(self):
        self.view.TucanListeLaden_btn.clicked.connect(self.oeffneTucanListe)
        self.view.MoodleListeLaden_btn.clicked.connect(self.oeffneMoodleListe)
        self.view.BatchImportKpLaden_btn.clicked.connect(self.oeffneKPOrdner)
        self.view.AenderungenSpeichern_btn.clicked.connect(self.speichereAenderungen)
        self.view.LadeSicherungsDatei_btn.clicked.connect(self.ladeSicherungsDatei)
        self.view.zurAbgabe_btn.clicked.connect(self.rufeOrdnerImFileExplorer)
        self.view.BewertungsUebersicht_table.cellClicked.connect(self.uebergebeBewertung)
        self.view.krit1_lineEdit.editingFinished.connect(partial(self.speichereKrit,self.view.krit1_lineEdit,1))
        self.view.krit2_lineEdit.editingFinished.connect(partial(self.speichereKrit,self.view.krit2_lineEdit,2))
        self.view.krit3_lineEdit.editingFinished.connect(partial(self.speichereKrit,self.view.krit3_lineEdit,3))
        self.view.pdfExport_btn.clicked.connect(self.erzeugePDF)

    def oeffneTucanListe(self):
        try:
            filename = self.view.fileDialog('xlsx')
            if 'tucan' in filename[0].lower():
                self.model.ladeTucanListe(filename[0])
                self.view.zeigeLadenHaken(self.view.TucanListeLaden_btn)
                self.view.zeigeAnzahl(self.view.AnzahlTucanTeilnehmer_label, self.model.tucanliste.shape[0])
                if hasattr(self.model, 'moodleliste'):
                    self.model.erstelleBewertungsUebersicht()
                    self.view.zeigeBewertungsUebersicht(self.model.bewertungsuebersicht)
            else:
                self.view.falscheListeFenster('TUCaN')    
        except:
            print('Die TucanListe konnte nicht geladen werden.')

    def oeffneMoodleListe(self):
        try:
            filename = self.view.fileDialog('xlsx')
            if 'moodle' in filename[0].lower():
                self.model.ladeMoodleListe(filename[0])
                self.view.zeigeLadenHaken(self.view.MoodleListeLaden_btn)
                self.view.zeigeAnzahl(self.view.AnzahlMoodleTeilnehmer_label, self.model.moodleliste.shape[0])
                if hasattr(self.model, 'tucanliste'):
                    self.model.erstelleBewertungsUebersichtAusListen()
                    self.view.zeigeBewertungsUebersicht(self.model.bewertungsuebersicht)
            else:
                self.view.falscheListeFenster('Moodle')  
        except:
            print('Die MoodleListe konnte nicht geladen werden.')

    def oeffneKPOrdner(self):
        path = self.view.folderDialog()
        if path:
            self.view.zeigeLadenHaken(self.view.BatchImportKpLaden_btn)
            anzahlAbgaben = self.model.ladeBatch(path)
            self.view.zeigeAnzahl(self.view.AnzahlAbgaben_label, anzahlAbgaben)
            self.view.zeigeBewertungsUebersicht(self.model.bewertungsuebersicht)

    def speichereAenderungen(self):
        self.model.speichereBewertungsUebersichtAlsCSV()

    def ladeSicherungsDatei(self):
        pfad = self.view.fileDialog('csv')[0]
        self.model.ladeBewertungsUebersichtAusCSV(pfad)
        self.view.zeigeBewertungsUebersicht(self.model.bewertungsuebersicht)

    def zeigeZusammenfassung(self):
        self.model.erstelleZusammenfassung()

    def uebergebeBewertung(self, row, column):
        self.view.aktiviereBewertungsdetails(True)
        self.geklickteMatrikelnummer = int(self.view.BewertungsUebersicht_table.item(row, 0).text())
        self.geklickteZeile = self.model.bewertungsuebersicht.loc[self.geklickteMatrikelnummer]

        # Logik zum Aktivieren/Deaktivieren des Zur-Abgabe-Buttons
        if self.geklickteZeile['Pfad'] == '':
            self.view.zurAbgabe_btn.setEnabled(False)
        else:
            self.view.zurAbgabe_btn.setEnabled(True)

        # Fülle alle Bewertungsdetails des ausgewählten Studenten
        self.view.fuelleBewertungsDetails(self.geklickteZeile.fillna(''))

    def speichereKrit(self, lineEditObj, kritNr):
        self.model.updateBewertungsuebersicht(self.geklickteMatrikelnummer,f"Kriterium {kritNr}",lineEditObj.text())
        self.view.zeigeBewertungsUebersicht(self.model.bewertungsuebersicht)
        self.view.setzePunktestandLabel(self.model.gesamtPunktzahl(self.geklickteMatrikelnummer))

    def rufeOrdnerImFileExplorer(self):
        self.view.zeigeOrdnerImFinder(self.geklickteZeile['Pfad'])

    def erzeugePDF(self):
        pdfStatus = self.model.exportPDF(self.geklickteMatrikelnummer)
        self.view.pdfStatusFenster(pdfStatus)