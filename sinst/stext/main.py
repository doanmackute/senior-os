from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QPushButton, QShortcut, QMenu, QAction, QTextEdit, QGraphicsScene, QGraphicsView, QStackedWidget, QLabel, QDialog, QFormLayout, QGroupBox
from PyQt5.QtGui import QFont, QKeySequence, QCursor, QTransform, QTextBlockFormat, QDropEvent, QTextListFormat, QTextCharFormat, QTextCursor, QPixmap, QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDir, Qt, QBuffer, QMimeData, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from saveAsDialog import SaveDialog
import markdown
from xhtml2pdf import pisa
from datetime import datetime
from functools import partial
import sys, re, json, math, os
from bs4 import BeautifulSoup




player = QMediaPlayer()
buff = QBuffer()

def playAudio(filename):
    buff.close()
    with open(filename, "rb") as f:
        data = f.read()
    ba = QtCore.QByteArray(data)
    buff.setData(ba)
    buff.open(QtCore.QIODevice.ReadOnly)
    player.setMedia(QMediaContent(), buff)
    player.play()

class ClickableLabel(QLabel):
    def __init__(self, path, objectName):
        super(QLabel, self).__init__()
        self.openPath = path
        self.name = objectName

        self.setStyleSheet("""
            QWidget:hover {
                background: rgb(180,180,180);
            }

            QWidget {   
                border-top: 2px solid rgb(180,180,180); 
            }
        """)
    
    def mousePressEvent(self, event):
        home.openFileInTextEditor(self.openPath, self.name)


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("homePage.ui", self)
        self.loadingPath = "filesToHomePage.txt"

        self.newFileBtn.clicked.connect(partial(self.openFileInTextEditor, None))
        self.newFileBtn.enterEvent = lambda e: playAudio("AudioTTS/CZ_CreateNewFile.mp3")

        self.lblNameDate.setText("<table width=\"100%\"><td width=\"75%\" align=\"left\"><b>&nbsp;&nbsp;&nbsp;&nbsp;Název souboru:</b></td><td width=\"25%\" align=\"left\"><b>&nbsp;Datum změny:</b></td></table>")

        self.formLayout = QFormLayout()
        self.groupBox = QGroupBox()

        with open(self.loadingPath, "r") as f:
            pathsFromFiles = f.read()

        btnNames = pathsFromFiles.splitlines()

        for i in range(0, len(btnNames), 2):
            currentBtnName = btnNames[i].split("/")
            lblObjectName = "lblFilePath" + str(i)
            self.label = ClickableLabel(btnNames[i], lblObjectName)
            self.label.setText("<table width=\"100%\"><td width=\"78%\" align=\"left\">"+currentBtnName[len(currentBtnName)-1]+ "</td><td width=\"22%\" align=\"left\">"+btnNames[i+1]+"</td></table>")
            self.label.setFont(QFont('Segoe UI', 20))
            self.label.setObjectName(lblObjectName)
            
            self.formLayout.addRow(self.label) #Qt.AlignHCenter|Qt.AlignVCenter
            
            #Create new attribut
            setattr(self, lblObjectName, self.label)
        
        self.groupBox.setLayout(self.formLayout)
        self.scrollArea.setWidget(self.groupBox)

        self.groupBox.setStyleSheet("padding: 20px;")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setSpacing(0)

        closeIcon = QIcon("closeIcon.png")
        self.btnClose.setIcon(closeIcon)
        self.btnClose.setIconSize(QtCore.QSize(55, 55))
    
        self.btnClose.setStyleSheet("QPushButton { border: none; padding: 0px; background-color: transparent;}")
        self.btnClose.enterEvent = lambda e: self.focusCloseBtn()
        self.btnClose.leaveEvent = lambda e: self.btnClose.setIconSize(QtCore.QSize(55, 55))
        self.btnClose.clicked.connect(ui.close)

        #default styleSheet
        with open("defaultStyleSheet.json", "r", encoding="utf8") as f:
            styleSheet = json.load(f)
        
        self.newFileBtn.setStyleSheet("QPushButton { background-color: "+styleSheet["background-color"] + ";} QPushButton:hover { background-color: "+styleSheet["background-color-hover"] + ";}")

    def focusCloseBtn(self):
        self.btnClose.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnClose.setIconSize(QtCore.QSize(58, 58))
        playAudio(f"AudioTTS/CZ_Close.mp3")
    
    def openFileInTextEditor(self, pathValue, objectName):
        if pathValue == None:
            textEditor = Main()
            ui.addWidget(textEditor)
            ui.setCurrentIndex(ui.currentIndex()+1)
        else:
            if os.path.exists(pathValue):
                textEditor = Main()
                ui.addWidget(textEditor)
                textEditor.openCurrentFile(pathValue)
                ui.setCurrentIndex(ui.currentIndex()+1) 
            else:
                #hiding button
                self.widgetToHide = self.findChild(ClickableLabel, objectName)
                self.widgetToHide.hide()

                noFileMessBox = QMessageBox()
                noFileMessBox.setWindowTitle("Soubor nebyl nalezen")
                noFileMessBox.setText("Je nám líto, soubor nelze otevřit, protože nebyl nalezen.")
                noFileMessBox.setIcon(QMessageBox.Warning)
                noFileMessBox.setStandardButtons(QMessageBox.Ok)
                noFileMessBox.exec_()

                #deleting not founded file
                with open(self.loadingPath, "r") as f:
                    lines = f.readlines()
                with open(self.loadingPath, "w") as f:
                    delDateLine = None
                    for x in range(len(lines)):
                        if x == delDateLine:
                            continue
                        elif lines[x].strip("\n") != pathValue:
                            f.write(lines[x])
                        else:
                            delDateLine=x+1
                

