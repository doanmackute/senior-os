from tkinter import *
import guiTemplate as temp
try:
    import sgive.src.gui_template.configActions as act
except ImportError:
    print("error")
try:
    import configActions as act
except ImportError:
    print("Error")

if __name__ == '__main__':
    _currentVersionOfConfig = 0.2
    isExist = act.configExistCheck(_currentVersionOfConfig)
    if isExist:
        root = Tk()
        temp.App(root)
        AppResolution = temp.resolutionMath()
        print(f"resolution of the app is:{AppResolution[3]}x{AppResolution[4]}")
        root.mainloop()
    else:
        print("LOG: there is no conf.json present in the system")
        exit(1)
