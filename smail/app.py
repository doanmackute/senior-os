import tkinter
import demo.guiTemplate.configActions as act
import demo.guiTemplate.guiTemplate as temp
import smail.layout
from smail.layout import defaultFrame, readMailFrame
from tkinter import *

def change_frame():
    if frame.currentFrame.__class__ is readMailFrame:
        print("readMailFrame")
        frame.showWriteMailFrame()
    else:
        print(frame.currentFrame.__class__)
        print(readMailFrame)
        frame.showReadMailFrame()


def main():

    root = Tk()
    app = temp.App(root)

    global frame
    frame = defaultFrame(root)

    options_buttons_crt1 = app.menuFrameCreateButtonsVal.optButtons1
    options_buttons_crt2 = app.menuFrameCreateButtonsVal.optButtons2
    sendButtonText = "Send Email"
    person1Text = "Person1"
    person2Text = "Person2"
    person3Text = "Person3"
    person4Text = "Person4"
    person5Text = "Person5"
    sendToText = "Send To"

    options_buttons_crt1.button_dict[2].config(text=sendButtonText, command = change_frame)
    options_buttons_crt1.button_dict[3].config(text=person1Text)
    options_buttons_crt1.button_dict[4].config(text=person2Text)
    options_buttons_crt2.button_dict[1].config(text=person3Text)
    options_buttons_crt2.button_dict[2].config(text=person4Text)
    options_buttons_crt2.button_dict[3].config(text=person5Text)
    options_buttons_crt2.button_dict[4].config(text=sendToText)

    root.mainloop()

if __name__ == '__main__':
    main()