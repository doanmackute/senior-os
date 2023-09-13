'''
Author : Tarik Alkanan 
'''
import json
from setConstant import *
import os
# change dir to /home/srun
os.chdir("/home/srun")
path = os.getcwd()
# read the Json file
file_json = open(path + '/Constants.json')
loaded_file = json.load(file_json)

if COLORFUL == True:

    SWEB_ACTIVEBACKGROUND = loaded_file["C_SWEB_ACTIVEBACKGROUND"] 
    STEXT_ACTIVEBACKGROUND = loaded_file["C_STEXT_ACTIVEBACKGROUND"]
    SMAIL_ACTIVEBACKGROUND = loaded_file["C_SMAIL_ACTIVEBACKGROUND"] 
    SHUTDOWN_ACTIVEBACKGROUND = loaded_file["C_SHUTDOWN_ACTIVEBACKGROUND"]
    CANCEL_ACTIVEBACKGROUND = loaded_file["C_CANCEL_ACTIVEBACKGROUND"]

    SWEB_BACKGROUND = loaded_file["C_SWEB_BACKGROUND"] 
    STEXT_BACKGROUND = loaded_file["C_STEXT_BACKGROUND"] 
    SMAIL_BACKGROUND = loaded_file["C_SMAIL_BACKGROUND"] 
    SHUTDOWN_BACKGROUND = loaded_file["C_SHUTDOWN_BACKGROUND"] 
    CANCEL_BACKGROUND = loaded_file["C_CANCEL_BACKGROUND"] 

    SWEB_IMG = path + loaded_file["C_SWEB_IMG"]
    STEXT_IMG = path + loaded_file["C_STEXT_IMG"]
    SMAIL_IMG = path + loaded_file["C_SMAIL_IMG"]
    SHUTDOWN_IMG = path + loaded_file["C_SHUTDOWN_IMG"]
    CANCEL_IMG = path + loaded_file["C_CANCEL_IMG"]
else:

    SWEB_ACTIVEBACKGROUND = loaded_file["B_SWEB_ACTIVEBACKGROUND"] 
    STEXT_ACTIVEBACKGROUND = loaded_file["B_STEXT_ACTIVEBACKGROUND"]
    SMAIL_ACTIVEBACKGROUND = loaded_file["B_SMAIL_ACTIVEBACKGROUND"] 
    SHUTDOWN_ACTIVEBACKGROUND = loaded_file["B_SHUTDOWN_ACTIVEBACKGROUND"]
    CANCEL_ACTIVEBACKGROUND = loaded_file["B_CANCEL_ACTIVEBACKGROUND"]

    SWEB_BACKGROUND = loaded_file["B_SWEB_BACKGROUND"] 
    STEXT_BACKGROUND = loaded_file["B_STEXT_BACKGROUND"] 
    SMAIL_BACKGROUND = loaded_file["B_SMAIL_BACKGROUND"] 
    SHUTDOWN_BACKGROUND = loaded_file["B_SHUTDOWN_BACKGROUND"] 
    CANCEL_BACKGROUND = loaded_file["B_CANCEL_BACKGROUND"] 

    SWEB_IMG = path + loaded_file["B_SWEB_IMG"]
    STEXT_IMG = path + loaded_file["B_STEXT_IMG"]
    SMAIL_IMG = path + loaded_file["B_SMAIL_IMG"]
    SHUTDOWN_IMG = path + loaded_file["B_SHUTDOWN_IMG"]
    CANCEL_IMG = path + loaded_file["B_CANCEL_IMG"]

if LANGUAGE == True:
    SWEB_WAV = path + loaded_file["CZ_SWEB_WAV"]
    STEXT_WAV = path + loaded_file["CZ_STEXT_WAV"]
    SMAIL_WAV = path + loaded_file["CZ_SMAIL_WAV"]
    SHUTDOWN_WAV = path + loaded_file["CZ_SHUTDOWN_WAV"]
    CANCEL_WAV = path + loaded_file["CZ_CANCEL_WAV"]
else:
    SWEB_WAV = path + loaded_file["EN_SWEB_WAV"]
    STEXT_WAV = path + loaded_file["EN_STEXT_WAV"]
    SMAIL_WAV = path + loaded_file["EN_SMAIL_WAV"]
    SHUTDOWN_WAV = path + loaded_file["EN_SHUTDOWN_WAV"]
    CANCEL_WAV = path + loaded_file["EN_CANCEL_WAV"]

