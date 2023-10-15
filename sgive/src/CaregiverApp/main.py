from tkinter import *
import configurationActions as ryuconf
import os
import CaregiverGUI as ryuGUI
import logging

logging.basicConfig(
    filename=os.path.join(ryuconf.temporaryGetPath(), 'CaregiverAPP.log'),
    level=logging.INFO,
    format="%(asctime)s : %(levelname)s -> %(module)s %(funcName)s %(lineno)s : %(message)s",
    filemode='w+',
)

if __name__ == '__main__':
    whereTheFuckAmI = os.getcwd()
    split = whereTheFuckAmI.split("sgive")
    path = split[0]
    configPath = os.path.join(path, "sconf")
    #create config, only if there is not any config.json already
    if os.path.exists(configPath) and not os.path.isfile(os.path.join(configPath, 'config.json')):
        ryuconf.caregiverAppConfig(configPath)

    root = Tk()
    ryuGUI.AppBase(root)
    root.mainloop()
