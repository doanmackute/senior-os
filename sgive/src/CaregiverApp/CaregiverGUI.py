from tkinter import *
import configurationActions as ryuconf
from screeninfo import get_monitors
from configurationActions import readFile
import logging

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
        self.options = ryuconf.testRead("careConf", "menuButtonsList")
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
        self.heightDivisor = 7
        self.numberOfFrames = 4
        self.whichFrameIsON = None
        self.configFrameHeight = self.height - (self.height / self.heightDivisor)
        self.frameDict = {}
        self.createFrame()
        self._isGlobalConfigRunning = False
        # positions etc. on frame things:
        self.widthLabel = self.width / 2.2
        self.widthButton = 200
        self.Xposition = 0
        self.Yposition = 10
        # change language things:
        self.heightWidgets = (self.height / self.heightDivisor) / 2
        self.changeLanguageDict = {}
        self.pickedButton = None
        self.options = ryuconf.testRead("careConf", "LanguageOptions")
        # change color scheme things:
        self.colorButtonSelected = None
        self.errorLabel = None

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

    def getDelayTime(self, time, xPos, yPos):
        global timeInt
        try:
            timeInt = int(time)
            self.errorLabel.place_forget()
            ryuconf.editConfig("GlobalConfiguration", "soundDelay", timeInt)
        except ValueError:
            iks = xPos + self.widthButton + 10
            self.errorLabel.place(x=iks, y=yPos, width=self.width / 6, height=self.heightWidgets)
            logger.error(f"Value '{time}' is not supported for time delay")
            return

    def restoreGlobalConfigs(self):  # RESTORES ALL SELECTED BUTTONS
        ryuconf.caregiverAppConfig()
        if not self.pickedButton is None:
            self.changeLanguageDict[self.pickedButton].configure(bg="#D3D3D3", activebackground="#bdbbbb")
            self.colorButtonSelected.configure(bg="#D3D3D3", activebackground="#bdbbbb")
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

        fontGet = (f"{ryuconf.testRead('GlobalConfiguration', 'fontFamily')} "  # font family
                   f"{ryuconf.testRead('GlobalConfiguration', 'labelFontSize')} "  # font size
                   f"{ryuconf.testRead('GlobalConfiguration', 'fontThickness')}")  # font thicc?

        # CHOOSE LANGUAGE SECTION --------------------------------

        languageLabel = Label(self.frameDict[x], text="Please, choose which language you want this OS to be:")
        languageLabel['font'] = fontGet
        languageLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        self.Xposition = self.Xposition + self.widthLabel + 10

        counterLangCount = 1
        radioVar = IntVar(value=2)  # english
        for name in self.options:
            def getName(n=name):
                self.changeColorLanguage(radioVar.get())
                ryuconf.editConfig("GlobalConfiguration", "language", n)

            self.changeLanguageDict[counterLangCount] = Radiobutton(self.frameDict[x], text=name, variable=radioVar,
                                                                    value=counterLangCount)
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

        colorModeLabel = Label(self.frameDict[x], text="Choose if you want your system to be in white or black:")
        colorModeLabel['font'] = fontGet
        colorModeLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        radioVar2 = StringVar(value="Light")
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
                                text="Choose for how long system needs to wait before playing sound [in s]:")
        soundDelayLabel['font'] = fontGet
        soundDelayLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        inputText = Text(self.frameDict[x])
        inputText['font'] = (f"{ryuconf.testRead('GlobalConfiguration', 'fontFamily')} "
                             f"{ryuconf.testRead('GlobalConfiguration', 'fontSize')} "
                             f"{ryuconf.testRead('GlobalConfiguration', 'fontThickness')}")
        inputText.insert(END, "5")
        self.Xposition = self.Xposition + self.widthLabel + 10
        inputText.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

        delaySubmit = Button(self.frameDict[x], text="submit")
        delaySubmit['font'] = fontGet
        self.Xposition = self.Xposition + self.widthButton + 10
        delaySubmit.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

        getCurrentX = self.Xposition
        getCurrentY = self.Yposition

        self.errorLabel = Label(self.frameDict[x], bg="#D2042D", text="you must enter only number!")

        delaySubmit['command'] = lambda: self.getDelayTime(inputText.get(1.0, 'end-1c'), getCurrentX,
                                                           getCurrentY)

        # CHOOSE NOTIFY COLOR SECTION --------------------------------

        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + 10

        colorModeLabel = Label(self.frameDict[x], text="Pick color you want to have as a notification color: ")
        colorModeLabel['font'] = fontGet
        colorModeLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        # CHOOSE ALERT LANG SECTION --------------------------------

        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + 10

        alertLangLabel = Label(self.frameDict[x], text="Choose your alert language: ")
        alertLangLabel['font'] = fontGet
        alertLangLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        # CHOOSE FONT SIZE SECTION --------------------------------

        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + 10

        fontSizeLabel = Label(self.frameDict[x], text="Set size of the text: ")
        fontSizeLabel['font'] = fontGet
        fontSizeLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        # CHOOSE FONT FAMILY SECTION -------------------------------

        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + 10

        fontFamilyLabel = Label(self.frameDict[x], text="Choose Font for your OS: ")
        fontFamilyLabel['font'] = fontGet
        fontFamilyLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        # FACTORY RESET  ------------------------------------------

        self.Xposition = (self.width / 2) - ((self.width / 5) / 2)
        self.Yposition = self.Yposition + self.heightWidgets + 100
        restore = Button(self.frameDict[x], text="RESTORE TO DEFAULT SETTINGS")
        restore.place(x=self.Xposition, y=self.Yposition, width=self.width / 5, height=self.heightWidgets)
        # behold the worst thing in the code: (eventually I will change this, but for now it works :))
        restore['command'] = lambda: [radioVar.set(2), radioVar2.set("Light"), inputText.delete("1.0", "end"),
                                      self.restoreGlobalConfigs(), logger.info("resetting config"),
                                      self.errorLabel.place_forget(), inputText.insert(END, "5")]
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
        self.screenWidth = get_monitors()[readFile("resolution_info", "numOfScreen")].width  # screen width
        self.screenHeight = get_monitors()[readFile("resolution_info", "numOfScreen")].height  # screen height
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
