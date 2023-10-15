from tkinter import *
import configurationActions as ryuconf
from screeninfo import get_monitors
from configurationActions import readJsonConfig
import logging
import re

logger = logging.getLogger(__file__)
logger.info("initiated logging")


class menuBarButtons:
    def __init__(self, menuFrame: Frame, root: Tk, heightDivisor: int, height: int, width: int):
        self.height = height
        self.width = width
        self.root = root
        self.menuFrame = menuFrame
        self.heightDivisor = heightDivisor
        self.xValue = 0
        self.options = ryuconf.readJsonConfig("careConf", "menuButtonsList")
        self.buttonDictionary = {}
        # calls section
        self.buttons()
        self.callOPT = configFrame(self.root, self.width, self.height)
        self.pickedButton = None

    def buttons(self):
        counter = 0
        self.options.append("EXIT")  # add exit as a last button
        for i in self.options:
            def getButtonNum(y=counter):
                if y == 0:
                    self.callOPT.globalConfig(y + 1)
                elif y == 1:
                    self.callOPT.mailConfig(y + 1)
                elif y == 2:
                    self.callOPT.webConfig(y + 1)
                elif y == 3:
                    self.callOPT.viewLogs(y + 1)
                elif y == int(len(self.options) - 1):
                    exit(0)

            self.buttonDictionary[counter] = Button(self.menuFrame)
            self.buttonDictionary[counter]['text'] = i
            self.buttonDictionary[counter]['bg'] = '#C7C6C1'
            self.buttonDictionary[counter]['activebackground'] = '#a8a7a2'
            self.buttonDictionary[counter]['relief'] = 'solid'
            self.buttonDictionary[counter]['command'] = getButtonNum
            self.buttonDictionary[counter]['font'] = "Helvetica 36 bold"
            self.buttonDictionary[counter]['borderwidth'] = 2
            self.buttonDictionary[counter]['highlightbackground'] = "black"

            if counter == 0:
                self.buttonDictionary[counter].place(x=0, y=0, width=self.width / len(self.options),
                                                     height=self.height / self.heightDivisor)
            else:
                self.xValue = self.xValue + int(self.width / len(self.options)) + 5
                self.buttonDictionary[counter].place(x=self.xValue, y=0,
                                                     width=self.width / len(self.options),
                                                     height=self.height / self.heightDivisor)
            counter += 1
        logger.info("created buttons")


