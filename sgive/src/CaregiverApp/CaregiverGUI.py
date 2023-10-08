from tkinter import *
import configurationActions as ryuconf
from screeninfo import get_monitors
from configurationActions import readFile
from getmac import get_mac_address as gmac
import logging

logger = logging.getLogger(__file__)
logger.info("initiated logging")


def resolutionMath():
    screenWidth = get_monitors()[readFile("resolution_info", "numOfScreen")].width
    screenHeight = get_monitors()[readFile("resolution_info", "numOfScreen")].height
    return screenWidth, screenHeight


def getMac():
    mac = gmac()
    print(mac)
    return mac

class menuBarButtons:
    def __init__(self, menuFrame: Frame, root: Tk, heightDivisor: int):
        self.root = root
        self.menuFrame = menuFrame
        self.heightDivisor = heightDivisor
        self.xValue = 0
        self.options = ["GLOBAL", "MAIL", "WEB", "LOGS"]
        self.optionsCounter = 0
        self.buttonDictionary = {}
        # calls section
        self.callOPT = optFrame(self.root)  # call class for loweFrame
        self.buttons()

    def buttons(self):
        self.options.append("EXIT")  # add exit as a last button
        for i in self.options:
            def getButtonNum(x=self.optionsCounter, y=i):
                print(f"num:{x}, name: {y}")  # placeholder
                sortButtonsCommand(x, y)

            self.buttonDictionary[self.optionsCounter] = Button(self.menuFrame)
            self.buttonDictionary[self.optionsCounter]['text'] = i
            self.buttonDictionary[self.optionsCounter]['bg'] = '#696969'
            self.buttonDictionary[self.optionsCounter]['fg'] = 'white'
            self.buttonDictionary[self.optionsCounter]['activebackground'] = '#373737'
            self.buttonDictionary[self.optionsCounter]['activeforeground'] = 'white'
            self.buttonDictionary[self.optionsCounter]['relief'] = 'solid'
            self.buttonDictionary[self.optionsCounter]['command'] = getButtonNum
            self.buttonDictionary[self.optionsCounter]['font'] = "Helvetica 36 bold"
            if self.optionsCounter == 0:
                self.buttonDictionary[self.optionsCounter].place(x=0, y=0, width=resolutionMath()[0] / len(self.options),
                                                                 height=resolutionMath()[1] / self.heightDivisor)
            else:
                self.xValue = self.xValue + int(resolutionMath()[0] / len(self.options))
                self.buttonDictionary[self.optionsCounter].place(x=self.xValue, y=0,
                                                                 width=resolutionMath()[0] / len(self.options),
                                                                 height=resolutionMath()[1] / self.heightDivisor)
            self.optionsCounter += 1
        logger.info("created buttons")

        def sortButtonsCommand(x, y):
            if y == 'LOGS':
                self.callOPT.viewLogs(x)
            elif y == 'GLOBAL':
                self.callOPT.globalConfig(x)
            elif y == 'MAIL':
                self.callOPT.mailConfig(x)
            elif y == 'WEB':
                self.callOPT.webConfig(x)
            elif y == 'EXIT':
                logger.info("exiting application. (bye)")
                exit(0)


class optFrame:
    def __init__(self, root):
        self.root = root
        self.heightDivisor = 7
        self.numberOfFrames = 5
        self.valueI = 0
        self.whichFrameIsON = None
        self.langaugeOPT = ('Czech', 'English', 'Deutsch')
        self.frameDict = {}
        self.createFrame()

    def createFrame(self):
        while self.valueI <= self.numberOfFrames:
            self.frameDict[self.valueI] = Frame(self.root)
            self.frameDict[self.valueI]['bg'] = "#1e1f22"
            self.frameDict[self.valueI]['width'] = resolutionMath()[0]
            self.frameDict[self.valueI]['height'] = resolutionMath()[1] - (resolutionMath()[1] / self.heightDivisor)
            self.valueI += 1

    def viewLogs(self, x):
        if not self.whichFrameIsON is None and self.whichFrameIsON != x:  # close whatever frame is on AppFrame section
            self.frameDict[self.whichFrameIsON].pack_forget()
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        else:  # just open frame for this option
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        # some setup
        textThing = Text(self.frameDict[x], height=resolutionMath()[1] - (resolutionMath()[1] / 7),
                         width=resolutionMath()[0],
                         bg="gray")
        scroll = Scrollbar(orient=VERTICAL, )
        scroll.config(command=textThing.yview, )
        textThing["yscrollcommand"] = scroll.set
        labelThing = Label(self.frameDict[x], text="LOG")
        labelThing.config(font=("Courier", 14))
        labelThing.pack()
        textThing.pack()
        file = ryuconf.readLog()
        for f in file:
            textThing.insert(END, f)
        textThing.config(state=DISABLED)  # disable editing
        logger.info("opened logs frame")

    def globalConfig(self, x):
        if not self.whichFrameIsON is None and self.whichFrameIsON != x:
            self.frameDict[self.whichFrameIsON].pack_forget()
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        else:
            self.whichFrameIsON = x
            self.frameDict[x].pack()

        var = StringVar(self.frameDict[x])
        var.set(self.langaugeOPT[0])
        option = OptionMenu(self.frameDict[x], var, *self.langaugeOPT)
        option.pack()
        logger.info("opened global config frame")

    def mailConfig(self, x):
        if not self.whichFrameIsON is None and self.whichFrameIsON != x:
            self.frameDict[self.whichFrameIsON].pack_forget()
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        else:
            self.whichFrameIsON = x
            self.frameDict[x].pack()

        logger.info("opened mail config frame")

    def webConfig(self, x):
        if not self.whichFrameIsON is None and self.whichFrameIsON != x:
            self.frameDict[self.whichFrameIsON].pack_forget()
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        else:
            self.whichFrameIsON = x
            self.frameDict[x].pack()
        logger.info("opened web config frame")


class AppBase:
    def __init__(self, root: Tk):
        self.root = root
        self.heightDivisor = 7
        self.rootSetup()  # def for root window
        self.menuBarFrameSetup()  # def for creating menu bar frame

    def rootSetup(self):
        self.root.title("Caregiver Configuration v:0.0.1")
        self.root.attributes('-fullscreen', True)
        self.root.configure(background="#1e1f22")
        logger.info("created root window")

    def menuBarFrameSetup(self):
        masterFrame = Frame(self.root)  # creating menu bar frame (tkinter.Frame)
        masterFrame.pack_propagate(False)
        masterFrame['width'] = resolutionMath()[0]
        masterFrame['height'] = resolutionMath()[1] / self.heightDivisor
        masterFrame['bg'] = '#232323'
        masterFrame.pack(side=TOP)
        logger.info("created menuFrame")
        # call class for creating objects
        menuBarButtons(masterFrame, self.root, self.heightDivisor)