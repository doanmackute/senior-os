import logging
import tkinter
from demo.guiTemplate import configActions as act
from smail.layout import oneFrame

logging.basicConfig(
     level=logging.INFO,
     filename="SMAILlog.log",
     filemode="w",
     format="%(asctime)s:SMAIL-%(levelname)s-%(funcName)s: %(message)s",
     datefmt="%b %d %H:%M:%S",
)

if __name__ == '__main__':
    _currentVersionOfConfig = 0.3
    isExist = act.configExistCheck(_currentVersionOfConfig)
    if isExist:
        root = tkinter.Tk()
        root.configure(bg="#FFFFFF")
        app = oneFrame(root)
        root.mainloop()


    else:
        logging.critical("Could not start smail app. "
                         "Check the configuration file.")
