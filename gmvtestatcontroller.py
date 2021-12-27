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
        self.view.Speichern_btn.clicked.connect(self.speichereAenderungen)
        self.view.Laden_btn.clicked.connect(self.ladeSicherungsDatei)
        self.view.zurAbgabe_btn.clicked.connect(self.rufeOrdnerImFileExplorer)
        self.view.BewertungsUebersicht_table.cellClicked.connect(self.uebergebeBewertung)
        self.view.krit1_lineEdit.editingFinished.connect(partial(self.speichereKrit,self.view.krit1_lineEdit,"Kriterium 1"))
        self.view.krit2_lineEdit.editingFinished.connect(partial(self.speichereKrit,self.view.krit2_lineEdit,"Kriterium 2"))
        self.view.krit3_lineEdit.editingFinished.connect(partial(self.speichereKrit,self.view.krit3_lineEdit,"Kriterium 3"))
        self.view.krit4_lineEdit.editingFinished.connect(partial(self.speichereKrit,self.view.krit4_lineEdit,"Kriterium 4"))
        self.view.krit5_lineEdit.editingFinished.connect(partial(self.speichereKrit,self.view.krit5_lineEdit,"Kriterium 5"))
        self.view.krit6_lineEdit.editingFinished.connect(partial(self.speichereKrit,self.view.krit6_lineEdit,"Kriterium 6"))
        self.view.krit7_lineEdit.editingFinished.connect(partial(self.speichereKrit,self.view.krit7_lineEdit,"Kriterium 7"))
        self.view.krit8_lineEdit.editingFinished.connect(partial(self.speichereKrit,self.view.krit8_lineEdit,"Kriterium 8"))
        self.view.krit9_lineEdit.editingFinished.connect(partial(self.speichereKrit,self.view.krit9_lineEdit,"Kriterium 9"))
        self.view.abzug1_lineEdit.editingFinished.connect(partial(self.speichereKrit,self.view.abzug1_lineEdit,"Abzug 1"))
        self.view.abzug2_lineEdit.editingFinished.connect(partial(self.speichereKrit,self.view.abzug2_lineEdit,"Abzug 2"))
        self.view.grenze_spinBox.valueChanged.connect(self.neueGrenzeErhalten)
        self.view.bemerkung_lineEdit.editingFinished.connect(partial(self.speichereBemerkung,self.view.bemerkung_lineEdit))
        self.view.pdfExport_btn.clicked.connect(self.erzeugePDF)
        self.view.batchPDF_btn.clicked.connect(self.erzeugeBatchPDF)

    def oeffneTucanListe(self):
        try:
            filename = self.view.fileDialog('xlsx')
            if 'tucan' in filename[0].lower():
                self.model.ladeTucanListe(filename[0])
                self.view.zeigeLadenHaken(self.view.TucanListeLaden_btn)
                self.view.fuelleLabel(self.view.AnzahlTucanTeilnehmer_label, self.model.tucanliste.shape[0])
                if hasattr(self.model, 'moodleliste'):
                    self.model.erstelleBewertungsUebersicht()
                    self.view.fuelleBewertungsUebersicht(self.model.bewertungsuebersicht)
                    self.uebergebeStatistik()
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
                self.view.fuelleLabel(self.view.AnzahlMoodleTeilnehmer_label, self.model.moodleliste.shape[0])
                if hasattr(self.model, 'tucanliste'):
                    self.model.erstelleBewertungsUebersichtAusListen()
                    self.view.fuelleBewertungsUebersicht(self.model.bewertungsuebersicht)
                    self.uebergebeStatistik()
            else:
                self.view.falscheListeFenster('Moodle')  
        except:
            print('Die MoodleListe konnte nicht geladen werden.')

    def oeffneKPOrdner(self):
        path = self.view.folderDialog()
        if path:
            self.view.zeigeLadenHaken(self.view.BatchImportKpLaden_btn)
            anzahlAbgaben, fehler = self.model.ladeBatch(path)
            self.view.fuelleLabel(self.view.fehler_label, fehler)
            self.view.fuelleLabel(self.view.AnzahlAbgaben_label, anzahlAbgaben)
            self.view.fuelleBewertungsUebersicht(self.model.bewertungsuebersicht)

    def speichereAenderungen(self):
        self.model.speichereBewertungsUebersichtAlsCSV()

    def ladeSicherungsDatei(self):
        path = self.view.fileDialog('csv')[0]
        if path:
            self.model.ladeBewertungsUebersichtAusCSV(path)
            self.view.fuelleBewertungsUebersicht(self.model.bewertungsuebersicht)
            self.view.fuelleLabel(self.view.fehler_label, self.model.anzahlFehler())
            self.uebergebeStatistik()

    def uebergebeBewertung(self, row, column):
        self.geklickteMatrikelnummer = int(self.view.BewertungsUebersicht_table.item(row, 0).text())
        self.geklickteZeile = self.model.bewertungsuebersicht.loc[self.geklickteMatrikelnummer]

        # Logik zum Aktivieren/Deaktivieren des Zur-Abgabe-Buttons
        if self.geklickteZeile['Pfad'] != '':
            self.view.aktiviereBewertungsdetails(True)
        else:
            self.view.aktiviereBewertungsdetails(False)

        # Fülle alle Bewertungsdetails des ausgewählten Studenten
        self.view.fuelleBewertungsDetails(self.geklickteZeile.fillna(''))

    def uebergebeStatistik(self):
        anzahlAbgaben = self.model.anzahlInSpalte('Abgabe')
        anzahlBestandenerAbgaben = self.model.anzahlInSpalte('Bestanden')
        anzahlBewertet = self.model.anzahlBewertet()
        anteilBestanden = ('%.2f' % (anzahlBestandenerAbgaben/anzahlBewertet * 100)) if anzahlBewertet != 0 else 0
        gesamtPunktzahl = self.model.gesamtPunktzahl()
        durchschnitt = round(gesamtPunktzahl/anzahlBewertet,2) if anzahlBewertet != 0 else 0
        self.view.fuelleLabel(self.view.AnzahlAbgaben_label, anzahlAbgaben)
        self.view.fuelleLabel(self.view.bestanden_label, f'{anzahlBestandenerAbgaben} ({anteilBestanden}%)')
        self.view.fuelleLabel(self.view.unbewertet_label, anzahlAbgaben-anzahlBewertet)
        self.view.fuelleLabel(self.view.bewertet_label, anzahlBewertet)    
        self.view.fuelleLabel(self.view.durchschnitt_label, durchschnitt)

    def speichereKrit(self, lineEditObj, header):
        self.model.updateBewertungsUebersichtZelle(self.geklickteMatrikelnummer,header,lineEditObj.text().replace(',','.'))
        df = self.model.bewertungsuebersicht.reset_index(drop=True)
        row = df[df['Matrikelnummer'] == self.geklickteMatrikelnummer].index[0] 
        columnPunkte = df.columns.get_loc("Punkte")
        neueGesamtPunkte = self.model.bewertungsuebersicht.at[self.geklickteMatrikelnummer,'Punkte']
        self.view.setzeBewertungsUebersichtZelle(row, columnPunkte, neueGesamtPunkte)
        columnBestanden = df.columns.get_loc("Bestanden")
        neuerBestandenStatus = self.model.bewertungsuebersicht.at[self.geklickteMatrikelnummer,'Bestanden']
        self.view.setzeBewertungsUebersichtZelle(row, columnBestanden, neuerBestandenStatus)
        self.view.setzePunktestandLabel(self.model.gesamtPunktzahlStudent(self.geklickteMatrikelnummer))    

        self.uebergebeStatistik()    

    def speichereBemerkung(self, lineEditObj):
        self.model.updateBewertungsUebersichtZelle(self.geklickteMatrikelnummer,f"Bemerkungen",lineEditObj.text())

    def neueGrenzeErhalten(self, newValue):
        self.model.bestehensGrenze = newValue
        rows = self.model.updateBestandenStatusAllerStudenten()
        df = self.model.bewertungsuebersicht.reset_index(drop=True)
        column = df.columns.get_loc("Bestanden")
        for row in rows:
            neuerBestandenStatus = df.at[row,'Bestanden']
            self.view.setzeBewertungsUebersichtZelle(row, column, neuerBestandenStatus)
        self.uebergebeStatistik()

    def rufeOrdnerImFileExplorer(self):
        self.view.zeigeOrdnerImFinder(self.geklickteZeile['Pfad'])

    def erzeugePDF(self):
        pdfStatus = self.model.exportPDF(self.geklickteMatrikelnummer)
        self.view.pdfStatusFenster(pdfStatus)

    def erzeugeBatchPDF(self):
        df = self.model.bewertungsuebersicht
        matrikelNummern = df[(df['Abgabe'] == 'Ja') & (df['Punkte'] != '')].index

        for matrikelNummer in matrikelNummern:
            self.geklickteMatrikelnummer = matrikelNummer
            self.erzeugePDF()