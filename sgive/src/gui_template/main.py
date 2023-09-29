from tkinter import *
import gui_temp as temp
import json_actions as jason

if __name__ == '__main__':
    #jason._jsonWrite()
    print("main")
    root = Tk()
    temp.App(root)
    idk = temp.Application_frame_temp(root)
    idk.create_exit_button("EXIT")
    root.mainloop()
