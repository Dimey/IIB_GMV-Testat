import pandas as pd
import numpy as np
from shutil import copytree
import datetime
import os
from fpdf import FPDF
from testatpdf import TestatPDF
from testatpdf_v2 import TestatPDF2

class TestatData():
    def __init__(self):
        super(TestatData, self).__init__() 
        self.bestehensGrenze = 15
        self.variationsMatrix = [
            [7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9],
            [2.71, 2.72, 2.73, 2.74, 2.75, 2.76, 2.77, 2.78, 2.79, 2.7],
            [-5.2, -5.3, -5.4, -5.5, -5.6, -5.7, -5.8, -5.9, -5, -5.1]]

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
        teilnehmerliste[['Abgabe', 'Bestanden']] = 'Nein'
        self.bewertungsuebersicht = teilnehmerliste.set_index('Matrikelnummer',drop=False)

    def speichereBewertungsUebersichtAlsCSV(self):
        self.bewertungsuebersicht.to_csv('Ressources/Testat1_Bewertungsuebersicht_SensibleDaten.csv',index=False)

    def ladeBewertungsUebersichtAusCSV(self, pfad):
        self.bewertungsuebersicht = pd.read_csv(pfad).set_index('Matrikelnummer',drop=False).fillna('')

    def ladeBatch(self, path):
        konstruktionsprotokolleListe = []
        abgabenZaehler = 0
        fehlerZaehler = 0
        schiebereglerFehler = 0
        datum = datetime.datetime.now()
        # Ordnername für die Kopie aller Abgaben
        folderNameCopy = f"Testatabgaben_{datum.day}{datum.month}{datum.year}"
        if not os.path.isdir(folderNameCopy): # Wenn noch keine Abgaben-Kopie vorhanden
            print("Kopie wurde angelegt.")
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
                            if self.idCheck(kp, werte) == False:
                                schiebereglerFehler += 1
                        except:
                            # Weise Abgabenstatus (=Fehler) zu
                            self.bewertungsuebersicht.loc[(self.bewertungsuebersicht.Matrikelnummer == int(matrikelnummer)), ['Abgabe','Pfad']] = ['Fehler',f'{folderNameCopy}/{foldername}']
                            fehlerZaehler += 1
                        
                        # print(kp)
                        # status = self.idCheck(kp)
                        # print(f"Konstruktionsprotokoll von {foldername.split('_')[0]} geladen.")
                        # Verkettete xml erstellen
                        # kp.to_xml(f"konstruktionsprotokolle.xml",index=False,root_name=f"id{filename[0:-5]}")
                        # Werte KP aus
                        # self.bepunkteKP(kp)
        print(schiebereglerFehler)
        return abgabenZaehler, fehlerZaehler

    def extrahiereWerteVonZiffern(self, matrikelnummer):
        E, F, G = str(matrikelnummer)[4], str(matrikelnummer)[5], str(matrikelnummer)[6]
        return [self.variationsMatrix[0][int(E)], self.variationsMatrix[1][int(F)], self.variationsMatrix[2][int(G)]] 

    def idCheck(self, kp, werte):
        schieberegler, zKoordinate, ebenenHoehe = werte[0], werte[1], werte[2]
        check = f'SchiebereglerE = {schieberegler}' in kp['Wert'].unique()
        return check
        # return: 0 / -0 / -2 / -4 / -30

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
        # Update ebenfalls die Gesamtpunktzahl
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
        wertungsSchluessel = [1.5, 1, 1, 1, 0.5, 0.25, 0.625, 1, 0.375, 1, 1]
        return (pd.to_numeric(self.bewertungsuebersicht.loc[matrikelnummer,'Kriterium 1':'Abzug 2'])*wertungsSchluessel).sum()

    def gesamtPunktzahl(self):
        return pd.to_numeric(self.bewertungsuebersicht.Punkte).sum()

    def exportPDF(self, matrikelNummer):
        df = self.bewertungsuebersicht.loc[matrikelNummer]
        pdf = TestatPDF2(df)
        pdf.output(f"{df['Pfad']}/{matrikelNummer}.pdf")
        return 0