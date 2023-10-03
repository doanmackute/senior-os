import json
import os


def configExistCheck():
    # path to config.json ~/.config/seniorOS-JSON/*
    pathToJsonConf = os.path.join(os.path.expanduser('~'), '.config/seniorOS-JSON')
    # this checks, if user even exist
    if os.path.expanduser('~') is None:
        print("Where is your home mate?")
        return False, None
    # creates the folder if it doesn't exist
    if not os.path.exists(pathToJsonConf):
        os.mkdir(pathToJsonConf)
        _jsonWrite(pathToJsonConf)
        return True, pathToJsonConf
    else:
        _jsonWrite(pathToJsonConf)  # making sure there is no old version of the conf.json
        return True, pathToJsonConf


def _jsonWrite(pathToJsonConf):
    # path to .json conf
    print(f"making sure there is path: {pathToJsonConf}")
    dictionary = {
        'buttons_info': {
            "num_of_frame": 4,
            "num_of_menu_buttons": 2,
            "num_of_opt_buttons": 12,
            "num_of_opt_on_frame": 4
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
    with open(f"{pathToJsonConf}/config.json", "w+") as outfile:
        outfile.write(json_object)


def jsonRed(key, value):
    path_to_json = os.path.join(os.path.expanduser('~'), '.config/seniorOS-JSON')
    # if there is no user, leave
    if os.path.expanduser('~') is None:
        print("Where is your home mate?")
        return
    with open(os.path.join(path_to_json, 'config.json'), "r") as file:
        jsonData = json.load(file)
    return jsonData[key][value]


if __name__ == '__main__':
    idkValue = configExistCheck()
    if idkValue[0]:
        print("sex")
        _jsonWrite(idkValue[1])

    check = configExistCheck()
