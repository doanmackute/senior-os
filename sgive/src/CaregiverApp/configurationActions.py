import json
import os
import logging
from getmac import get_mac_address as gmac

logger = logging.getLogger(__file__)
logger.info("initiated logging")


def temporaryGetPath():  # this is how i get to the sconf/ file, for now :)
    whereTheFuckAmI = os.getcwd()
    split = whereTheFuckAmI.split("sgive")
    path = split[0]
    configPath = os.path.join(path, "sconf")
    return configPath


def readJsonConfig(key, value):
    path = temporaryGetPath()
    if os.path.exists(path) and os.path.isfile(
            os.path.join(temporaryGetPath(), 'config.json')):  # checks for the conf file, if there is any
        with open(os.path.join(path, 'config.json'), "r") as file:
            jsonData = json.load(file)
        return jsonData[key][value]
    else:
        logging.critical('There is no config.json or sconf/ file present in system, exiting program now.')
        exit(1)


def readLog():
    path = temporaryGetPath()
    if os.path.exists(path) and os.path.isfile(os.path.join(temporaryGetPath(), 'CaregiverAPP.log')):
        file = open(os.path.join(path, 'CaregiverAPP.log'), "r")
        return [file.read()]
    else:
        logging.critical('There is no CaregiverApp.log or sconf/ file present in system, exiting program now.')
        exit(1)


def editConfig(key, name, value):
    # this def edits name in conf.json to value
    path = temporaryGetPath()
    # checks for the conf file, if there is any
    if os.path.exists(path) and os.path.isfile(os.path.join(temporaryGetPath(), 'config.json')):
        with open(os.path.join(path, 'config.json'), 'r') as file:
            data = json.load(file)
            data[key][name] = value
        with open(os.path.join(path, 'config.json'), 'w') as f:
            json.dump(data, f, indent=4)
    logging.info(f'successfully edited value: "{value}" at key: "{name}".')


def getMac():
    mac = gmac()
    return mac


def caregiverAppConfig(path):
    options = ["Global\nconfig", "Mail\nconfig", "Web\nconfig", "LOGS"]
    languageOPT = ["Czech", "English", "German"]
    dictionary = {
        'pathToConfig': {
            "path": path
        },
        'GlobalConfiguration': {
            "numOfScreen": 0,
            "language": "English",
            "colorMode": "Light",
            "soundDelay": 5,
            "alertColor": "#AAFF00",
            "alertSoundLanguage": "english",
            "fontSize": 36,
            "labelFontSize": 12,
            "fontThickness": "bold",
            "fontFamily": "Helvetica",
            "macAddress": getMac(),
        },
        'smail': {
            "smtp": "X",
            "imap": "X",
            "icons": "X",
            "photographyURL": "X",
            "soundsUrl": "X",
        },
        'sweb': {
            "photography": "X",
            "iconsURL": "X",
            "sounds": "X",
        },
        'careConf': {
            "fg": 5,
            "bg": 5,
            "heightDivisor": 7,
            "menuButtonsList": options.copy(),
            "LanguageOptions": languageOPT.copy()

        },
    }
    json_object = json.dumps(dictionary, indent=4)
    with open(os.path.join(path, 'config.json'), "w+") as outfile:
        outfile.write(json_object)
