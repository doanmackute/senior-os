import json
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
    if os.path.exists(path) and os.path.isfile(os.path.join(temporaryGetPath(), 'config.json')):  # checks for the conf file, if there is any
        with open(os.path.join(path, 'config.json'), "r") as file:
            jsonData = json.load(file)
            logging.info('Data was successfully loaded')
        return jsonData[key][value]
    else:
        logging.critical('There is no config.json or sconf/ file present in system, exiting program now.')
        exit(1)