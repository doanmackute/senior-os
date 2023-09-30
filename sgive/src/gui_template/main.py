from pprint import pprint
from tkinter import *
import guiTemplate as temp
import configActions as act


if __name__ == '__main__':
    root = Tk()
    value = temp.App(root)
    print("value jest:",value.menuFrameTempVal)

    root.mainloop()
    """
    confCheck = act.configExistCheck()
    if confCheck:
        root = Tk()
        temp.App(root)



    """