class MoreWindows(QStackedWidget):
    def __init__(self):
        super(MoreWindows, self).__init__()
        self.resize(1300, 900)

        #TODO:nefunguje se StackedWidge
    def closeEvent(self, event):
        if self.currentIndex() == 1:
            if self.currentWidget().markdownWithEmptyLines() != self.currentWidget().textEditContent:
                dialog = QMessageBox()
                dialog.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
                dialogFont = QFont()
                dialogFont.setPointSize(22)
                dialog.setFont(dialogFont)
                dialog.setWindowTitle("Textový editor")
                dialog.setText("Chcete uložit soubor?")

                language = self.currentWidget().btnChangeLanguage.text()
                with open("translate.json", "r", encoding="utf8") as f:
                    translate = json.load(f)
                dialog.setWindowTitle(translate[f"stext_{language}_closeDialogTitle"])
                dialog.setText(translate[f"stext_{language}_closeDialogText"])

                dialog.addButton(QPushButton(translate[f"stext_{language}_closeDialogYesRole"]), QMessageBox.YesRole) #value - 0
                dialog.addButton(QPushButton(translate[f"stext_{language}_closeDialogNoRole"]), QMessageBox.NoRole) #value - 1
                dialog.addButton(QPushButton(translate[f"stext_{language}_closeDialogRejectRole"]), QMessageBox.RejectRole) #value - 2

                answer = dialog.exec_()
                self.currentIndex()
                if answer == 0:
                    self.currentWidget().saveFile()
                    event.accept()
                elif answer == 2:
                    event.ignore()
                else:
                    if self.currentWidget().continuosPath != None:
                        if os.path.exists(self.currentWidget().continuosPath):
                            os.remove(self.currentWidget().continuosPath)

