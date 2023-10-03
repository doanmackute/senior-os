"""
Written by: RYUseless
"""
import tkinter
from tkinter import *
from tkinter import font
import configActions as JS


def getButtonConf():
    # collecting values for font and colors
    bg = JS.jsonRed('colors_info', "buttons_unselected")
    bg_active = JS.jsonRed('colors_info', "buttons_selected")
    # end of collecting values for font and colors
    return bg, bg_active


def resolutionMath(root: tkinter.Tk):
    _screenWidth = root.winfo_screenwidth()
    _screenHeight = root.winfo_screenheight()

    screen_res = f"{_screenWidth}x{_screenHeight}"

    panelWidth = int(_screenWidth / JS.jsonRed('resolution_info', "width_divisor"))
    panelHeight = int(_screenHeight / JS.jsonRed('resolution_info', "height_divisor"))

    app_width = _screenWidth - panelWidth
    app_height = _screenHeight - panelHeight

    return _screenWidth, panelWidth, panelHeight, app_width, app_height


def executeCommandFromOPTButton(x: object):  # call def for opt1 commands
    if x == 1:
        print(f"id tlacitka jest:{x}")
    elif x == 2:
        print(f"id tlacitka jest:{x}")
    elif x == 3:
        print(f"id tlacitka jest:{x}")
    elif x == 4:
        print(f"id tlacitka jest:{x}")


class _MenuFrameTemplate:
    def __init__(self, root: tkinter.Tk, sixWidth: int, sixHeight: int):
        self.root = root
        bg_color = '#e5e5e5'

        # master frame
        master_bar = Frame(root, height=sixHeight, bg=bg_color)
        # ↓ forbids frame to resize to button size
        master_bar.pack_propagate(False)
        master_bar.pack(side=TOP, fill=X)

        # menu frame
        self.menuBar = Frame(master_bar, width=sixWidth, bg=bg_color)
        self.menuBar.pack_propagate(False)
        self.menuBar.pack(side=LEFT, fill=Y)

        # options frame
        self.optionsBar = Frame(master_bar, bg=bg_color)
        self.optionsBar.pack_propagate(False)
        self.optionsBar.pack(expand=True, fill=BOTH)


class MenuFrameCreateButtons:
    """Create Menu_Action_Buttons and Back_Action_Button.
    :param text_value: this class creates buttons for menu selection and going back option.
    """

    def __init__(self, width, menu_bar, options_bar, panelWidth: int, sixHeight: int):
        self.sixWidth = panelWidth  # get portion of the screen width
        self.optionsBar = options_bar
        self.sixHeight = sixHeight  # get portion of the screen height
        self.menu_bar = menu_bar  # tkinter menu frame
        self.button_dict = {}  # this thing for creating menu and back buttons
        self.option = []  # array for specifying 'IDs' for buttons
        self.id_of_menu = 1  # value that keeps track of which ID is in use
        self.createOptArr()  # get number of men. and bac. buttons
        self.createMenuAndBackButtons()  # def call
        # call for opt. class buttons:
        self.optButtons = optFrameCreateButtons(optionsBar=options_bar, panelWidth=panelWidth, sixHeight=sixHeight)

    def createOptArr(self):  # this reads values from conf.json and creates array based of length that was given
        _numberOfValues = JS.jsonRed('buttons_info', "num_of_menu_buttons")  # get values from conf.json
        _counter = 1
        while _counter <= _numberOfValues:
            self.option.append(_counter)
            _counter += 1

    def menuActionUp(self):  # this def goes up one menu button: menu_X -> menu_X+1
        if self.id_of_menu == 1:
            new_dict = self.optButtons.button_dict
            for i in new_dict:
                new_dict[i].pack_forget()
        if self.id_of_menu < len(self.option):
            self.button_dict[self.id_of_menu].pack_forget()
            self.button_dict[self.id_of_menu + 1].pack(side=LEFT, expand=True, fill='both')
            self.id_of_menu += 1
        elif self.id_of_menu == len(self.option):
            self.button_dict[self.id_of_menu].pack_forget()
            self.id_of_menu = 1
            self.button_dict[self.id_of_menu].pack(side=LEFT, expand=True, fill='both')
            new_dict = self.optButtons.button_dict  # show again the first opt buttons
            for i in new_dict:
                new_dict[i].pack(side=LEFT, padx=10)

    def createMenuAndBackButtons(self):  # this def creates menu and back action button
        # collecting values for font and colors from def
        getValues = getButtonConf()
        bg = getValues[0]
        bg_active = getValues[1]
        # end of collecting values for font and colors
        for i in self.option:
            self.button_dict[i] = Button(self.menu_bar, text=f"MENU {i}",command=lambda: self.menuActionUp())
            # buttons configuration:
            self.button_dict[i]['activebackground'] = bg_active
            self.button_dict[i]['bg'] = bg
            self.button_dict[i]['font'] = JS.jsonRed('font_info', "font")
            self.button_dict[i]['borderwidth'] = 2
            self.button_dict[i]['relief'] = 'solid'
        self.button_dict[1].pack(side=LEFT, expand=True, fill='both')  # FIRST MENU


