import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from gmvtestatmodel import TestatModel


class PDFGenerationThread(QThread):
    _signal = pyqtSignal(int, str)

    def __init__(self, testatModel):
        super(PDFGenerationThread, self).__init__()
        self.testatModel = testatModel

    def run(self):
        self.testatModel.erzeugeOrdner("GMV Testat Tool/Studenten ohne Abgabe")
        df = self.testatModel.bewertungsuebersicht
        matrikelNummern = df[(df["Punkte"] != "")].index
        anzahlPDFs = len(matrikelNummern)
        for idx, matrikelNummer in enumerate(matrikelNummern):
            self.testatModel.exportPDF(matrikelNummer)
            progress = np.ceil((idx + 1) * 100 / anzahlPDFs)
            self._signal.emit(progress, f"{idx+1} von {anzahlPDFs} PDFs erzeugt.")


class BatchImportThread(QThread):
    _progressSignal = pyqtSignal(int, str)
    _setModelSignal = pyqtSignal(TestatModel, int)

    def __init__(self, testatModel, pathsToSubmissions):
        super(BatchImportThread, self).__init__()
        self.testatModel = testatModel
        self.pathsToSubmissions = pathsToSubmissions

    def run(self):
        anzahlAbgaben = len(self.pathsToSubmissions)
        fehlerZaehler = 0
        for idx, pfadZurAbgabe in enumerate(self.pathsToSubmissions):
            if self.testatModel.ladeAbgabe(pfadZurAbgabe) == False:
                fehlerZaehler += 1
            progress = np.ceil((idx + 1) * 100 / anzahlAbgaben)
            self._progressSignal.emit(
                progress, f"{idx+1} von {anzahlAbgaben} Abgaben importiert."
            )
        self._setModelSignal.emit(self.testatModel, fehlerZaehler)
