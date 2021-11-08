#from PyQt5 import QtWidgets

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
        pass
        
    def connectSignals(self):
        self.view.TucanListeLaden_btn.clicked.connect(self.oeffneTucanListe)
        self.view.MoodleListeLaden_btn.clicked.connect(self.oeffneMoodleListe)
        self.view.BatchImportKpLaden_btn.clicked.connect(self.oeffneKPOrdner)

    # TODO: Parametrisieren
    def oeffneTucanListe(self):
        try:
            filename = self.view.fileDialog('xlsx')
            if 'tucan' in filename[0].lower():
                self.model.ladeTucanListe(filename[0])
                self.view.zeigeLadenHaken(self.view.TucanListeLaden_btn)
                self.view.zeigeAnzahl(self.view.AnzahlTucanTeilnehmer_label, self.model.tucanliste)
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
                self.view.zeigeAnzahl(self.view.AnzahlMoodleTeilnehmer_label, self.model.moodleliste)
                if hasattr(self.model, 'tucanliste'):
                    self.model.erstelleBewertungsUebersicht()
                    self.view.zeigeBewertungsUebersicht(self.model.bewertungsuebersicht)
            else:
                self.view.falscheListeFenster('Moodle')  
        except:
            print('Die MoodleListe konnte nicht geladen werden.')

    def oeffneKPOrdner(self):
        path = self.view.folderDialog()
        if path:
            path += '/'
            self.view.zeigeLadenHaken(self.view.BatchImportKpLaden_btn)
            self.model.ladeBatch(path)