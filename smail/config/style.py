import json
import pygame
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


def images():

    with open("config/email_address_config.json", "r") as f:
        data = json.loads(f.read())
        images = data["images"]
    f.close()

    return images


def search_mail(id):
    with open("config/email_address_config.json", "r") as f:
        data = json.loads(f.read())
        emails = data["emails"]
        email = emails[f"Person{id}"]
    f.close()
    return email


def getLanguage():
    with open("config/translate.json") as f:
        translate = json.loads(f.read())
        language = translate["lang"]
        text = translate["text"]
    f.close()
    return language, text


# audio session
def getAudio():
    # reads configuration from json file
    with open("config/translate.json") as f:
        translate = json.loads(f.read())
        language = translate["lang"]
        audio = translate["audio"]
        timer = translate["timer"]
    f.close()
    return language, audio, timer


def play_sound(button_name):
    pygame.mixer.init()
    language, audio, timer = getAudio()
    # Loads the audio file corresponding to the button_name.
    pygame.mixer.music.load(audio[f"smail_{language}_{button_name}"])
    # Plays the loaded audio.
    pygame.mixer.music.play()


def button_hover(button, button_name, enter_time):
    # Function is called when the mouse cursor hovers over a button.
    language, audio, timer = getAudio()
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
