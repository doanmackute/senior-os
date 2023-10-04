from tkinter import *
import guiTemplate as temp
import demo.guiTemplate.configActions as act


if __name__ == '__main__':
    isExist = act.configExistCheck()
    if isExist:
        root = Tk()
        temp.App(root)

        AppResolution = temp.resolutionMath(root)
        print(f"resolution of the app is:{AppResolution[3]}x{AppResolution[4]}")

        root.mainloop()
    else:
        print("LOG: there is no conf.json present in the system")
        exit(1)
