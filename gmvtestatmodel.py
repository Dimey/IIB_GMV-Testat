import pandas as pd
import numpy as np
from shutil import copytree
import datetime
import os
from fpdf import FPDF
from testatpdf import TestatPDF

class TestatData():
    def __init__(self):
        super(TestatData, self).__init__() 

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
        teilnehmerliste['Abgabe'] = 'Nein'
        self.bewertungsuebersicht = teilnehmerliste.set_index('Matrikelnummer',drop=False)

    def speichereBewertungsUebersichtAlsCSV(self):
        self.bewertungsuebersicht.to_csv('Ressources/Testat1_Bewertungsuebersicht_SensibleDaten.csv',index=False)

    def ladeBewertungsUebersichtAusCSV(self, pfad):
        self.bewertungsuebersicht = pd.read_csv(pfad).set_index('Matrikelnummer',drop=False).fillna('')

    def ladeBatch(self, path):
        konstruktionsprotokolleListe = []
        abgabenZaehler = 0
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
                        # Weise Abgabenstatus zu
                        self.bewertungsuebersicht.loc[(self.bewertungsuebersicht.Matrikelnummer == int(filename[0:-5])), ['Abgabe','Pfad']] = ['Ja',f'{folderNameCopy}/{foldername}']
                        # kp = pd.read_html(f"{path}/{foldername}/{filename}")[0]
                        # print(f"Konstruktionsprotokoll von {foldername.split('_')[0]} geladen.")
                        # Verkettete xml erstellen
                        # kp.to_xml(f"konstruktionsprotokolle.xml",index=False,root_name=f"id{filename[0:-5]}")
                        # Werte KP aus
                        # self.bepunkteKP(kp)
        return abgabenZaehler

    def bepunkteKP(self, kp):
        # return: punkte
        pass 

    def erstelleZusammenfassung(self):
        pass
    
    def updateBewertungsuebersicht(self, geklickteMatrikelnummer, header, value):
        # Überschreibe den Zellenwert des zugehörigen Kriteriums
        self.bewertungsuebersicht.at[geklickteMatrikelnummer,header] = np.NaN if value == '' else value       
        # Update ebenfalls die Gesamtpunktzahl
        self.bewertungsuebersicht.at[geklickteMatrikelnummer,'Punkte'] = self.gesamtPunktzahl(geklickteMatrikelnummer)

    def gesamtPunktzahl(self, matrikelnummer):
        wertungsSchluessel = [1.5, 1, 1, 1, 0.5, 0.25, 0.625, 1, 0.375, 1, 1]
        return (pd.to_numeric(self.bewertungsuebersicht.loc[matrikelnummer,'Kriterium 1':'Abzug 2'])*wertungsSchluessel).sum()

    def exportPDF(self, matrikelNummer):
        df = self.bewertungsuebersicht.loc[matrikelNummer]
        pdf = TestatPDF(df)
        pdf.output(f"{df['Pfad']}/{matrikelNummer}.pdf")
        return 0