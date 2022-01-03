from PyQt5.QtWidgets import QWidget, QLabel, QProgressBar, QVBoxLayout
from PyQt5 import QtCore

class LadeView(QWidget):
    def __init__(self, title):
        super(LadeView, self).__init__()
        self.setWindowTitle(title)
        self.progressBar = QProgressBar(self)
        self.progressLabel = QLabel(self)
        self.progressBar.setValue(0)
        self.progressLabel.setText('Test-String')
        self.resize(300,100)
        self.vBox = QVBoxLayout()
        self.vBox.addWidget(self.progressBar)
        self.vBox.addWidget(self.progressLabel, alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.vBox)
        self.show()

    def updateProgressInfo(self, progressValue, progressText=''):
        self.progressBar.setValue(progressValue)
        self.progressLabel.setText(progressText)
        if progressValue == 100:
            self.close()
        