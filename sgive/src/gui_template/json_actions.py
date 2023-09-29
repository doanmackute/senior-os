import json
import os


def _jsonWrite():
    # path to .json conf
    path_to_json = os.path.join(os.path.expanduser('~'), '.config/seniorOS-JSON')
    # if there is no user, leave
    if os.path.expanduser('~') is None:
        print("Where is your home mate?")
        return
    # this creates dir if it doesn't exist
    if not os.path.exists(path_to_json):
        os.mkdir(path_to_json)

    dictionary = {
        'buttons_info': {
            "num_of_frame": "4",
            "num_menu_back_buttons": "5",
            "num_of_opt_buttons": "12",
            "num_of_opt_on_frame": "4"
        },
        'frame_info': {
            "master_frame_width": "X",
            "master_frame_height": "X",
            "sub_options_frame_width": "X",
            "sub_options_frame_height": "X",
            "sub_menu_frame_width": "X",
            "sub_menu_frame_height": "X",
            "sub_back_frame_width": "X",
            "sub_back_frame_height": "X",
            "application_frame_width": "X",
            "application_frame_height": "X",
        },
        'colors_info': {
            "menu_frame": "#e5e5e5",
            "app_frame": "#FFFFFF",
            "buttons_unselected": "#e5e5e5",
            "buttons_selected": "#00ff00",
        },
        'font_info': {
            "screenResolution": "68",
        },
        'resolution_info': {
            "frame_divisor": 5,
        }
    }
    json_object = json.dumps(dictionary, indent=4)
    with open(f"{path_to_json}/config.json", "w+") as outfile:
        outfile.write(json_object)

def jsonRed(key: str,value: str):
    path_to_json = os.path.join(os.path.expanduser('~'), '.config/seniorOS-JSON')
    # if there is no user, leave
    if os.path.expanduser('~') is None:
        print("Where is your home mate?")
        return
    with open(os.path.join(path_to_json, 'config.json'), "r") as file:
        jsonData = json.load(file)
    return jsonData[key][value]


if __name__ == '__main__':
    _jsonWrite()
    value = jsonRed('buttons_info', "num_of_frame")
    print(value)