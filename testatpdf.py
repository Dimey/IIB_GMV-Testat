import datetime
from fpdf import FPDF

class TestatPDF(FPDF):
    def __init__(self, df):
        super().__init__('P','mm')
        self.data = df
        self.constructPDF(df)

        # Meta data
        self.set_title(f"Testatbewertung für {df['Vorname']} {df['Nachname']}")
        self.set_author(f'Pascal Mosler')

    def header(self):
        # IIB Logo
        self.image(name='Assets/iib_logo.png', x=170, y=10, w=30)
        # Font
        self.set_font(family='Arial', style='B', size=16)
        # Title
        self.cell(w=0, h=8, txt='Geometrische Modellierung und Visualisierung I', border=False, ln=1, align='L')
        self.set_font('Arial', '', 14)
        self.cell(w=130, h=8, txt='Wintersemester 2021/2022', align='L')
        # Line break
        self.ln(24)

    def footer(self):
        # Set position
        self.set_y(-16)
        # Set font and color
        self.set_font(family='Arial', style='I', size=10)
        self.set_text_color(0,0,0)
        # Set text
        self.cell(w=0, h=8, txt=f'PDF erzeugt am {str(datetime.datetime.now())[0:19]} von Pascal Mosler', align='C')

    def constructPDF(self, df):
        # Add a page
        self.add_page()

        # Name and student id
        self.set_font(family='Arial', style='B', size=14)
        self.cell(w=0, h=8, txt=f'Bewertung des Testats vom 13. Dezember 2021', border=False, ln=1, align='L')
        self.set_font(family='Arial', style='U', size=12)
        self.cell(w=35, h=8, txt='Name:', align='L')
        self.set_font(family='Arial', style='', size=12)
        self.cell(w=35, h=8, txt=f"{df['Vorname']} {df['Nachname']}", align='L', ln=1)
        self.set_font(family='Arial', style='U', size=12)
        self.cell(w=35, h=8, txt='Matrikelnummer:', align='L')
        self.set_font(family='Arial', style='', size=12)
        self.cell(w=35, h=8, txt=f"{df['Matrikelnummer']}", align='L')
        self.ln(24)

        # tasks and gradings
        # task 1
        self.set_font(family='Arial', style='b', size=12)
        self.cell(w=0, h=8, txt=f"Aufgabe 1: Schattenwurf", align='L')
        self.set_font(family='Courier', style='b', size=12)
        punkteAufg1 = float(df['Kriterium 1'])*1.5 + float(df['Kriterium 2']) + float(df['Kriterium 3']) + float(df['Kriterium 4'])
        self.cell(w=0, h=8, txt=f"({punkteAufg1} / 12 Punkte)", align='R', ln=1)
        # crit 1
        self.set_font(family='Arial', style='', size=12)
        self.cell(w=0, h=8, txt=f"Schatteneckpunkte", align='L')
        self.set_font(family='Courier', style='', size=12)
        self.cell(w=0, h=8, txt=f"({float(df['Kriterium 1'])*1.5} / 6 Punkte)", align='R', ln=1)
        # crit 2
        self.set_font(family='Arial', style='', size=12)
        self.cell(w=0, h=8, txt=f"Stamm ausgespart", align='L')
        self.set_font(family='Courier', style='', size=12)
        self.cell(w=0, h=8, txt=f"({df['Kriterium 2']} / 1 Punkte)", align='R', ln=1)
        # crit 3
        self.set_font(family='Arial', style='', size=12)
        self.cell(w=0, h=8, txt=f"Vielecke zwischen Schatteneckpunkten", align='L')
        self.set_font(family='Courier', style='', size=12)
        self.cell(w=0, h=8, txt=f"({df['Kriterium 3']} / 4 Punkte)", align='R', ln=1)
        # crit 4
        self.set_font(family='Arial', style='', size=12)
        self.cell(w=0, h=8, txt=f"Vielecke verschneidungsfrei", align='L')
        self.set_font(family='Courier', style='', size=12)
        self.cell(w=0, h=8, txt=f"({df['Kriterium 4']} / 1 Punkte)", align='R', ln=1)
        self.ln(16)

        # task 2
        self.cell(w=0, h=8, txt=f"Aufgabe 2: Dreitafelprojektion ({df['Kriterium 2']}/10 Punkte)", align='L')
        self.ln(16)

        # task 3
        self.cell(w=0, h=8, txt=f"Aufgabe 3: Abbildung 3D auf 2D ({df['Kriterium 3']}/8 Punkte)", align='L')
        self.ln(24)

        # notes
        self.cell(w=0, h=8, txt=f'Bemerkungen', ln=1, align='L')
        self.set_font(family='Arial', style='', size=12)
        self.multi_cell(w=100, h=8, txt=f"{df['Bemerkungen']}", align='L')

        # final grade
        punkteGesamt = punkteAufg1
        bestehensGrenze = 15
        self.set_y(-48)
        self.set_font(family='Arial', style='B', size=12)
        self.cell(117)
        self.cell(w=76, h=16, txt='', border=True, align='R')
        self.cell(w=0, h=8, txt=f'Gesamtpunktzahl:  {punkteGesamt} / 30 ({int(round(punkteGesamt/30,2))*100}%)', align='R', ln=1)
        if punkteGesamt > bestehensGrenze:
            self.set_text_color(102,164,99)
            self.cell(w=0, h=8, txt=f'BESTANDEN', align='R')
        else:
            self.set_text_color(191,70,39)
            self.cell(w=0, h=8, txt=f'NICHT BESTANDEN', align='R')