class configFrame:
    def __init__(self, root: Tk, width: int, height: int):
        self.width = width
        self.height = height
        self.root = root
        self.heightDivisor = ryuconf.readJsonConfig("careConf","heightDivisor")
        self.numberOfFrames = 4
        self.whichFrameIsON = None
        self.configFrameHeight = self.height - (self.height / self.heightDivisor)
        self.frameDict = {}
        self.createFrame()
        self._isGlobalConfigRunning = False
        self.activeColor = "#5c6447"
        self.normalColor = "#D3D3D3"
        # positions etc. on frame things:
        self.widthLabel = self.width / 2
        self.widthButton = self.width / 10
        self.heightWidgets = (self.height / self.heightDivisor) / 2
        self.Xposition = 0
        self.Yposition = 10
        # change language things:
        self.changeLanguageDict = {}
        self.pickedButton = None
        self.options = ryuconf.readJsonConfig("careConf", "LanguageOptions")
        # change color scheme things:
        self.colorButtonSelected = None
        self.errorLabel = None
        self.delaySubmit = None

    """
        Creating base frame for all of the options: ------------------------------------------------------------------------
        """

    def createFrame(self):
        valueOfI = 1
        while valueOfI <= self.numberOfFrames + 1:
            self.frameDict[valueOfI] = Frame(self.root)
            self.frameDict[valueOfI].pack_propagate(False)
            self.frameDict[valueOfI]['bg'] = "white"
            self.frameDict[valueOfI]['width'] = self.width
            self.frameDict[valueOfI]['height'] = self.configFrameHeight
            valueOfI += 1

    """
    Functions used in defs for each button: ----------------------------------------------------------------------------
    """

    def refreshLogFrame(self, x):  # F5 ON FRAME THAT SHOWS LOGS
        for widgets in self.frameDict[x].winfo_children():
            widgets.destroy()
        self.viewLogs(x)

    def changeColorLanguage(self, idLanButton):  # LANGUAGE SELECTION
        buttonSelectedColor = "#5c6447"
        if not self.pickedButton is None:
            self.changeLanguageDict[self.pickedButton].configure(bg="#D3D3D3", activebackground="#bdbbbb")
            self.changeLanguageDict[idLanButton].configure(bg=buttonSelectedColor, activebackground=buttonSelectedColor)
            self.pickedButton = idLanButton
        else:
            self.changeLanguageDict[idLanButton].configure(bg=buttonSelectedColor, activebackground=buttonSelectedColor)
            self.pickedButton = idLanButton

    def changeColorColorschemeSelection(self, buttonID):  # COLOR SCHEME SELECTION
        buttonSelectedColor = "#5c6447"
        if not self.colorButtonSelected is None:
            self.colorButtonSelected.configure(bg="#D3D3D3", activebackground="#bdbbbb")
            buttonID.configure(bg=buttonSelectedColor, activebackground=buttonSelectedColor)
            self.colorButtonSelected = buttonID
        else:
            buttonID.configure(bg=buttonSelectedColor, activebackground=buttonSelectedColor)
            self.colorButtonSelected = buttonID

    def checkIfInputIsNumber(self, timeInput, xPos, yPos,whichConfig):
        global timeInt
        try:
            timeInt = int(timeInput)
        except ValueError:
            self.delaySubmit.configure(bg=self.normalColor, activebackground=self.normalColor)  # change submit button color barch
            iks = xPos + self.widthButton + 10
            self.errorLabel['text'] = f"'{timeInput}' is not a number, value must be number!"
            errorLabelWidth = self.width - (2*self.widthButton + self.widthLabel + 30)
            self.errorLabel.place(x=iks, y=yPos, width=errorLabelWidth, height=self.heightWidgets)
            logger.error(f"Value '{timeInput}' is not a number, value must be number!")
            return

        self.errorLabel.place_forget()
        self.delaySubmit.configure(bg=self.activeColor, activebackground=self.activeColor)

        if whichConfig == "soundDelay":
            ryuconf.editConfig("GlobalConfiguration", "soundDelay", timeInt)

    def hexCheck(self, hexInput, xPos, yPos):
        if not len(hexInput) == 7:  # hex needs (?) to have 7 characters
            self.colorSubmit.configure(bg=self.normalColor, activebackground=self.normalColor)
            self.errorLabel['text'] = f"'{hexInput}' needs to have 7 characters"
            iks = xPos + self.widthButton + 10
            errorLabelWidth = self.width - (2 * self.widthButton + self.widthLabel + 30)
            self.errorLabel.place(x=iks, y=yPos, width=errorLabelWidth, height=self.heightWidgets)
            return

        match = re.search(r'^#(?:[0-9a-fA-F]{1,2}){3}$', hexInput)  # regex check

        if match:
            self.errorLabel.place_forget()
            ryuconf.editConfig("GlobalConfiguration", "alertColor", hexInput)
            self.colorSubmit.configure(bg=self.activeColor, activebackground=self.activeColor)
        else:
            self.colorSubmit.configure(bg=self.normalColor, activebackground=self.normalColor)
            self.errorLabel['text'] = f"'{hexInput}' is not a HEX value in format '#123456'"
            iks = xPos + self.widthButton + 10
            errorLabelWidth = self.width - (2 * self.widthButton + self.widthLabel + 30)
            self.errorLabel.place(x=iks, y=yPos, width=errorLabelWidth, height=self.heightWidgets)

    def restoreGlobalConfigs(self):  # RESTORES ALL SELECTED BUTTONS
        getWhereConfigIs = ryuconf.readJsonConfig("pathToConfig", "path")
        ryuconf.caregiverAppConfig(getWhereConfigIs)  # generates default config.json
        self.delaySubmit.configure(bg=self.normalColor, activebackground=self.normalColor)
        self.colorSubmit.configure(bg=self.normalColor, activebackground=self.normalColor)
        if not self.pickedButton is None:
            self.changeLanguageDict[self.pickedButton].configure(bg=self.normalColor, activebackground=self.normalColor)
        if not self.colorButtonSelected is None:
            self.colorButtonSelected.configure(bg=self.normalColor, activebackground=self.normalColor)
        else:
            return

    """
    Configuration for each options Frame: ------------------------------------------------------------------------------
    
    LOGS: --------------------------------------------------------------------------------------------------------------
    """

    def viewLogs(self, x):
        if not self.whichFrameIsON is None and self.whichFrameIsON != x:  # close whatever frame is on AppFrame section
            # destroy all widget from frame, if there is any present (for refreshing data values)
            for widgets in self.frameDict[x].winfo_children():
                widgets.destroy()
            self.frameDict[self.whichFrameIsON].pack_forget()
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        else:  # just open frame for this option
            self.whichFrameIsON = x
            self.frameDict[x].pack()

        B = Button(self.frameDict[x], text="REFRESH", command=lambda: self.refreshLogFrame(x))
        B.pack(side=TOP)
        textThing = Text(self.frameDict[x], height=self.height - (self.height / 7),
                         width=self.width,
                         bg="white")
        scroll = Scrollbar(orient=VERTICAL, )
        scroll.config(command=textThing.yview, )
        textThing["yscrollcommand"] = scroll.set
        textThing.pack()
        file = ryuconf.readLog()
        for f in file:
            textThing.insert(END, f)
        textThing.config(state=DISABLED)  # disable editing

    """
    GLOBAL CONFIG: -----------------------------------------------------------------------------------------------------
    """

    def globalConfig(self, x):
        if not self.whichFrameIsON is None and self.whichFrameIsON != x:
            self.frameDict[self.whichFrameIsON].pack_forget()
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        else:
            self.whichFrameIsON = x
            self.frameDict[x].pack()

        if self._isGlobalConfigRunning is True:
            return

        self._isGlobalConfigRunning = True  # "single instance lock"
        # start from x = 0 and y = 30 of the application frame
        self.Xposition = 0
        self.Yposition = 30

        fontGet = (f"{ryuconf.readJsonConfig('GlobalConfiguration', 'fontFamily')} "  # font family
                   f"{ryuconf.readJsonConfig('GlobalConfiguration', 'labelFontSize')} "  # font size
                   f"{ryuconf.readJsonConfig('GlobalConfiguration', 'fontThickness')}")  # font thicc?

        fontInputThing = (f"{ryuconf.readJsonConfig('GlobalConfiguration', 'fontFamily')} "
                          f"{ryuconf.readJsonConfig('GlobalConfiguration', 'fontSize')} "
                          f"{ryuconf.readJsonConfig('GlobalConfiguration', 'fontThickness')}")

        # CHOOSE LANGUAGE SECTION --------------------------------

        languageLabel = Label(self.frameDict[x], text="OS language:")
        languageLabel['font'] = fontGet
        languageLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        self.Xposition = self.Xposition + self.widthLabel + 10

        counterLangCount = 1
        radioVar = StringVar(value=ryuconf.readJsonConfig("GlobalConfiguration", "language"))
        for name in self.options:
            def getName(n=name, c=counterLangCount):
                self.changeColorLanguage(c)
                ryuconf.editConfig("GlobalConfiguration", "language", n)
            self.changeLanguageDict[counterLangCount] = Radiobutton(self.frameDict[x], text=name, variable=radioVar,
                                                                    value=name)
            self.changeLanguageDict[counterLangCount]['font'] = fontGet
            self.changeLanguageDict[counterLangCount].configure(bg="#D3D3D3", activebackground="#bdbbbb")
            self.changeLanguageDict[counterLangCount]['command'] = getName
            if counterLangCount == 1:
                self.changeLanguageDict[counterLangCount].place(x=self.Xposition, y=self.Yposition,
                                                                width=self.widthButton, height=self.heightWidgets)
            else:
                self.Xposition = self.Xposition + self.widthButton + 10
                self.changeLanguageDict[counterLangCount].place(x=self.Xposition, y=self.Yposition,
                                                                width=self.widthButton, height=self.heightWidgets)
            counterLangCount += 1
        logger.info("opened global config frame")

        # CHOOSE COLOR SECTION -------------------------------------

        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + 10

        colorModeLabel = Label(self.frameDict[x], text="System color scheme:")
        colorModeLabel['font'] = fontGet
        colorModeLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        radioVar2 = StringVar(value=ryuconf.readJsonConfig("GlobalConfiguration", "colorMode"))
        print(ryuconf.readJsonConfig("GlobalConfiguration", "colorMode") == "Light")
        # light mode
        whiteColorButton = Radiobutton(self.frameDict[x], text="Light", variable=radioVar2, value="Light")
        whiteColorButton['command'] = lambda: [ryuconf.editConfig("GlobalConfiguration", "colorMode", radioVar2.get()),
                                               self.changeColorColorschemeSelection(whiteColorButton)]
        whiteColorButton['font'] = fontGet
        self.Xposition = self.Xposition + self.widthLabel + 10
        whiteColorButton.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)
        # dark mode
        BlackColorButton = Radiobutton(self.frameDict[x], text="Dark", variable=radioVar2, value="Dark")
        BlackColorButton['command'] = lambda: [ryuconf.editConfig("GlobalConfiguration", "colorMode", radioVar2.get()),
                                               self.changeColorColorschemeSelection(BlackColorButton)]
        BlackColorButton['font'] = fontGet
        self.Xposition = self.Xposition + self.widthButton + 10
        BlackColorButton.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

        # CHOOSE DELAY SECTION --------------------------------------

        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + 10

        soundDelayLabel = Label(self.frameDict[x],
                                text="Alert delay (in seconds):")
        soundDelayLabel['font'] = fontGet
        soundDelayLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        inputText = Text(self.frameDict[x])
        inputText['font'] = fontInputThing
        defalultDelayValue = ryuconf.readJsonConfig("GlobalConfiguration", "soundDelay")
        inputText.insert(1.0, defalultDelayValue)
        self.Xposition = self.Xposition + self.widthLabel + 10
        inputText.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

        self.delaySubmit = Button(self.frameDict[x], text="submit")
        self.delaySubmit['font'] = fontGet
        self.Xposition = self.Xposition + self.widthButton + 10
        self.delaySubmit.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

        getCurrentX = self.Xposition
        getCurrentY = self.Yposition

        self.errorLabel = Label(self.frameDict[x], bg="#D2042D")

        self.delaySubmit['command'] = lambda: self.checkIfInputIsNumber(inputText.get(1.0, 'end-1c'), getCurrentX,
                                                                        getCurrentY, "soundDelay")

        # CHOOSE NOTIFY COLOR SECTION --------------------------------

        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + 10

        colorModeLabel = Label(self.frameDict[x], text="Alert color in hex (#12345): ")
        colorModeLabel['font'] = fontGet
        colorModeLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        inputHex = Text(self.frameDict[x])
        inputHex['font'] = fontInputThing
        defaultHexValue = ryuconf.readJsonConfig("GlobalConfiguration", "alertColor")
        inputHex.insert(1.0, defaultHexValue)
        self.Xposition = self.Xposition + self.widthLabel + 10
        inputHex.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel/3, height=self.heightWidgets)

        self.colorSubmit = Button(self.frameDict[x], text="submit")
        self.colorSubmit['font'] = fontGet
        self.Xposition = self.Xposition + (self.widthLabel/3) + 10
        self.colorSubmit.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

        getCurrentXforHex = self.Xposition
        getCurrentYforHex = self.Yposition

        self.colorSubmit['command'] = lambda : self.hexCheck(inputHex.get(1.0, 'end-1c'), getCurrentXforHex,
                                                             getCurrentYforHex)

        # CHOOSE ALERT LANG SECTION --------------------------------

        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + 10

        alertLangLabel = Label(self.frameDict[x], text="Alert language: ")
        alertLangLabel['font'] = fontGet
        alertLangLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        # CHOOSE FONT SIZE SECTION --------------------------------

        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + 10

        fontSizeLabel = Label(self.frameDict[x], text="Text size: ")
        fontSizeLabel['font'] = fontGet
        fontSizeLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        fontSizeINput = Text(self.frameDict[x])
        fontSizeINput['font'] = fontInputThing

        defaultFontSize = ryuconf.readJsonConfig("GlobalConfiguration", "fontSize")
        fontSizeINput.insert(1.0, "36")
        self.Xposition = self.Xposition + self.widthLabel + 10
        fontSizeINput.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

        self.fontSubmit = Button(self.frameDict[x], text="submit")
        self.fontSubmit['font'] = fontGet
        self.Xposition = self.Xposition + self.widthButton + 10
        self.fontSubmit.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

        getCurrentX = self.Xposition
        getCurrentY = self.Yposition

        self.errorLabel = Label(self.frameDict[x], bg="#D2042D") # error label, when input is wrong

        # CHOOSE FONT FAMILY SECTION -------------------------------

        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + 10

        fontFamilyLabel = Label(self.frameDict[x], text="Font name (Font family): ")
        fontFamilyLabel['font'] = fontGet
        fontFamilyLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        fontFamilyInput = Text(self.frameDict[x])
        fontFamilyInput['font'] = fontInputThing

        defaultFontName = ryuconf.readJsonConfig("GlobalConfiguration", "fontFamily")
        fontFamilyInput.insert(1.0, defaultFontName)
        self.Xposition = self.Xposition + self.widthLabel + 10
        fontFamilyInput.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel/2, height=self.heightWidgets)

        self.familySubmit = Button(self.frameDict[x], text="submit")
        self.familySubmit['font'] = fontGet
        self.Xposition = self.Xposition + self.widthLabel/2 + 10
        self.familySubmit.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

        getCurrentX = self.Xposition
        getCurrentY = self.Yposition

        self.errorLabel = Label(self.frameDict[x], bg="#D2042D")  # error label, when input is wrong

        # FACTORY RESET  ------------------------------------------

        self.Xposition = (self.width / 2) - ((self.width / 5) / 2)
        self.Yposition = self.Yposition + self.heightWidgets + 100
        restore = Button(self.frameDict[x], text="RESTORE TO DEFAULT SETTINGS")
        restore.place(x=self.Xposition, y=self.Yposition, width=self.width / 5, height=self.heightWidgets)
        # behold the worst thing in the code: (eventually I will change this, but for now it works :))
        restore['command'] = lambda: [self.restoreGlobalConfigs(),self.errorLabel.place_forget(),
                                      radioVar.set(ryuconf.readJsonConfig("GlobalConfiguration", "language")),
                                      radioVar2.set(ryuconf.readJsonConfig("GlobalConfiguration", "colorMode")),
                                      inputText.delete("1.0", "end"),
                                      inputText.insert(1.0, ryuconf.readJsonConfig("GlobalConfiguration", "soundDelay")),
                                      inputHex.delete(1.0, "end"),
                                      inputHex.insert(1.0, ryuconf.readJsonConfig("GlobalConfiguration", "alertColor")),
                                      logger.info("resetting config")]
        # restores config to default values and restores also gui visualization

    """
    MAIL CONFIG: -------------------------------------------------------------------------------------------------------
    """

    def mailConfig(self, x):
        if not self.whichFrameIsON is None and self.whichFrameIsON != x:
            self.frameDict[self.whichFrameIsON].pack_forget()
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        else:
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        logger.info("opened mail config frame")

    """
    WEB CONFIG: -------------------------------------------------------------------------------------------------------
    """

    def webConfig(self, x):
        if not self.whichFrameIsON is None and self.whichFrameIsON != x:
            self.frameDict[self.whichFrameIsON].pack_forget()
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        else:
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        logger.info("opened web config frame")

    """
       END OF  CONFIG: -------------------------------------------------------------------------------------------------
       
       -----------------------------------------------------------------------------------------------------------------
    """


class AppBase:
    def __init__(self, root: Tk):
        self.root = root
        self.heightDivisor = 7
        self.screenWidth = get_monitors()[readJsonConfig("GlobalConfiguration", "numOfScreen")].width  # screen width
        self.screenHeight = get_monitors()[readJsonConfig("GlobalConfiguration", "numOfScreen")].height  # screen height
        self.rootSetup()  # def for root window
        self.menuBarFrameSetup()  # def for creating menu bar frame

    def rootSetup(self):
        self.root.title("Caregiver Configuration v:0.0.1")
        self.root.attributes('-fullscreen', True)
        self.root.configure(background="white")
        logger.info("created root window")

    def menuBarFrameSetup(self):
        masterFrame = Frame(self.root)  # creating menu bar frame (tkinter.Frame)
        masterFrame.pack_propagate(False)
        masterFrame['width'] = self.screenWidth
        masterFrame['height'] = self.screenHeight / self.heightDivisor
        masterFrame['bg'] = 'white'
        masterFrame.pack(side=TOP)
        logger.info("created menuFrame")
        # calling class for creating objects
        menuBarButtons(masterFrame, self.root, self.heightDivisor, self.screenHeight, self.screenWidth)
