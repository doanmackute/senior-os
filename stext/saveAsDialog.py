from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QPushButton, QInputDialog, QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import QBuffer, QByteArray, QIODevice, Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

import json
import sys

from requests import options

class SaveDialog(QDialog):
    def __init__(self, language="cz"):
        super(SaveDialog, self).__init__()
        self.btnLanguage = language
        # Load the dialog's GUI
        loadUi("saveAs.ui", self)
        self.setFixedSize(570, 255)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)

        self.widget_4.hide()
        self.btnSave.clicked.connect(self.getResults)
        self.btnCancel.clicked.connect(self.close)

        self.player = QMediaPlayer()
        self.buff = QBuffer()

        with open("translate.json", "r") as f:
            translate = json.load(f)
        
        if self.btnLanguage == "en":
            self.lblFileName.setText(translate["stext_en_lblFileName"])
            self.btnSave.setText(translate["stext_en_btnSave"])
            self.btnCancel.setText(translate["stext_en_btnCancel"])
            self.windowTitle("Save as")

        with open("audioTTS.json", "r") as f:
            audio = json.load(f)
        self.lineEdit.enterEvent = lambda e: self.playAudio(audio[f"stext_{self.btnLanguage}_lblFileNameTTS"])
        self.btnSave.enterEvent = lambda e: self.playAudio(audio[f"stext_{self.btnLanguage}_btnSaveTTS"])
        self.btnCancel.enterEvent = lambda e: self.playAudio(audio[f"stext_{self.btnLanguage}_btnCancelTTS"])

    def getResults(self):
        illegalCharacters = ["<", ">", ":", "\"", "\\", "/", "|", "?", "*", ".", ";"]
        match = [x for x in illegalCharacters if x in self.lineEdit.text()]
        if self.lineEdit.text() != "":
            if not match:
                text = self.lineEdit.text()
                self.close()
                return text
            else:
                self.widget_4.show()
                if self.btnLanguage == "cz":
                    textOflbl = "V názvu souboru se nemůže nacházet znak: "
                else:
                    textOflbl = "The file name cannot contain the character: "

                for i in range(0, len(match)):
                    textOflbl = textOflbl + match[i] + " "
                self.lblError.setText(textOflbl)
        else:
            self.widget_4.show()
            if self.btnLanguage == "cz":
                self.lblError.setText("Zadejte prosím jméno souboru")
            else:
                self.lblError.setText("Please enter a file name") 
    
    def playAudio(self, filename):
        self.buff.close()
        with open(filename, "rb") as f:
            data = f.read()
        ba = QByteArray(data)
        self.buff.setData(ba)
        self.buff.open(QIODevice.ReadOnly)
        self.player.setMedia(QMediaContent(), self.buff)
        self.player.play()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = SaveDialog()
    ui.show()
    app.exec_()