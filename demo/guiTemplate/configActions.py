import json
import os

def temporaryGetPath():
    currentDir = os.path.dirname(os.path.dirname(__file__))
    parentCurentDir = os.path.abspath(os.path.join(currentDir, os.pardir))
    # (if launched in sgive, it is needed)
    # supaParent = os.path.abspath(os.path.join(parentCurentDir, os.pardir))
    confPath = os.path.join(parentCurentDir, "sconf")
    return confPath


def configExistCheck():
    pathToJsonConf = temporaryGetPath()
    if os.path.exists(pathToJsonConf):
        _jsonWrite()
        return True
    else:
        print("LOG: there is no path to the configuration file")
        return False

def _jsonWrite():
    # path to .json conf
    dictionary = {
        'buttons_info': {
            "num_of_frame": 4,
            "num_of_menu_buttons": 2,
            "num_of_opt_on_frame": 4,
            "padx_value": 5,
        },
        'colors_info': {
            "menu_frame": "#e5e5e5",
            "app_frame": "#FFFFFF",
            "buttons_unselected": "#e5e5e5",
            "buttons_selected": "#00ff00",
        },
        'font_info': {
            "font": "Helvetica 36 bold",
        },
        'resolution_info': {
            "height_divisor": 4.5,
            "width_divisor": 5,
        }
    }
    json_object = json.dumps(dictionary, indent=4)
    with open(f"{temporaryGetPath()}/config.json", "w+") as outfile:
        outfile.write(json_object)


def jsonRed(key, value):
    path = temporaryGetPath()
    # if there is no user, leave
    if os.path.expanduser('~') is None:
        print("Where is your home mate?")
        return
    if os.path.exists(path): #checks for the conf file, if there is any
        with open(os.path.join(path, 'config.json'), "r") as file:
            jsonData = json.load(file)
        return jsonData[key][value]
    else:
        print("LOG: there is no path to the configuration file")
        return
