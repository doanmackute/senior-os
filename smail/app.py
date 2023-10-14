import logging
import tkinter
from demo.guiTemplate import configActions as act
from smail.layout import one_frame

logging.basicConfig(
     level=logging.INFO,
     filename="../sconf/SMAILlog.log",
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
        app = one_frame(root)
        root.mainloop()


    else:
        logging.critical("Could not start smail app. "
                         "Check the configuration file.")
