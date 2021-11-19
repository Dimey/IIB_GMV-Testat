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
        #self.model.checkAndLoadSave
        pass
        
    def initializeUI(self):
        pass
        
    def connectSignals(self):
        self.view.TucanListeLaden_btn.clicked.connect(self.oeffneTucanListe)
        self.view.MoodleListeLaden_btn.clicked.connect(self.oeffneMoodleListe)
        self.view.BatchImportKpLaden_btn.clicked.connect(self.oeffneKPOrdner)
        self.view.AenderungenSpeichern_btn.clicked.connect(self.speichereAenderungen)
        self.view.LadeSicherungsDatei_btn.clicked.connect(self.ladeSicherungsDatei)
        self.view.BewertungsUebersicht_table.cellClicked.connect(self.uebergebeBewertung)
        self.view.krit1_lineEdit.editingFinished.connect(self.speichereKrit1)
        self.view.krit2_lineEdit.editingFinished.connect(self.speichereKrit2)
        self.view.krit3_lineEdit.editingFinished.connect(self.speichereKrit3)

    # TODO: Parametrisieren
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
            self.model.ladeBatch(path)

    def speichereAenderungen(self):
        self.model.speichereBewertungsUebersichtAlsCSV()

    def ladeSicherungsDatei(self):
        pfad = self.view.fileDialog('csv')[0]
        self.model.ladeBewertungsUebersichtAusCSV(pfad)
        self.view.zeigeBewertungsUebersicht(self.model.bewertungsuebersicht)

    def zeigeZusammenfassung(self):
        self.model.erstelleZusammenfassung()
        pass

    def uebergebeBewertung(self, row, column):
        self.geklickteMatrikelnummer = int(self.view.BewertungsUebersicht_table.item(row, 0).text())
        print(self.model.bewertungsuebersicht)
        geklickteZeile = self.model.bewertungsuebersicht.loc[self.geklickteMatrikelnummer]
        self.view.zeigeBewertungsDetails(geklickteZeile)

    def speichereKrit1(self):
        self.model.updateBewertungsuebersicht(self.geklickteMatrikelnummer,"Kriterium 1",self.view.krit1_lineEdit.text())

    def speichereKrit2(self):
        pass

    def speichereKrit3(self):
        pass