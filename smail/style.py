import json
from tkinter import ttk

def font_config():

    with open("../sconf/config.json", "r") as f:
        config = json.loads(f.read())
        font_info = config["font_info"]["font"]
    f.close()

    return font_info

def button_config():
    with open("../sconf/config.json", "r") as f:
        config = json.loads(f.read())
        font_info = config["font_info"]["font"]
    f.close()

    style = ttk.Style()
    style.configure("my.TButton", font=font_info)

    return "my.TButton"
