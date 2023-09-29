import json_actions
from tkinter import *
import os, sys

def resolution_math(root):
    _screen_width = root.winfo_screenwidth()
    _screen_height = root.winfo_screenheight()
    screen_res=f"{_screen_width}x{_screen_height}"
    fifth_width = int(_screen_width/4.5)
    fifth_height = int(_screen_height/4.5)
    app_width = _screen_width - fifth_width
    app_height = _screen_height - fifth_height
    return [screen_res,fifth_width,fifth_height,app_width,app_height]


class Menu_frame:
    def __init__(self, root):
        self.root = root
        bg_color='#e5e5e5'
        sixWidth = resolution_math(root)[1]
        sixHeight = resolution_math(root)[2]
        # master frame
        master_bar = Frame(root, height=sixHeight, bg=bg_color)
        # ↓ forbids frame to resize to button size
        master_bar.pack_propagate(False)
        master_bar.pack(side=TOP, fill=X)

        # menu frame
        menu_bar = Frame(master_bar, width=sixWidth,bg=bg_color)
        menu_bar.pack_propagate(False)
        menu_bar.pack(side=LEFT, fill=Y)

        # exit frame
        exit_bar = Frame(master_bar, width=sixWidth,bg=bg_color)
        exit_bar.pack_propagate(False)
        exit_bar.pack(side=RIGHT, fill=Y)

        # options frame
        options_bar = Frame(master_bar, bg=bg_color)
        options_bar.pack_propagate(False)
        options_bar.pack(expand=True, fill=BOTH)

        # call class for buttons
        Buttons(master_bar, menu_bar, exit_bar, options_bar)
class Aplication_frame:
    def __init__(self, root):
        self.root = root
        bg_color='#FFFFFF'
        app_frame_width = resolution_math(root)[3]
        app_frame_heigh =  resolution_math(root)[4]

        master_frame = Frame(root,height=app_frame_heigh, bg=bg_color)
        master_frame.pack_propagate(False)
        master_frame.pack(fill=X)

        def createExitButton():
            exitButtonPokus = Button(master_frame, text="EXIT", command=self.root.destroy,bg="white")
            exitButtonPokus['width'] = app_frame_width
            exitButtonPokus['height']= app_frame_heigh
            exitButtonPokus.pack()
        createExitButton()

class Buttons:
    def __init__(self, master_bar, menu_bar, exit_bar, options_bar):
        self.master_bar = master_bar
        self.menu_bar = menu_bar
        self.exit_bar = exit_bar
        self.options_bar = options_bar


class App:
    def __init__(self,root):
        self.root = root

        root.title("SeniorOS interface app")
        root.attributes('-fullscreen', True)
        Menu_frame(root)
        Aplication_frame(root)


if __name__ == '__main__':
    root = Tk()

    print("main")
    App(root)
    root.mainloop()
    print(os.path.join(os.path.expanduser('~'),'.config'))

