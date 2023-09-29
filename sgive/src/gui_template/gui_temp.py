import tkinter
from tkinter import *
from tkinter import font
import json_actions as JS


def resolutionMath(root: tkinter.Tk):
    _screenWidth = root.winfo_screenwidth()
    _screenHeight = root.winfo_screenheight()
    screen_res = f"{_screenWidth}x{_screenHeight}"
    fifth_width = int(_screenWidth / 4.5)
    fifth_height = int(_screenHeight / 4.5)
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

        Buttons_menu_bar(menu_bar, exit_bar, options_bar, sixWidth, sixHeight)


class Buttons_menu_bar:
    def __init__(self, menu_bar: tkinter.Frame, exit_bar: tkinter.Frame, options_bar: tkinter.Frame, sixWidth: int, sixHeight: int):
        self.sixWidth = sixWidth
        self.sixHeight = sixHeight
        self.menu_bar = menu_bar
        self.exit_bar = exit_bar
        self.options_bar = options_bar
        self.button_dict = {}
        self.option = [1, 2, 3, 4, 5]
        self.value = 0
        self.fontSize = font.Font(family='Halvetica', size=36, weight=font.BOLD)
        self.bg = JS.jsonRed('colors_info', "buttons_unselected")
        self.bg_active = JS.jsonRed('colors_info', "buttons_selected")
        self.id_of_menu = 1
        print("ČUM SEM", len(self.option))
        self.menu_back_buttons()

    def menu_act_up(self):
        # here is 'len(self.option) - 1', because the last one is back button
        if not self.id_of_menu >= len(self.option) - 1:
            self.button_dict[self.id_of_menu].pack_forget()
            self.button_dict[self.id_of_menu + 1].pack()
            self.id_of_menu += 1

    def menu_act_down(self):
        if not self.id_of_menu == 1:
            self.button_dict[self.id_of_menu].pack_forget()
            self.button_dict[self.id_of_menu - 1].pack()
            self.id_of_menu -= 1

    def menu_back_buttons(self):
        for i in self.option:
            if i == len(self.option):  # BACK BUTTON conf
                self.button_dict[i] = Button(self.exit_bar, text=f"BACK", command=lambda: self.menu_act_down())
            else:  # MENU BUTTONS conf
                self.button_dict[i] = Button(self.menu_bar, text=f"MENU#{i}", command=lambda: self.menu_act_up())
            self.button_dict[i]['activebackground'] = self.bg_active
            self.button_dict[i]['bg'] = self.bg
            self.button_dict[i]['width'] = self.sixWidth
            self.button_dict[i]['height'] = self.sixHeight
            self.button_dict[i]['font'] = self.fontSize
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
