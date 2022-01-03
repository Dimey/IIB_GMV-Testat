import datetime
import pandas as pd
from fpdf import FPDF

class PDFModel(FPDF):
    def __init__(self, df, ws, bg):
        super().__init__('P','mm')
        self.data = df
        self.bestehensGrenze = bg

        # Meta data
        self.set_title(f"Testatbewertung für {df['Vorname']} {df['Nachname']}")
        self.set_author(f'GMV I WS21/22')

        # Set document parameters
        self.textHeight = 11
        self.titleHeight = 13
        self.cellHeight = 8
        self.cellMaxWidth = 170
        self.cellWidthLeft = 135.9
        self.cellWidthLeftPart = 42.5
        self.cellWidthRight = 26.1
        self.font = 'Courier'

        self.set_auto_page_break(auto=False)
        self.set_left_margin(20)
        self.set_right_margin(20)
        self.set_top_margin(20)
        self.constructPDF(pd.to_numeric(df['Kriterium 1':'Abzug 2'])*ws)

    def header(self):
        # IIB Logo
        self.image(name='Assets/iib_logo.png', x=160, y=22, w=25)
        # Font
        self.set_font(family='Arial', style='B', size=16)
        # Title
        self.cell(w=0, h=8, txt='Geometrische Modellierung und Visualisierung I', border=False, ln=1, align='L')
        self.set_font('Arial', '', 14)
        self.cell(w=130, h=8, txt='Wintersemester 2021/2022', align='L')
        # Line break
        self.ln(16)

    def footer(self):
        # Set position
        self.set_y(-20)
        # Set font and color
        self.set_font(family='Arial', style='I', size=10)
        self.set_text_color(0,0,0)
        # Set text
        self.cell(w=0, h=8, txt=f'Dokument erzeugt am {str(datetime.datetime.now())[0:19]}', align='C')

    def emptyLine(self):
        self.cell(w=0, h=self.cellHeight, border=True, ln=1)

    def twoPartCell_subTask(self, txt1, pt1, pt2):
        self.set_font(family=self.font, style='', size=self.textHeight)
        self.cell(w=self.cellWidthLeft, h=self.cellHeight, txt=txt1, align='L', border=True)
        self.set_font(family=self.font, style='B', size=self.textHeight)
        self.cell(w=15.5, h=self.cellHeight, txt=f'{pt1:g}', align='R', border='TB')
        self.set_font(family=self.font, style='', size=self.textHeight)
        self.cell(w=3.1, h=self.cellHeight, txt='/', align='C', border='TB')
        self.cell(w=15.5, h=self.cellHeight, txt=f'{pt2}', align='L', border='TBR', ln=1)

    def twoPartCell_penalty(self, txt1, pen):
        self.set_font(family=self.font, style='', size=self.textHeight)
        self.cell(w=self.cellWidthLeft, h=self.cellHeight, txt=txt1, align='L', border=True)
        self.set_font(family=self.font, style='B', size=self.textHeight)
        self.cell(w=34.1, h=self.cellHeight, txt=f'{pen:g}', align='C', border='TBR', ln=1)

    def twoPartCell_param(self, txt1, txt2):
        self.set_font(family=self.font, style='', size=self.textHeight)
        self.cell(w=self.cellWidthLeftPart, h=self.cellHeight, txt=txt1, align='L', border=True)
        self.set_font(family=self.font, style='B', size=self.textHeight)
        self.cell(w=self.cellMaxWidth-self.cellWidthLeftPart, h=self.cellHeight, txt=f'{txt2}', align='L', border=True, ln=1)

    def twoPartCell_notes(self, txt1):
        self.set_font(family=self.font, style='', size=self.textHeight)
        self.multi_cell(w=self.cellWidthLeftPart, h=self.cellHeight, txt='Bemerkungen\n \n \n ', align='L', border=True)
        self.set_font(family=self.font, style='B', size=self.textHeight-2)
        x = 20+self.cellWidthLeftPart
        y = self.get_y()-4*self.cellHeight
        self.set_xy(x, y)
        #TODO: ".replace('\n', '')" entfernen
        self.multi_cell(w=self.cellMaxWidth-self.cellWidthLeftPart, h=self.cellHeight, txt=str(txt1).replace(u'\u000A', '\n').replace(r'\n', ''), align='L', border=False)
        self.set_xy(x, y)
        self.cell(w=self.cellMaxWidth-self.cellWidthLeftPart, h=self.cellHeight*4, border=True, ln=1)

    def taskTitle(self, title):
        self.set_font(family=self.font, style='U', size=self.textHeight)
        self.cell(w=0, h=self.cellHeight, txt=f'{title}', align='C', border=True, ln=1)

    def textLine(self, txt1, family, style, align):
        self.set_font(family=family, style=style, size=self.textHeight)
        self.cell(w=0, h=self.cellHeight, txt=f'{txt1}', align=align, border=False, ln=1)

    def grading(self, punkteGesamt, bestehensGrenze):
        self.set_font(family=self.font, style='', size=self.textHeight)
        self.cell(w=self.cellWidthLeft, h=self.cellHeight, txt='Ergebnis', align='L', border='LT')
        self.set_font(family=self.font, style='B', size=self.textHeight)
        self.set_line_width(width=0.2)
        self.cell(w=15.5, h=self.cellHeight, txt=f'{punkteGesamt:g}', align='R', border='LT')
        self.set_font(family=self.font, style='', size=self.textHeight)
        self.cell(w=3.1, h=self.cellHeight, txt='/', align='C', border='T')
        self.cell(w=15.5, h=self.cellHeight, txt='30', align='L', border='TR', ln=1)

        self.set_line_width(width=0.2)
        self.cell(w=self.cellWidthLeft, h=self.cellHeight, txt=f'(Bestehensgrenze: {self.bestehensGrenze} Punkte)', align='L', border='LB')
        self.set_font(family=self.font, style='B', size=self.textHeight-1)
        self.set_line_width(width=0.2)
        if punkteGesamt >= bestehensGrenze:
            self.set_text_color(102,164,99)
            self.cell(w=34.1, h=self.cellHeight, txt=f'BESTANDEN', align='C', border='LBR', ln=1)
        else:
            self.set_text_color(191,70,39)
            self.cell(w=34.1, h=self.cellHeight, txt=f'NICHT BESTANDEN', align='C', border='LBR', ln=1)
        self.set_text_color(0,0,0)
        self.set_line_width(width=0.2)

    def constructPDF(self, df):
        # Add a page
        self.add_page()

        # Title
        self.taskTitle('Bewertung des Testats vom 13.12.21')

        # Id + name
        self.twoPartCell_param('Matrikelnummer', f"{self.data['Matrikelnummer']}")
        self.twoPartCell_param('Name', f"{self.data['Nachname']}, {self.data['Vorname']}")
        self.emptyLine()

        # Task 1
        self.taskTitle('Aufgabe 1: Schattenwurf')
        self.twoPartCell_subTask('Schatteneckpunkte', df['Kriterium 1'], 6)
        self.twoPartCell_subTask('Stamm ausgespart', df['Kriterium 2'], 1)
        self.twoPartCell_subTask('Vielecke zwischen Schatteneckpunkten', df['Kriterium 3'], 4)
        self.twoPartCell_subTask('Vielecke verschneidungsfrei', df['Kriterium 4'], 1)
        self.emptyLine()

        # Task 2
        self.taskTitle('Aufgabe 2: Dreitafelprojektion')
        self.twoPartCell_subTask('Eckpunkte Weihnachtsbaum + Stamm', df['Kriterium 5'], 4.5)
        self.twoPartCell_subTask('Verbindungslinien Stamm + Krone', df['Kriterium 6'], 3)
        self.twoPartCell_subTask('Verbindungslinien zum Wipfel', df['Kriterium 7'], 2.5)
        self.emptyLine()

        # Task 3
        self.taskTitle('Aufgabe 3: Abbildung 3D auf 2D')
        self.twoPartCell_subTask('Eckpunkte Weihnachtsbaum + Stamm', df['Kriterium 8'], 5)
        self.twoPartCell_subTask('Verbindungslinien Stamm + Krone', df['Kriterium 9'], 3)
        self.emptyLine()

        # Penalty
        self.taskTitle('Abzüge')
        self.twoPartCell_penalty('Zahlenwerte an Matrikelnummer nicht korrekt angepasst', df['Abzug 1'])
        self.twoPartCell_penalty('Verspätete Abgabe', df['Abzug 2'])
        self.emptyLine()

        # Grading
        self.grading(self.data['Punkte'], self.bestehensGrenze)

        # Notes
        self.twoPartCell_notes(self.data['Bemerkungen'])