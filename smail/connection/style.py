import logging
import json
import pygame
from tkinter import ttk
import PIL
from PIL import Image, ImageTk
from demo.guiTemplate.guiTemplate import resolutionMath

logger = logging.getLogger(__file__)

def font_config():
    try:
        with open("../sconf/config.json", "r") as f:
            config = json.loads(f.read())
            font_info = config["font_info"]["font"]
        f.close()
        return font_info
    except Exception:
        logger.error("Couldn't read fontconfig, file is missing.", exc_info=True)


def button_config():

    font_info = font_config()
    style = ttk.Style()
    style.configure("my.TButton", font=font_info)

    return "my.TButton"

def app_color():
    try:
        with open("../sconf/config.json", "r") as f:
            config = json.loads(f.read())
            bg = config["colors_info"]["app_frame"]
        f.close()
        return bg
    except Exception:
        logger.error("Couldn't read application color, file is missing.", exc_info=True)


def images():
    try:
        with open("../sconf/SMAIL_config.json", "r") as f:
            data = json.loads(f.read())
            images = data["images"]
        f.close()
        return images
    except Exception:
        logger.error("Couldn't find SMAIL_config.json", exc_info=True)



def search_mail(id):
    try:
        with open("../sconf/SMAIL_config.json", "r") as f:
            data = json.loads(f.read())
            emails = data["emails"]
            email = emails[f"Person{id}"]
        f.close()
        return email
    except Exception:
        logger.error("Couldn't find SMAIL_config.json", exc_info=True)


def get_language():
    try:
        with open("../sconf/SMAIL_config.json") as f:
            data = json.loads(f.read())
            language = data["lang"]
            text = data["text"]
        f.close()
        return language, text
    except Exception:
        logger.error("Couldn't find SMAIL_config.json",
                     exc_info=True)


# audio session
def get_audio():
    # reads configuration from json file
    try:
        with open("../sconf/SMAIL_config.json") as f:
            data = json.loads(f.read())
            language = data["lang"]
            audio = data["audio"]
            timer = data["timer"]
        f.close()
        return language, audio, timer
    except Exception:
        logger.error("Couldn't find SMAIL_config.json",
                     exc_info=True)


def play_sound(button_name):
    pygame.mixer.init()
    language, audio, timer = get_audio()
    # Loads the audio file corresponding to the button_name.
    pygame.mixer.music.load(audio[f"smail_{language}_{button_name}"])
    # Plays the loaded audio.
    pygame.mixer.music.play()


def button_hover(button, button_name, enter_time):
    # Function is called when the mouse cursor hovers over a button.
    language, audio, timer = get_audio()
    # It schedules playing sound after a specified time delay.
    # It stores the scheduled time event ID in enter_time[0].
    enter_time[0] = button.after(timer, lambda: play_sound(button_name))


def button_leave(button, enter_time):
    # Function is called when the mouse cursor leaves the button.
    # It checks if there is a scheduled event and cancels it if it exists.
    # This ensures that the sound won't play if the mouse leaves the button
    # before the specified delay.
    if enter_time[0]:
        button.after_cancel(enter_time[0])

def image_config(name, btn_height):
    data = images()
    path = data[name]
    original_image = Image.open(path)
    height_ratio = btn_height / original_image.height
    new_height = int(original_image.height * height_ratio)
    resized_image = original_image.resize((int(original_image.width * height_ratio), new_height), PIL.Image.LANCZOS)
    image = ImageTk.PhotoImage(resized_image)
    return image

def height_config(parent):

    font_base = font_config()

    # pt to pixels
    font = font_base.split(" ")
    font_size = int(font[1])
    font_size_in_pixels = font_size / 0.75

    # resolution info
    parent_height = parent.winfo_screenheight()
    area_of_upper_widget = resolutionMath()[2]
    usable_height = parent_height - area_of_upper_widget

    # calculating widget height
    number_of_lines_listbox = int((usable_height - font_size_in_pixels * 3) / font_size_in_pixels)
    number_of_lines_textarea = int((usable_height - font_size_in_pixels * 6) / font_size_in_pixels)

    return number_of_lines_listbox, number_of_lines_textarea
