import json, codecs
import os
import logging

logger = logging.getLogger(__file__)
logger.info("initiated logging")


def temporaryGetPath():  # this is how i get to the sconf/ file, for now :)
    currentDir = os.path.dirname(os.path.dirname(__file__))
    parentCurentDir = os.path.abspath(os.path.join(currentDir, os.pardir))
    supaParent = os.path.abspath(os.path.join(parentCurentDir, os.pardir))
    confPath = os.path.join(supaParent, "sconf")
    return confPath


def readFile(key, value):
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


def testRead(key, value):
    with open('data.json', "r") as file:
        jsonData = json.load(file)
    return jsonData[key][value]


def editConfig(key, name, value):
    # this def edits name in conf.json to value
    with open('data.json', 'r') as file:
        data = json.load(file)
        data[key][name] = value
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


def caregiverAppConfig():
    options = ["Global\nconfig", "Mail", "Web", "LOGS"]
    dictionary = {
        'GlobalConfiguration': {
            "language": "czech",
            "colorMode": "colorfull",
            "soundDelay": 5,
            "alertColor": "green",
            "alertSoundLanguage": "czech",
            "fontSize": "36",
            "fontFamily": "someCoolName",
            "macAddress": "1:1:1:1:",
        },
        'smail': {
            "smtp": "czech",
            "imap": "colorful",
            "icons": 5,
            "photographyURL": "red",
            "soundsUrl": "czech",
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
            "menuButtonsList": options.copy()
        },
    }
    json_object = json.dumps(dictionary, indent=4)
    with open('data.json', "w+") as outfile:
        outfile.write(json_object)
