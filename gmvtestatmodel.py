import pandas as pd
import numpy as np
import os

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

    def erstelleBewertungsUebersicht(self):
        teilnehmerliste = pd.merge(self.moodleliste,self.tucanliste,on=['Nachname', 'Vorname'])
        columns_titles = ['Matrikelnummer','Nachname','Vorname']
        teilnehmerliste = teilnehmerliste.reindex(columns = columns_titles)
        teilnehmerliste[['Punkte','Bestanden']] = ''
        self.bewertungsuebersicht = teilnehmerliste

    def ladeBatch(self, path):
        konstruktionsprotokolleListe = []
        for foldername in os.listdir(path): # Iteriere über alle Studenten-Ordner
            if not foldername.startswith('.'): # Ignoriere versteckte Dateien
                for filename in os.listdir(f"{path}/{foldername}"):
                    if filename.endswith('html'):
                        kp = pd.read_html(f"{path}/{foldername}/{filename}")[0]
                        # Verkettete xml erstellen
                        # kp.to_xml(f"konstruktionsprotokolle.xml",index=False,root_name=f"id{filename[0:-5]}")
                        # Werte KP aus
                        # self.bepunkteKP(kp)
                    else:
                        print('Nicht passend.')

    def bepunkteKP(self, kp):
        # return: punkte
        pass 