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
        for foldername in os.listdir(path):
            if not foldername.startswith('.'):
                for filename in os.listdir(path + foldername):
                    if filename.endswith('html'):
                        kp = pd.read_html(f"{path+foldername}/{filename}")[0].to_numpy()
                        konstruktionsprotokolleListe.append(kp)
                        # verkettete xml erstellen
                        # kp.to_xml(f"konstruktionsprotokolle.xml",index=False,root_name=f"id{filename[0:-5]}")
                        # werte KP aus
                    else:
                        print('Nicht passend.')
        
        #kpDF = pd.DataFrame(konstruktionsprotokolleListe)
        print(konstruktionsprotokolleListe)

    def bepunkteKP(self, kp):
        # return: punkte
        pass