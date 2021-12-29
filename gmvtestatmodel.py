import pandas as pd
import numpy as np
from shutil import copytree
import os
from fpdf import FPDF
from pdfmodel import PDFModel

class TestatModel():
    def __init__(self):
        super(TestatModel, self).__init__() 
        self.bestehensGrenze = 15
        self.wertungsSchluessel = [1.5, 1, 1, 1, 0.5, 0.25, 0.625, 1, 0.375, 1, 1]
        self.variationsMatrix = [
            [7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9],
            [2.71, 2.72, 2.73, 2.74, 2.75, 2.76, 2.77, 2.78, 2.79, 2.7],
            [-5.2, -5.3, -5.4, -5.5, -5.6, -5.7, -5.8, -5.9, -5, -5.1]]   

    def erzeugeOrdner(self, pfad):
        if not os.path.isdir(pfad):
            os.mkdir(pfad)  

    def ladeTucanListe(self, pfad):
        tucanliste = pd.read_excel(pfad, header = None)
        tucanliste.columns = ['Index', 'Matrikelnummer', 'Nachname', 'Vorname']
        tucanliste = tucanliste.drop('Index', axis = 1)
        self.tucanliste = tucanliste
    
    def ladeMoodleListe(self, pfad):
        moodleliste = pd.read_excel(pfad)
        moodleliste = moodleliste.drop('E-Mail-Adresse', axis = 1)
        self.moodleliste = moodleliste

    def erstelleBewertungsUebersichtAusListen(self):
        teilnehmerliste = pd.merge(self.moodleliste,self.tucanliste,on=['Nachname', 'Vorname'])
        columns_titles = ['Matrikelnummer','Nachname','Vorname']
        teilnehmerliste = teilnehmerliste.reindex(columns = columns_titles)
        teilnehmerliste[['Abgabe', 
        'Punkte', 
        'Bestanden', 
        'Kriterium 1', 
        'Kriterium 2', 
        'Kriterium 3',
        'Kriterium 4',
        'Kriterium 5',
        'Kriterium 6',
        'Kriterium 7',
        'Kriterium 8',
        'Kriterium 9', 
        'Abzug 1',
        'Abzug 2',
        'Bemerkungen', 
        'Pfad']] = ''
        teilnehmerliste['Punkte'] = 0
        teilnehmerliste['Bemerkungen'] = 'Keine Abgabe. Nachtestat möglich.'
        teilnehmerliste[['Abgabe', 'Bestanden']] = 'Nein'
        self.bewertungsuebersicht = teilnehmerliste.set_index('Matrikelnummer',drop=False)
        self.bewertungsuebersicht.sort_values(by=['Nachname', 'Vorname'], inplace=True)

    def speichereBewertungsUebersichtAlsCSV(self):
        self.bewertungsuebersicht.to_csv('Ressources/Testat1_Bewertungsuebersicht_SensibleDaten.csv',index=False)

    def ladeBewertungsUebersichtAusCSV(self, pfad):
        self.bewertungsuebersicht = pd.read_csv(pfad).set_index('Matrikelnummer',drop=False).fillna('')

    def ladeBatch(self, path):
        konstruktionsprotokolleListe = []
        abgabenZaehler = 0
        fehlerZaehler = 0
        # Ordnername für die Kopie aller Abgaben
        folderNameCopy = f"Testatabgaben_Kopie"
        if not os.path.isdir(folderNameCopy): # Wenn noch keine Abgaben-Kopie vorhanden
            print("Kopie wurde angelegt.") # TODO: Infofenster nachrüsten
            copytree(f"{path}", folderNameCopy)
        else:
            print("Es besteht bereits eine Abgaben-Kopie.")
        for foldername in os.listdir(path): # Iteriere über alle Studenten-Ordner
            if not foldername.startswith('.'): # Ignoriere versteckte Dateien
                for filename in os.listdir(f"{path}/{foldername}"):
                    if filename.endswith('html'):
                        abgabenZaehler += 1
                        # Matrikelnummervariation checken
                        matrikelnummer = filename[0:-5]
                        werte = self.extrahiereWerteVonZiffern(matrikelnummer)

                        try:
                            kp = pd.read_html(f"{path}/{foldername}/{filename}")[0]
                            # Weise Abgabenstatus (=Ja) zu
                            self.bewertungsuebersicht.loc[(self.bewertungsuebersicht.Matrikelnummer == int(matrikelnummer)), ['Abgabe','Pfad']] = ['Ja',f'{folderNameCopy}/{foldername}']
                            anzahlFalscheKriterien = self.idCheck(kp, werte)
                            
                            if anzahlFalscheKriterien == 0:
                                self.bewertungsuebersicht.loc[(self.bewertungsuebersicht.Matrikelnummer == int(matrikelnummer)), ['Abzug 1', 'Punkte', 'Bemerkungen']] = [0, '', 'Keine']
                            elif anzahlFalscheKriterien == 1:
                                self.bewertungsuebersicht.loc[(self.bewertungsuebersicht.Matrikelnummer == int(matrikelnummer)), ['Abzug 1', 'Punkte', 'Bemerkungen']] = [-0, '', 'Ein Wert entspricht nicht der Matrikelnummer (kein Abzug).']
                            elif anzahlFalscheKriterien == 2:
                                self.bewertungsuebersicht.loc[(self.bewertungsuebersicht.Matrikelnummer == int(matrikelnummer)), ['Abzug 1', 'Punkte', 'Bemerkungen']] = [-2, '', 'Zwei Werte entsprechen nicht der Matrikelnummer.']
                            elif anzahlFalscheKriterien == 3:
                                self.bewertungsuebersicht.loc[(self.bewertungsuebersicht.Matrikelnummer == int(matrikelnummer)), ['Abzug 1', 'Punkte', 'Bemerkungen']] = [-4, '', 'Drei Werte entsprechen nicht der Matrikelnummer.']
                            else:
                                print(f'ID Check Error! Anzahl der falschen Kriterien: {anzahlFalscheKriterien}.')
                        except:
                            # Weise Abgabenstatus (=Fehler) zu
                            self.bewertungsuebersicht.loc[(self.bewertungsuebersicht.Matrikelnummer == int(matrikelnummer)), ['Abgabe','Pfad']] = ['Fehler',f'{folderNameCopy}/{foldername}']
                            fehlerZaehler += 1

        return abgabenZaehler, fehlerZaehler

    def extrahiereWerteVonZiffern(self, matrikelnummer):
        E, F, G = str(matrikelnummer)[4], str(matrikelnummer)[5], str(matrikelnummer)[6]
        return [self.variationsMatrix[0][int(E)], self.variationsMatrix[1][int(F)], self.variationsMatrix[2][int(G)]] 

    def idCheck(self, kp, werte):
        # Gibt Anzahl falscher Kriterien zurück
        werteStudent = kp['Wert'].unique()
        schieberegler, zKoordinate, ebenenHoehe = werte[0], werte[1], werte[2]
        return 3 - np.count_nonzero((np.where((werteStudent == f'SchiebereglerE = {schieberegler}') |
        (werteStudent == f'Augpunkt = (2.75, -2.49, {zKoordinate})'), True, False)) |
        (pd.Series(werteStudent).str.slice(start=4).str.match(f'z = {ebenenHoehe}')))

    def anzahlFehler(self):
        df = self.bewertungsuebersicht
        return len(df[(df['Abgabe'] == 'Fehler')].index)

    def anzahlInSpalte(self, spalte):
        df = self.bewertungsuebersicht
        return len(df[(df[spalte] == 'Ja') | (df[spalte] == 'Fehler')].index)

    def anzahlBewertet(self):
        df = self.bewertungsuebersicht
        return len(df[(df['Punkte'] != '')].index)
    
    def updateBewertungsUebersichtZelle(self, geklickteMatrikelnummer, header, value):
        # Überschreibe den Zellenwert des zugehörigen Kriteriums
        self.bewertungsuebersicht.at[geklickteMatrikelnummer,header] = np.NaN if value == '' else value       
        # Update ebenfalls die Gesamtpunktzahl und den Bestandenstatus, wenn Punkte verändert wurden
        if header != 'Bemerkungen':
            gesamtPunktzahl = self.gesamtPunktzahlStudent(geklickteMatrikelnummer)
            self.bewertungsuebersicht.at[geklickteMatrikelnummer,'Punkte'] = gesamtPunktzahl
            self.bewertungsuebersicht.at[geklickteMatrikelnummer,'Bestanden'] = 'Ja' if gesamtPunktzahl >= self.bestehensGrenze else 'Nein'

    def updateBestandenStatusAllerStudenten(self):
        df = self.bewertungsuebersicht
        for index_i in df[(df['Abgabe'] == 'Ja') & (df['Punkte'] != '')].index:
            bestandenStatus = 'Ja' if df.loc[index_i,'Punkte'] >= self.bestehensGrenze else 'Nein'
            self.bewertungsuebersicht.at[index_i,'Bestanden'] = bestandenStatus
        df = df.reset_index(drop=True)
        # rows aller fraglichen Studenten
        return df[(df['Abgabe'] == 'Ja') & (df['Punkte'] != '')].index 

    def gesamtPunktzahlStudent(self, matrikelnummer):
        return np.clip((pd.to_numeric(self.bewertungsuebersicht.loc[matrikelnummer,'Kriterium 1':'Abzug 2'])*self.wertungsSchluessel).sum(), a_min=0, a_max=30)

    def gesamtPunktzahl(self):
        return pd.to_numeric(self.bewertungsuebersicht.Punkte).sum()

    def exportPDF(self, matrikelNummer):
        df = self.bewertungsuebersicht.loc[matrikelNummer]
        ws = self.wertungsSchluessel
        bg = self.bestehensGrenze
        pfad = df['Pfad']
        pdf = PDFModel(df,ws,bg)
        pdf.output(f"{pfad}{'/' if pfad != '' else 'Studenten ohne Abgabe/'}{matrikelNummer}.pdf")