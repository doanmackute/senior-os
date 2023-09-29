from tkinter import *
from tkinter import font

import json_actions as JS
import json
import os


def resolution_math(root):
    _screen_width = root.winfo_screenwidth()
    _screen_height = root.winfo_screenheight()
    screen_res = f"{_screen_width}x{_screen_height}"
    fifth_width = int(_screen_width / 4.5)
    fifth_height = int(_screen_height / 4.5)
    app_width = _screen_width - fifth_width
    app_height = _screen_height - fifth_height
    return [screen_res, fifth_width, fifth_height, app_width, app_height]


class _Menu_frame_temp:
    def __init__(self, root):
        self.root = root
        bg_color = '#e5e5e5'
        sixWidth = resolution_math(root)[1]
        sixHeight = resolution_math(root)[2]

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
    def __init__(self, menu_bar, exit_bar, options_bar, sixWidth, sixHeight):
        self.menu_bar = menu_bar
        self.exit_bar = exit_bar
        self.options_bar = options_bar
        self.button_dict = {}
        self.option = [1, 2, 3, 4]
        self.value = 0
        self.fontSize = font.Font(family='Halvetica', size=36, weight=font.BOLD)

        # this isn't final version :)
        def menu_back_buttons():
            def menu_action_up(text):  # pohyb z menu_x na menu_x+1
                if not text >= 3:  # hradlo, aby to nezmizelo
                    self.button_dict[text].pack_forget()
                    self.button_dict[text + 1].pack()

            for i in self.option:
                def func(x=i):
                    self.value = x
                    return menu_action_up(x)

                def menu_action_back():  # vraci menu_x na menu_x-1
                    if self.value == 3:
                        self.button_dict[self.value].pack_forget()
                        self.button_dict[self.value - 1].pack()
                        self.value = self.value - 2
                    elif self.value == 0:
                        return
                    else:
                        self.button_dict[self.value + 1].pack_forget()
                        self.button_dict[self.value].pack()
                        self.value = self.value - 1

                if (i == 4): #BACK BUTTON conf
                    self.button_dict[i] = Button(self.exit_bar, text=f"BACK#{i}", command=menu_action_back)
                else: # MENU BUTTONS conf
                    self.button_dict[i] = Button(self.menu_bar, text=f"MENU#{i}", command=func)
                self.button_dict[i]['activebackground'] = '#00ff00'
                self.button_dict[i]['width'] = sixWidth
                self.button_dict[i]['height'] = sixHeight
                self.button_dict[i]['font'] = self.fontSize

            self.button_dict[1].pack()  # FIRST MENU
            self.button_dict[4].pack()  # BACK

        menu_back_buttons()


class Application_frame_temp:
    def __init__(self, root):
        bg_color = '#FFFFFF'
        self.root = root
        self.app_frame_width = resolution_math(root)[3]
        self.app_frame_height = resolution_math(root)[4]
        self.master_frame = Frame(root, height=self.app_frame_height, bg=bg_color)
        self.master_frame.pack_propagate(False)
        self.master_frame.pack(fill=X)

    def create_exit_button(self, text_value=str()):
        exitButtonPokus = Button(self.master_frame, text=text_value, command=self.root.destroy, bg="white")
        exitButtonPokus['width'] = self.app_frame_width
        exitButtonPokus['height'] = self.app_frame_height
        exitButtonPokus.pack()


class App:
    def __init__(self, root):
        self.root = root
        root.title("SeniorOS interface app")
        root.attributes('-fullscreen', True)
        _Menu_frame_temp(root)
