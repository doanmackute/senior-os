from tkinter import *
import configurationActions as ryuconf
import os
import logging
import CaregiverGUI as ryuGUI

logging.basicConfig(
    filename=os.path.join(ryuconf.temporaryGetPath(), 'CaregiverAPP.log'),
    level=logging.INFO,
    format="%(asctime)s : %(levelname)s -> %(module)s %(funcName)s %(lineno)s : %(message)s",
    filemode='w+',
)

if __name__ == '__main__':
    root = Tk()
    ryuGUI.AppBase(root)
    root.mainloop()