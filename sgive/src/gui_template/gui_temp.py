import tkinter
from tkinter import *
from tkinter import font
import json_actions as JS


def resolutionMath(root: tkinter.Tk):
    _screenWidth = root.winfo_screenwidth()
    _screenHeight = root.winfo_screenheight()
    _get_factor = JS.jsonRed('resolution_info', "factor")
    screen_res = f"{_screenWidth}x{_screenHeight}"
    fifth_width = int(_screenWidth / _get_factor)
    fifth_height = int(_screenHeight / _get_factor)
    app_width = _screenWidth - fifth_width
    app_height = _screenHeight - fifth_height
    return [screen_res, fifth_width, fifth_height, app_width, app_height]


class _MenuFrameTemplate:
    def __init__(self, root: tkinter.Tk):
        self.root = root
        bg_color = '#e5e5e5'
        sixWidth = resolutionMath(root)[1]
        sixHeight = resolutionMath(root)[2]

        # master frame
        master_bar = Frame(root, height=sixHeight, bg=bg_color)
        # ↓ forbids frame to resize to button size
        master_bar.pack_propagate(False)
        master_bar.pack(side=TOP, fill=X)

        # menu frame
        menu_bar = Frame(master_bar, width=sixWidth, bg=bg_color)
        menu_bar.pack_propagate(False)
        menu_bar.pack(side=LEFT, fill=Y)

        # exit frame
        exit_bar = Frame(master_bar, width=sixWidth, bg=bg_color)
        exit_bar.pack_propagate(False)
        exit_bar.pack(side=RIGHT, fill=Y)

        # options frame
        options_bar = Frame(master_bar, bg=bg_color)
        options_bar.pack_propagate(False)
        options_bar.pack(expand=True, fill=BOTH)

        MenuFrameCreateButtons(menu_bar, exit_bar, sixWidth, sixHeight)


class MenuFrameCreateButtons:
    """Create Menu_Action_Buttons and Back_Action_Button.
    :param text_value: this class creates buttons for menu selection and going back option.
    """
    def __init__(self, menu_bar: tkinter.Frame, exit_bar: tkinter.Frame, sixWidth: int, sixHeight: int):
        self.sixWidth = sixWidth            # get portion of the screen width
        self.sixHeight = sixHeight          # get portion of the screen height
        self.menu_bar = menu_bar            # tkinter menu frame
        self.exit_bar = exit_bar            # tkinter back frame
        self.button_dict = {}               # this thing for creating menu and back buttons
        self.option = []                    # array for specifying 'IDs' for buttons
        self.id_of_menu = 1                 # value that keeps track of which ID is in use
        self.createOptArr()                 # get number of men. and bac. buttons
        self.createMenuAndBackButtons()     # def call

    def createOptArr(self):  # this reads values from conf.json and creates array based of length that was given
        _numberOfValues = JS.jsonRed('buttons_info', "num_menu_back_buttons")
        _counter = 1
        while _counter <= _numberOfValues:
            self.option.append(_counter)
            _counter += 1

    def menuActionUp(self):  # this def goes up one menu button: menu_X -> menu_X+1
        # here is 'len(self.option) - 1', because the last one is back button
        if not self.id_of_menu >= len(self.option) - 1:
            self.button_dict[self.id_of_menu].pack_forget()
            self.button_dict[self.id_of_menu + 1].pack()
            self.id_of_menu += 1

    def menuActionDown(self):    # this def goes back one menu button: menu_X -> menu_X-1
        if not self.id_of_menu == 1:
            self.button_dict[self.id_of_menu].pack_forget()
            self.button_dict[self.id_of_menu - 1].pack()
            self.id_of_menu -= 1

    def createMenuAndBackButtons(self):    # this def creates menu and back action button
        # collecting values for font and colors
        bg = JS.jsonRed('colors_info', "buttons_unselected")
        bg_active = JS.jsonRed('colors_info', "buttons_selected")
        _fontFamily = JS.jsonRed('font_info', "family")
        _fontSize = JS.jsonRed('font_info', "size")
        fontInfo = font.Font(family=_fontFamily, size=_fontSize, weight=font.BOLD)
        # end of collecting values for font and colors
        for i in self.option:
            if i == len(self.option):  # BACK BUTTON conf, checks for last value in array
                self.button_dict[i] = Button(self.exit_bar, text=f"BACK", command=lambda: self.menuActionDown())
            else:  # MENU BUTTONS conf
                self.button_dict[i] = Button(self.menu_bar, text=f"MENU#{i}", command=lambda: self.menuActionUp())
            # button configuration
            self.button_dict[i]['activebackground'] = bg_active
            self.button_dict[i]['bg'] = bg
            self.button_dict[i]['width'] = self.sixWidth
            self.button_dict[i]['height'] = self.sixHeight
            self.button_dict[i]['font'] = fontInfo
            self.button_dict[i]['borderwidth'] = 2
            self.button_dict[i]['relief'] = 'solid'
        # show first menu and back button
        self.button_dict[1].pack()  # FIRST MENU
        self.button_dict[len(self.option)].pack()  # BACK (is the last button)


class Application_frame_temp:
    def __init__(self, root: tkinter.Tk):
        bg_color = '#FFFFFF'
        self.root = root
        self.app_frame_width = resolutionMath(root)[3]
        self.app_frame_height = resolutionMath(root)[4]
        self.master_frame = Frame(root, height=self.app_frame_height, bg=bg_color)
        self.master_frame.pack_propagate(False)
        self.master_frame.pack(fill=X)

    def create_exit_button(self, text_value: str) -> None:
        """Populate exit buttons.
        :param text_value: Description of the exit button.
        """
        exitButtonPokus = Button(self.master_frame, text=text_value, command=self.root.destroy, bg="white")
        exitButtonPokus['width'] = self.app_frame_width
        exitButtonPokus['height'] = self.app_frame_height
        exitButtonPokus['activebackground'] = 'white'
        exitButtonPokus.pack()


class App:
    def __init__(self, root: tkinter.Tk):
        self.root = root
        root.title("SeniorOS interface app")
        root.attributes('-fullscreen', True)
        _MenuFrameTemplate(root)
