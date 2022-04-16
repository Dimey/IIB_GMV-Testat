import os
import sys
import pandas as pd
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from shutil import copytree
from datetime import datetime
from pdfmodel import PDFModel
from pdfmodel2 import PDFModel2

class TestatModel():

    @classmethod
    def resourcePath(cls, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def __init__(self):
        super(TestatModel, self).__init__() 
        self.bestehensGrenze = 15
        self.wertungsSchluessel = PDFModel2.wertungsSchluessel
        self.variationsMatrix = PDFModel2.variationsMatrix
        self.workingDir = os.path.abspath(os.getcwd())

    def aendereVerzeichnisPfad(self, pfad):
        os.chdir(pfad)
        self.workingDir = pfad

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
        now = datetime.now()
        date_time = now.strftime("date%d%m%Y_time%H%M%S")
        self.bewertungsuebersicht.to_csv(f'GMV Testat Tool/Save Files/savefile_{date_time}.csv',index=False)

    def ladeBewertungsUebersichtAusCSV(self, pfad):
        self.bewertungsuebersicht = pd.read_csv(pfad).set_index('Matrikelnummer',drop=False).fillna('')

    def pfadeAllerAbgaben(self, pfad):
        # Ordnername für die Kopie aller Abgaben
        copyFolderName = f"GMV Testat Tool/Testatabgaben_Kopie"
        if not os.path.isdir(copyFolderName): # Wenn noch keine Abgaben-Kopie vorhanden
            print("Kopie wurde angelegt.") # TODO: Infofenster nachrüsten
            copytree(f"{pfad}", copyFolderName)
        else:
            print("Es besteht bereits eine Abgaben-Kopie.")
        htmlDateien = []
        for dirpath, subdirs, files in os.walk(copyFolderName):
            for x in files:
                if x.endswith(".html"):
                    htmlDateien.append(os.path.join(dirpath, x))
        return htmlDateien
        
    def ladeAbgabe(self, path):
        matrikelnummer = path[-12:-5]
        ordnerPfad = path[0:-13]
        werte = self.extrahiereWerteVonZiffern(matrikelnummer)

        try:
            kp = pd.read_html(path)[0]
            # Weise Abgabenstatus (=Ja) zu
            self.bewertungsuebersicht.loc[(self.bewertungsuebersicht.Matrikelnummer == int(matrikelnummer)), ['Abgabe','Pfad']] = ['Ja',ordnerPfad]
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
            
            return True
        except:
            # Weise Abgabenstatus (=Fehler) zu
            self.bewertungsuebersicht.loc[(self.bewertungsuebersicht.Matrikelnummer == int(matrikelnummer)), ['Abgabe','Pfad']] = ['Fehler',ordnerPfad]
            return False

    def extrahiereWerteVonZiffern(self, matrikelnummer):
        E, F, G = str(matrikelnummer)[4], str(matrikelnummer)[5], str(matrikelnummer)[6]
        return [self.variationsMatrix[0][int(E)], self.variationsMatrix[1][int(F)], self.variationsMatrix[2][int(G)]] 

    def idCheck(self, kp, werte):
        return PDFModel2.idCheck(kp, werte)

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
        img_dir = TestatModel.resourcePath("imgs")
        pdf = PDFModel2(df,ws,bg,img_dir)
        pdf.output(f"{pfad}{'/' if pfad != '' else 'GMV Testat Tool/Studenten ohne Abgabe/'}{matrikelNummer}.pdf")