from pprint import pprint
from tkinter import *
import guiTemplate as temp
import configActions as act


if __name__ == '__main__':
    isExist = act.configExistCheck()
    if isExist[0]:
        root = Tk()
        temp.App(root)
        temp.Application_frame_temp(root)
        root.mainloop()
    else:
        print("there is no conf.json present in the system")
        exit(0)

