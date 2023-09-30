from tkinter import *
import guiTemplate as temp
import configActions as act

if __name__ == '__main__':
    confCheck = act.configExistCheck()
    if confCheck:
        print("main")
        root = Tk()
        temp.App(root)
        idk = temp.Application_frame_temp(root)
        idk.create_exit_button("EXIT")
        root.mainloop()