class optFrameCreateButtons:
    def __init__(self, optionsBar: tkinter.Frame, panelWidth: int, sixHeight: int):
        self.dummyPixel = PhotoImage(width=1, height=1)
        self.optionsBar = optionsBar
        self.button_dict = {}  # this thing for creating menu and back buttons
        self.option = []  # array for specifying 'IDs' for buttons
        self.sixWidth = panelWidth  # get portion of the screen width
        self.sixHeight = sixHeight  # get portion of the screen height
        self.createOptArr()
        self.createOPT1Buttons()

    def createOptArr(self):  # this reads values from conf.json and creates array based of length that was given
        _numberOfValues = JS.jsonRed('buttons_info', "num_of_opt_on_frame")
        _counter = 1
        while _counter <= _numberOfValues:
            self.option.append(_counter)
            _counter += 1

    def createOPT1Buttons(self):
        # collecting values for font and colors from def
        getValues = getButtonConf()
        bg = getValues[0]
        bg_active = getValues[1]
        # end of collecting values for font and colors
        # -------------------------------------------
        for i in self.option:
            def execCommand(x=i):  # this def stores current i of each button
                executeCommandFromOPTButton(x)
            # button config:
            self.button_dict[i] = Button(self.optionsBar, text=f'OPT#{i}', image=self.dummyPixel, compound="c", command=execCommand)
            self.button_dict[i]['activebackground'] = bg_active
            self.button_dict[i]['width'] = self.sixWidth - 40
            self.button_dict[i]['bg'] = bg
            self.button_dict[i]['font'] = JS.jsonRed('font_info', "font")
            self.button_dict[i]['height'] = self.sixHeight
            self.button_dict[i]['borderwidth'] = 2
            self.button_dict[i]['relief'] = 'solid'

            # show buttons:
            self.button_dict[i].pack(side=LEFT, padx=5)



class Application_frame_temp:
    def __init__(self, root: tkinter.Tk):
        bg_color = JS.jsonRed('colors_info', "app_frame")
        self.root = root
        self.app_frame_width = resolutionMath(root)[3]
        self.app_frame_height = resolutionMath(root)[4]
        self.master_frame = Frame(root, height=self.app_frame_height, bg=bg_color)
        self.master_frame.pack_propagate(False)
        self.master_frame.pack(fill=X)
        self.createExitButton()

    def createExitButton(self):
        exitButtonPokus = Button(self.master_frame, text="E X I T ", command=self.root.destroy, bg="white")
        exitButtonPokus['width'] = self.app_frame_width
        exitButtonPokus['height'] = self.app_frame_height
        exitButtonPokus['activebackground'] = 'white'
        exitButtonPokus.pack()


class App:
    def __init__(self, root: tkinter.Tk):
        sixWidth = resolutionMath(root)[1]  # get sixth of the resolution to make frame width
        sixHeight = resolutionMath(root)[2]  # get sixth of the resolution to make frame height
        width = resolutionMath(root)[0]
        root.title("SeniorOS interface app")
        root.attributes('-fullscreen', True)  # make app fullscreen
        # calling classes
        menuFrameTemp = _MenuFrameTemplate(root, sixWidth, sixHeight)
        self.menuFrameTempVal = menuFrameTemp.optionsBar  # return class frame value

        menuFrameCreateButtons = MenuFrameCreateButtons(width, menuFrameTemp.menuBar, menuFrameTemp.optionsBar,
                                                        sixWidth, sixHeight)
        self.menuFrameCreateButtonsVal = menuFrameCreateButtons