class TextEditor(QTextEdit):
    def __init__(self):
        super(QTextEdit, self).__init__()

    def dragEnterEvent(self, event):
        event.accept()
    

    def dropEvent(self, event):
        self.textCursor().beginEditBlock()
        cursor = self.cursorForPosition(event.pos())
        text = event.mimeData().text()

        self.textCursor().removeSelectedText()
        cursor.insertText(text)

        self.formatParagraph = QTextBlockFormat()
        self.formatParagraph.setBottomMargin(18)

        #set the block correctly
        if self.textCursor().block().blockFormat().headingLevel() == 1 and self.textCursor().atBlockStart() and self.textCursor().atBlockEnd():
            self.textCursor().setBlockFormat(self.formatParagraph)

        self.textCursor().endEditBlock()
        event.accept()

        #refresh text cursor
        mimeData = QMimeData()
        mimeData.setText("")
        dummyEvent = QDropEvent(event.posF(), event.possibleActions(),
                mimeData, event.mouseButtons(), event.keyboardModifiers())

        super(TextEditor, self).dropEvent(dummyEvent)

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("main.ui", self)

        #for zooming
        self.factor = 1.2
        self.zoomNum = 0

        self.currentPath = None 
        self.continuosPath = None
        self.setWindowTitle("Nový")
        self.loadingPath = "filesToHomePage.txt"
        self.textEditContent = None

        #to display the Navbar correctly
        self.btnChangeMenu.clicked.connect(self.changeNavbar)
        self.btnChangeMenu.clicked.connect(self.focusTextEdit)
        self.state = 1
        self.format_widget.hide()
        self.edit_widget.hide()
        self.view_widget.hide()

        #MouseOver Audio
        self.mouseOverAudio()


        #setting schedule for saving text files every 60 seconds
        self.checkThreadTimer = QtCore.QTimer(self)
        self.checkThreadTimer.setInterval(120000) #5000 for testing          120000 = 120 seconds
        self.checkThreadTimer.timeout.connect(self.automaticSave)
        self.checkThreadTimer.start()

        #For zooming Text Edit
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.verticalScrollBar().blockSignals(True)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    
        self.textEdit = TextEditor()
        self.textEdit.setFixedWidth(722)
        self.textEdit.setFixedWidth(722)
        self.textEdit.setFont(QFont("Arial", 22))
        self.textEdit.ensureCursorVisible()

        self.textEdit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.textEdit.customContextMenuRequested.connect(self.contextMenu)
        self.blockCount = self.textEdit.document().blockCount()
        self.enterBlock = ""
        self.textEdit.document().blockCountChanged.connect(self.handleBlockCountChanged)
        self.textEdit.setAcceptDrops(True)
        self.textEdit.installEventFilter(self)

        self.view.setScene(self.scene)
        self.scene.addWidget(self.textEdit)
        self.horizontalLayout_6.addWidget(self.view)

        self.styleDocument = """<style>
        p {
            margin-bottom: 18px;
            white-space: pre-wrap;
        }
        h1 {
            margin-bottom: 30px;
            white-space: pre-wrap;
        }
        </style>
        """

        self.btnZoomIn.clicked.connect(self.zoomIn)
        self.btnZoomOut.clicked.connect(self.zoomOut)

        #actions 
        self.boldAction = QAction("Bold")
        self.boldAction.setCheckable(True)    
        self.boldAction.triggered.connect(lambda x: self.textEdit.setFontWeight(QFont.Bold if x else QFont.Normal))

        self.italicAction = QAction()
        self.italicAction.setCheckable(True)
        self.italicAction.toggled.connect(self.textEdit.setFontItalic)
    

        #button connection
        self.btnOpenFile.clicked.connect(self.openFile)
        self.btnNewFile.clicked.connect(self.newFile)
        self.btnSaveFile.clicked.connect(self.saveFile)
        self.btnSaveFileAs.clicked.connect(self.saveFileAs)

        self.btnRedo.clicked.connect(self.textEdit.redo)
        self.btnRedo.clicked.connect(self.focusTextEdit)
        self.btnUndo.clicked.connect(self.textEdit.undo)
        self.btnUndo.clicked.connect(self.focusTextEdit)
        self.btnPaste.clicked.connect(self.textEdit.paste)
        self.btnPaste.clicked.connect(self.focusTextEdit)
        self.btnCopy.clicked.connect(self.textEdit.copy)
        self.btnCopy.clicked.connect(self.focusTextEdit)
        self.btnCut.clicked.connect(self.textEdit.cut)
        self.btnCut.clicked.connect(self.focusTextEdit)

        self.btnUnordered.clicked.connect(partial(self.addList, -1))
        self.btnUnordered.clicked.connect(self.focusTextEdit)
        self.btnOrdered.clicked.connect(partial(self.addList, -4))
        self.btnOrdered.clicked.connect(self.focusTextEdit)
        self.btnPic.clicked.connect(self.insertPicture)
        self.btnPic.clicked.connect(self.focusTextEdit)
        self.btnParagraph.clicked.connect(self.setParagraph)
        self.btnParagraph.clicked.connect(self.focusTextEdit)
        self.btnTitle.clicked.connect(self.setHeader)
        self.btnTitle.clicked.connect(self.focusTextEdit)

        self.btnBold.setCheckable(True)
        self.btnBold.clicked.connect(lambda x: self.textEdit.setFontWeight(QFont.Bold if x else QFont.Normal))
        self.btnBold.clicked.connect(self.focusTextEdit)

        self.btnItalics.setCheckable(True)
        self.btnItalics.clicked.connect(self.textEdit.setFontItalic)
        self.btnItalics.clicked.connect(self.focusTextEdit)

        self.btnSetFontSize18.clicked.connect(partial(self.changeFontSize, 18))
        self.btnSetFontSize22.clicked.connect(partial(self.changeFontSize, 22))
        self.btnSetFontSize28.clicked.connect(partial(self.changeFontSize, 28))
        self.btnChangeLanguage.clicked.connect(self.changeLanguage)

        closeIcon = QIcon('closeIcon.png')
        self.btnClose.setIcon(closeIcon)
        self.btnClose.setIconSize(QtCore.QSize(55, 55))
    
        self.btnClose.setStyleSheet("QPushButton { border: none; padding: 0px; background-color: transparent;}")
        self.btnClose.enterEvent = lambda e: self.focusCloseBtn()
        self.btnClose.leaveEvent = lambda e: self.btnClose.setIconSize(QtCore.QSize(55, 55))
        self.btnClose.clicked.connect(ui.close)

        #setting shortcuts
        self.shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.shortcut.activated.connect(self.openFile)
        self.shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        self.shortcut.activated.connect(self.newFile)
        self.shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut.activated.connect(self.saveFile)
        self.shortcut = QShortcut(QKeySequence("Ctrl+Shift+S"), self)
        self.shortcut.activated.connect(self.saveFileAs)

        self.shortcut = QShortcut(QKeySequence("Ctrl+++"), self)  
        self.shortcut.activated.connect(self.zoomIn)
        self.shortcut = QShortcut(QKeySequence("Ctrl+-"), self)  
        self.shortcut.activated.connect(self.zoomOut)

        self.shortcut = QShortcut(QKeySequence("Ctrl+I"), self)  
        self.shortcut.activated.connect(self.italicAction.trigger)
        self.shortcut = QShortcut(QKeySequence("Ctrl+B"), self)
        self.shortcut.activated.connect(self.boldAction.trigger)
        self.shortcut = QShortcut(QKeySequence("Ctrl+M"), self)  
        self.shortcut.activated.connect(lambda: print(self.textEdit.toMarkdown()))
        self.shortcut.activated.connect(self.markdownWithEmptyLines)
        self.shortcut = QShortcut(QKeySequence("Ctrl+H"), self)  
        self.shortcut.activated.connect(self.setHeader)
        self.shortcut = QShortcut(QKeySequence("Ctrl+P"), self)  
        self.shortcut.activated.connect(self.setParagraph)
        self.shortcut = QShortcut(QKeySequence("Ctrl+D"), self)  
        self.shortcut.activated.connect(self.insertPicture)

        #This fixed issue with redo in context menu
        self.shortcut = QShortcut(QKeySequence("Ctrl+Y"), self)  
        self.shortcut.activated.connect(self.textEdit.redo)

        self.zoomIn()
        self.zoomIn()
        self.zoomIn()

        self.resizeScene()

        self.formatHeader1 = QTextBlockFormat()
        self.formatHeader1.setHeadingLevel(1)
        self.formatHeader1.setBottomMargin(30)

        self.formatParagraph = QTextBlockFormat()
        self.formatParagraph.setBottomMargin(18)
        self.textEdit.textCursor().setBlockFormat(self.formatParagraph)

        #default styleSheet
        with open("defaultStyleSheet.json", "r", encoding="utf8") as f:
            styleSheet = json.load(f)
        
        self.main_menu_widget.setStyleSheet("QPushButton { background-color: "+styleSheet["background-color"] + ";} QPushButton:hover { background-color: "+styleSheet["background-color-hover"] + ";}")

        #load translate
        with open("translate.json", "r", encoding="utf8") as f:
            self.translate = json.load(f)

    def markdownWithEmptyLines(self):
        cursor = self.textEdit.textCursor() 
        cursor.beginEditBlock()
        emptyLinesChecker = False
        for block in range(self.textEdit.document().blockCount()):
            current_block = self.textEdit.document().findBlockByNumber(block)
            if current_block.length() == 1:
                cursor.setPosition(current_block.position())
                cursor.insertText(" ")
                emptyLinesChecker = True

        lines = self.textEdit.toMarkdown().splitlines()
        for i, line in enumerate(lines):
            if i % 2 == 0 and (re.search(r"^\*\*\s*\*\*$", line) or re.search(r"^\*\s*\*$", line) or re.search(r"^\*\*\*\s*\*\*\*$", line)):
                lines[i] = " "

        result = "\n".join(lines)

        if emptyLinesChecker:
            self.textEdit.undo()
        cursor.endEditBlock()

        return result
        
    def loadWithEmptyLines(self, file):
        with open(file, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if i % 2 == 0 and line.strip() == "":
                lines[i] = "<p> </p>"
            elif i % 2 == 0 and line.strip() == "#":
                lines[i] = "<h1> </h1>"

        result = "\n".join(lines)
        return result

    def loadWithEmptyLinesPDF(self, text):
        lines = text.splitlines()

        for i, line in enumerate(lines):
            if i % 2 == 0 and line.strip() == "":
                lines[i] = "<p><br></p>"
            elif i % 2 == 0 and line.strip() == "#":
                lines[i] = "<h1><br></h1>"

        result = "\n".join(lines)
        return result

    def deleteSpaces(self):
        cursor = self.textEdit.textCursor() 
        cursor.beginEditBlock()
        for block in range(self.textEdit.document().blockCount()):
            current_block = self.textEdit.document().findBlockByNumber(block)
            block_text = current_block.text()
            if block_text.strip() == '':
                cursor.setPosition(current_block.position())
                cursor.deleteChar()
        cursor.endEditBlock()


    def focusCloseBtn(self):
        self.btnClose.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnClose.setIconSize(QtCore.QSize(58, 58))
        playAudio(f"AudioTTS/{self.btnChangeLanguage.text().upper()}_Close.mp3")

    def sizePic(self, markdownText):
        editWidth = self.textEdit.geometry().width()
        htmlText = markdown.markdown(markdownText)
        
        soup = BeautifulSoup(htmlText, "html.parser")

        # Najděte všechny značky <img> v HTML
        imgs = soup.find_all("img")

        # Nastavení šířky každého obrázku na 600
        for img in imgs:
            img["width"] = editWidth - 40

        return str(soup)

    def addList(self, style):
        cursor = self.textEdit.textCursor()
        cursor.beginEditBlock()
        
        
        if cursor.block().blockFormat().headingLevel() == 1:
            cursor.setBlockFormat(self.formatParagraph)

            paragraphCharFormat = QTextCharFormat()
            paragraphCharFormat.setFontPointSize(self.textEdit.font().pointSize())
            paragraphCharFormat.setFontWeight(QFont.Normal)

            cursor.select(QTextCursor.LineUnderCursor)
            cursor.setCharFormat(paragraphCharFormat)
            
        blockFmt = cursor.blockFormat()

        listFmt = QTextListFormat()

        if cursor.currentList():
            listFmt = cursor.currentList().format()
        else:
            #cursor.setCharFormat(charFmt)
            listFmt.setIndent(1)
            blockFmt.setIndent(1)

            #blockFmt.setIndent(0)
            cursor.setBlockFormat(blockFmt)

        listFmt.setStyle(style)
        cursor.createList(listFmt)
        cursor.endEditBlock()
        

    def insertPicture(self):
        # Získání cesty k souboru
        filePath, _ = QFileDialog.getOpenFileName(self, self.translate[f"stext_{self.btnChangeLanguage.text()}_insertPictureDialogTitle"], 
            QDir().homePath(), self.translate[f"stext_{self.btnChangeLanguage.text()}_insertPictureDialogFiles"] +" (*.png *.PNG *.jpg *.JPG *.jpeg *.gif)", options=QFileDialog.DontUseNativeDialog)

        if filePath:
            # Načtení fotky z disku
            pixmap = QPixmap(filePath)

            # Nastavení maximální šířky labelu odpovídající šířce QTextEdit
            maxWidth = int(self.textEdit.width() - self.textEdit.document().documentMargin() * 2) - 40
            pixmap = pixmap.scaledToWidth(maxWidth, Qt.SmoothTransformation)

            # Vložení obrázku do QTextEdit
            cursor = self.textEdit.textCursor()

            cursor.beginEditBlock()

            if cursor.hasSelection():
                cursor.removeSelectedText()

            if (not cursor.atBlockEnd() and not cursor.atBlockStart()) or (cursor.atBlockEnd() and not cursor.atStart()):
                cursor.insertText('\n')

            cursor.insertHtml(f'<img src="{QUrl.fromLocalFile(filePath).toString()}" width="{pixmap.width()}" height="{pixmap.height()}">')
            cursor.insertText('\n')  

            cursor.endEditBlock()     


    def setParagraph(self):
        cursor = self.textEdit.textCursor()
        cursor.beginEditBlock()
        if cursor.block().blockFormat().headingLevel() == 1:
            cursor.select(QTextCursor.LineUnderCursor)
        elif not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)

        paragraphCharFormat = QTextCharFormat()
        paragraphCharFormat.setFontPointSize(self.textEdit.font().pointSize())
        paragraphCharFormat.setFontWeight(QFont.Normal)
        
        cursor.setBlockFormat(self.formatParagraph)
        cursor.setCharFormat(paragraphCharFormat)
        cursor.endEditBlock()

    def setHeader(self):
        cursor = self.textEdit.textCursor()
        if cursor.blockFormat().headingLevel() != 1:
            cursor.beginEditBlock()

            # Get selected text or current line
            if not cursor.hasSelection():
                cursor.select(cursor.LineUnderCursor)
            text = cursor.selectedText().strip()
            formattedText = f"<h1>{text}</h1><p></p>"

            selectionAtStart = cursor.selectionStart() == cursor.block().position()
            selectionAtEnd = cursor.selectionEnd() == cursor.block().position() + cursor.block().length() - 1

            # Replace text with formatted text
            if not selectionAtEnd and not selectionAtStart:
                if not cursor.atStart() or not cursor.selectionStart() == 0:
                    cursor.insertText("\n")
                cursor.setBlockFormat(self.formatHeader1)
                cursor.insertHtml(formattedText)
                cursor.insertText("\n")
                cursor.setBlockFormat(self.formatParagraph)
            elif selectionAtEnd and not selectionAtStart:
                cursor.insertText("\n")
                cursor.setBlockFormat(self.formatHeader1)
                cursor.insertHtml(formattedText)
                cursor.setPosition(cursor.NextBlock)
                cursor.setBlockFormat(self.formatParagraph)
            else:
                cursor.setBlockFormat(self.formatHeader1)
                cursor.insertHtml(formattedText)
                cursor.setBlockFormat(self.formatParagraph)

            cursor.endEditBlock()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.textEdit:
            if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
                cursor = self.textEdit.textCursor()
                block = cursor.block()
                format = block.blockFormat()
                if cursor.positionInBlock() == 0: #format.headingLevel() == 1
                    
                    #print("Deleted block content: {}".format(block.text()))
                    previusBlock = cursor.block().previous()
                    if previusBlock.isValid():
                        cursor.beginEditBlock()
                        previousCharFormat = previusBlock.charFormat()
                        #ochrana při undo()

                        if previusBlock.blockFormat().headingLevel() == 1:
                            previousCharFormat.setFontWeight(QFont.Bold)
                            previousCharFormat.setFontPointSize(self.textEdit.font().pointSize()*2)
                        # apply char format to all text in the deleted block
                        cursor.movePosition(cursor.EndOfBlock)
                        cursor.movePosition(cursor.StartOfBlock, cursor.KeepAnchor)
                        
                        cursor.setBlockFormat(self.formatParagraph)
                        cursor.setCharFormat(previousCharFormat)
                        cursor.endEditBlock()
            elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                cursor = self.textEdit.textCursor()
                block = cursor.block()
                if cursor.atBlockStart() and block.blockFormat().headingLevel() == 1:
                    self.enterBlock = True
                    cursor.setBlockFormat(self.formatParagraph)

        return super().eventFilter(obj, event)
    
    def handleBlockCountChanged(self, newBlockCount):
        if newBlockCount > self.blockCount:
            # Najdeme blok, který byl smazán
            if self.enterBlock == True:
                cursor = self.textEdit.textCursor()
                
                cursor.beginEditBlock()
                previusBlockPositon = cursor.block().previous().position()
                cursor.setBlockFormat(self.formatHeader1)
                cursor.setPosition(previusBlockPositon)
                cursor.insertText(" ")
                cursor.select(QTextCursor.BlockUnderCursor)
                cursor.setCharFormat(QTextCharFormat())
                cursor.endEditBlock()

                self.enterBlock = False
        
        self.blockCount = newBlockCount

    def focusTextEdit(self):
        self.textEdit.setFocus()
        self.view.setFocus()

    def contextMenu(self):
        menu = QMenu(self)
        menu.setFont(QFont("Segoe UI", 17))

        redo = QAction("Znovu", self)
        redo.triggered.connect(self.textEdit.redo)
        redo.setShortcut(QKeySequence("Ctrl+Y"))

        undo = QAction("Zpět", self)
        undo.triggered.connect(self.textEdit.undo)
        undo.setShortcut(QKeySequence("Ctrl+Z"))

        cut = QAction("Výjmout", self)
        cut.triggered.connect(self.textEdit.cut)
        cut.setShortcut(QKeySequence("Ctrl+X"))

        copy = QAction("Kopírovat", self)
        copy.triggered.connect(self.textEdit.copy)
        copy.setShortcut(QKeySequence("Ctrl+C"))

        paste = QAction("Vložit", self)
        paste.triggered.connect(self.textEdit.paste)
        paste.setShortcut(QKeySequence("Ctrl+V"))

        selectAll = QAction("Označit vše", self)
        selectAll.triggered.connect(self.textEdit.selectAll)
        selectAll.setShortcut(QKeySequence("Ctrl+A"))
        
        menu.addAction(undo)
        menu.addAction(redo)
        menu.addSeparator()
        menu.addAction(cut)
        menu.addAction(copy)
        menu.addAction(paste)
        menu.addAction(selectAll)

        menu.exec_(QCursor.pos())

    def mouseOverAudio(self):
        with open("audioTTS.json", "r", encoding="utf8") as f:
            audio = json.load(f)

        self.btnChangeMenu.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnChangeMenuTTS"])
        self.btnOpenFile.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnOpenFileTTS"])
        self.btnNewFile.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnNewFileTTS"])
        self.btnSaveFile.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnSaveFileTTS"])
        self.btnSaveFileAs.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnSaveFileAsTTS"])
        self.btnRedo.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnRedoTTS"])
        self.btnUndo.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnUndoTTS"])
        self.btnPaste.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnPasteTTS"])
        self.btnCopy.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnCopyTTS"])
        self.btnCut.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnCutTTS"])
        self.btnZoomIn.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnZoomInTTS"])
        self.btnZoomOut.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnZoomOutTTS"])
        self.lblLanguage.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_lblLanguageTTS"])
        self.btnBold.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnBoldTTS"])
        self.btnItalics.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnItalicsTTS"])
        self.btnTitle.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnTitleTTS"])
        self.btnPic.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnPicTTS"])
        self.btnParagraph.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnParagraphTTS"])
        self.btnOrdered.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnOrderedTTS"])
        self.btnUnordered.enterEvent = lambda e: playAudio(audio[f"stext_{self.btnChangeLanguage.text()}_btnUnorderedTTS"])



    def resizeScene(self):
        #self.view.fitInView(self.scene.sceneRect())
        if self.zoomNum > 0:
            self.textEdit.setFixedHeight(int(self.view.frameGeometry().height()/math.pow(1.2, self.zoomNum)))
        elif self.zoomNum < 0:
            self.textEdit.setFixedHeight(int(self.view.frameGeometry().height()*math.pow(1.2, abs(self.zoomNum))))
        else:
            self.textEdit.setFixedHeight(int(self.view.frameGeometry().height()))

    def resizeEvent(self, event):
        self.resizeScene()

    def showEvent(self, event):
        self.resizeScene()

    def changeNavbar(self):
        if self.state == 1:
            self.file_widget.hide()
            self.format_widget.show()
            self.edit_widget.hide()
            self.view_widget.hide()
            self.state=2
        elif self.state == 2:
            self.file_widget.hide()
            self.format_widget.hide()
            self.edit_widget.show()
            self.view_widget.hide()
            self.state = 3
        elif self.state == 3:
            self.file_widget.hide()
            self.format_widget.hide()
            self.edit_widget.hide()
            self.view_widget.show()
            self.state = 0
        else:
            self.file_widget.show()
            self.format_widget.hide()
            self.edit_widget.hide()
            self.view_widget.hide()
            self.state=1
    
    def openCurrentFile(self, pathBtn):
        self.textEdit.setHtml(self.styleDocument + self.sizePic(self.loadWithEmptyLines(pathBtn)))
        self.textEditContent = self.markdownWithEmptyLines()
        self.setWindowTitle(pathBtn)
        self.currentPath = pathBtn
        self.deleteSpaces()
        self.textEdit.document().clearUndoRedoStacks()

    @QtCore.pyqtSlot()
    def zoomIn(self):
        if self.zoomNum < 5:
            scaleTr = QTransform()
            scaleTr.scale(self.factor, self.factor)

            tr = self.view.transform() * scaleTr
            self.view.setTransform(tr)

            self.textEdit.setFixedHeight(round(self.textEdit.frameGeometry().height()/1.2))
            self.scaleStabilization()

            self.zoomNum = self.zoomNum + 1

    @QtCore.pyqtSlot()
    def zoomOut(self):
        if self.zoomNum > - 3:
            scaleTr = QTransform()
            scaleTr.scale(self.factor, self.factor)

            scaleInverted, invertible = scaleTr.inverted()

            if invertible:
                tr = self.view.transform() * scaleInverted
                self.view.setTransform(tr)

            self.textEdit.setFixedHeight(round(self.textEdit.frameGeometry().height()*1.2))
            self.scaleStabilization()
            
            self.zoomNum = self.zoomNum - 1
    
    def scaleStabilization(self):
        self.view.verticalScrollBar().blockSignals(False)
        self.view.verticalScrollBar().setValue(0) 
        self.view.verticalScrollBar().blockSignals(True)

    def newFile(self):
        self.setWindowTitle("Nový")
        self.currentPath = None

        cursor = self.textEdit.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())
        self.textEdit.clear()
        self.textEdit.textCursor().setBlockFormat(self.formatParagraph)
    
    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, self.translate[f"stext_{self.btnChangeLanguage.text()}_openFileDialogTitle"], QDir().homePath(), 
            (self.translate[f"stext_{self.btnChangeLanguage.text()}_openFileDialogTextFiles"]+" (*.txt *.md);; "+self.translate[f"stext_{self.btnChangeLanguage.text()}_openFileDialogAllFiles"]+" (*.*)"), 
            options=QFileDialog.DontUseNativeDialog)
        if fname[0] != "":
            self.textEdit.setHtml(self.styleDocument + self.sizePic(self.loadWithEmptyLines(fname[0])))
            self.textEditContent = self.markdownWithEmptyLines()
            self.setWindowTitle(fname[0])
            self.currentPath = fname[0]
            self.deleteSpaces()
            self.textEdit.document().clearUndoRedoStacks()

    def saveFile(self):
        if self.currentPath != None:
            self.saveFileTXT(self.currentPath)
            self.saveFilePDF(self.currentPath)
        else:
            self.saveFileAs()
    
    def changeFontSize(self, fontSize):
        self.textEdit.setFont(QFont("Arial", fontSize))
        self.lblFontSizeStat.setText(str(fontSize)+ "pt")


    def saveFileAs(self):
        dlg = SaveDialog(self.btnChangeLanguage.text())
        dlg.exec_()
        fileName = dlg.getResults()

        if fileName != None:
            pathName = QDir().homePath() + "/" + fileName + ".txt"
            self.currentPath = pathName
            self.saveFileTXT(pathName)
            self.saveLastFileName()
            self.setWindowTitle(pathName)
            if self.continuosPath != None:
                if os.path.exists(self.continuosPath):
                    os.remove(self.continuosPath)
            self.continuosPath = None

            self.saveFilePDF(pathName)


    def saveFileTXT(self, filepath):
        self.textEditContent = self.markdownWithEmptyLines()
        with open(filepath, "w") as f:
            f.write(self.textEditContent)
        


    def saveFilePDF(self, pathName):
        style = '''<!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <style type = "text/css">
        @font-face {
            font-family: Arial;
            src: url("Fonts/ARIAL.TTF");
        }

        @font-face {
            font-family: Arial;
            src: url("Fonts/ArialBold.ttf");
            font-weight: bold;
        }

        @font-face {
            font-family: Arial;
            src: url("Fonts/ArialItalic.ttf");
            font-style: italic;
        }

        @font-face {
            font-family: Arial;
            src: url("Fonts/ArialBoldItalic.ttf");
            font-weight: bold;
            font-style: italic;
        }

        body {
            font-family: Arial;
            font-size: '''+str(self.textEdit.font().pointSize())+'''pt;
        }        
                
        p {
            margin-bottom: 18px;
            margin-top: 12px;
            white-space: pre-wrap;
        }               

        h1 {
            font-size: '''+str(self.textEdit.font().pointSize()*2)+'''pt;
            margin-bottom: 30px;
            margin-top: 18px;
            white-space: pre-wrap;
        }
        </style>
        </head>'''
                
        markdownText = self.markdownWithEmptyLines().replace("file://", "")
        markdownCorrectly = self.loadWithEmptyLinesPDF(markdownText)
        htmlText = style + "\n<body>\n" + markdown.markdown(markdownCorrectly) + "\n</body>\n</html>"
        pathNamePDF = os.path.splitext(pathName)[0] + ".pdf"

        pisa_status = self.convert_html_to_pdf(htmlText, pathNamePDF)



    def convert_html_to_pdf(self, source_html, output_filename):
        # open output file for writing (truncated binary)
        result_file = open(output_filename, "w+b")

        # convert HTML to PDF
        pisa_status = pisa.CreatePDF(
                source_html,                # the HTML to convert
                dest=result_file,
                encoding="UTF-8")           # file handle to recieve result

        # close output file
        result_file.close()                 # close output file

        # return False on success and True on errors
        return pisa_status.err

    def automaticSave(self):
        if self.currentPath == None:
            if self.continuosPath != None:
                with open(self.continuosPath, "w") as f:
                    f.write(self.markdownWithEmptyLines())
            else:
                now = datetime.now()
                # dd/mm/YY H:M:S
                dtString = now.strftime("%H_%M__%d_%m_%Y")
                self.continuosPath = QDir().homePath() +"/file_" + dtString + ".txt"
        else:
            self.saveFileTXT(self.currentPath)

    def saveLastFileName(self):
        now = datetime.now()
        # dd/mm/YY H:M:S
        dtString = now.strftime("%H:%M %d.%m.%Y")
        firstLine = self.currentPath + "\n" + dtString + "\n"

        with open(self.loadingPath, "r") as f:
            lines = f.readlines()
        with open(self.loadingPath, "w") as f:
            delDateLine = None
            for x in range(len(lines)+1):
                if x == 0:
                    f.write(firstLine)
                elif x == delDateLine:
                    continue
                elif lines[x-1].strip("\n") != self.currentPath:
                    f.write(lines[x-1])
                else:
                    delDateLine=x+1
    
    def changeLanguage(self):
        if self.btnChangeLanguage.text() == "cz":
            self.btnChangeLanguage.setText("en")
        else:
            self.btnChangeLanguage.setText("cz")

        self.btnOpenFile.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnOpenFile"])
        self.btnNewFile.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnNewFile"])
        self.btnSaveFile.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnSaveFile"])
        self.btnSaveFileAs.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnSaveFileAs"])
        self.btnUndo.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnUndo"])
        self.btnRedo.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnRedo"])
        self.btnPaste.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnPaste"])
        self.btnCopy.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnCopy"])
        self.btnCut.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnCut"])
        self.lblLanguage.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_lblLanguage"])
        self.lblPaperSize.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_lblPaperSize"])
        self.btnChangeMenu.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnChangeMenu"])
        self.btnZoomIn.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnZoomIn"])
        self.btnZoomOut.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnZoomOut"])
        self.btnBold.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnBold"])
        self.btnItalics.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnItalics"])
        self.btnPic.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnPic"])
        self.btnTitle.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnTitle"])
        self.btnParagraph.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnParagraph"])
        self.btnOrdered.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnOrdered"])
        self.btnUnordered.setText(self.translate[f"stext_{self.btnChangeLanguage.text()}_btnUnordered"])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MoreWindows()
    home = WelcomeScreen()
    ui.addWidget(home)
    ui.setCurrentWidget(home)
    #ui.setWindowFlags(ui.windowFlags() & ~Qt.WindowMinimizeButtonHint) # |Qt.Tool
    #ui.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)

    #ui.showMaximized()
    ui.showFullScreen()
    app.exec_()
