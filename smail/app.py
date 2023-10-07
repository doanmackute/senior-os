import tkinter
from smail.template import configActions as act
from smail.layout import oneFrame


if __name__ == '__main__':
    _currentVersionOfConfig = 0.3
    isExist = act.configExistCheck(_currentVersionOfConfig)
    if isExist:
        root = tkinter.Tk()
        app = oneFrame(root)
        root.mainloop()
    else:
        print("error")
