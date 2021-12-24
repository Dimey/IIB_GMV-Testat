import datetime
from fpdf import FPDF

class TestatPDF2(FPDF):
    def __init__(self, df):
        super().__init__('P','mm')
        self.data = df

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

        self.set_left_margin(20)
        self.set_right_margin(20)
        self.set_top_margin(20)
        self.constructPDF(df)

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

    def twoPartCell_subTask(self, txt1, pt1, pt2):
        self.set_font(family=self.font, style='', size=self.textHeight)
        self.cell(w=self.cellWidthLeft, h=self.cellHeight, txt=txt1, align='L', border=True)
        self.set_font(family=self.font, style='B', size=self.textHeight)
        self.cell(w=15.5, h=self.cellHeight, txt=f'{pt1}', align='R', border='TB')
        self.set_font(family=self.font, style='', size=self.textHeight)
        self.cell(w=3.1, h=self.cellHeight, txt='/', align='C', border='TB')
        self.cell(w=15.5, h=self.cellHeight, txt=f'{pt2}', align='L', border='TBR', ln=1)

    def twoPartCell_penalty(self, txt1, pen):
        self.set_font(family=self.font, style='', size=self.textHeight)
        self.cell(w=self.cellWidthLeft, h=self.cellHeight, txt=txt1, align='L', border=True)
        self.set_font(family=self.font, style='B', size=self.textHeight)
        self.cell(w=34.1, h=self.cellHeight, txt=f'{pen}', align='C', border='TBL')

    def taskTitle(self, title):
        self.set_font(family=self.font, style='U', size=self.textHeight)
        self.cell(w=0, h=self.cellHeight, txt=f'{title}', align='C', border=True, ln=1)

    def constructPDF(self, df):
        # Add a page
        self.add_page()

        self.taskTitle('Schattenwurf', 1)
        self.twoPartCell_subTask('Schatteneckpunkte', 4.875, 2.5)