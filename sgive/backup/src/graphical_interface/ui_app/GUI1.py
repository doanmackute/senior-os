# Import the required Libraries
from tkinter import *
from tkinter import ttk

win = Tk()
win.geometry("750x250")
# Define a function to update the entry widget

# ryu autismus zacina zde :)-----------------------------------------------------
# program by mel pri stisknuti menu tlacitka prohodit ty tlacitka na dalsi a pri back zas o jedno zpe :)

def menu_action_up(text):  # pohyb z menu_x na menu_x+1
    #print(f"##OPT_MENU_THING:{opt_acit[value]}")
    if not text >= 4:  # hradlo, aby to nezmizelo

        button_dict[text].pack_forget()
        button_dict[text + 1].pack()


button_dict = {}
option = [1, 2, 3, 4, 5]  # v budoucnu načteno z conf.json i hope

for i in option:
    value = 0
    def func(x=i):
        global value
        value = x
        return menu_action_up(x)
    def menu_action_back():  # vraci menu_x na menu_x-1
        global value
        if value == 4:
            #print(f"OPT_MENU_THING:{opt_acit[value-1]}")
            button_dict[value].pack_forget()
            button_dict[value - 1].pack()
            value = value - 2
        elif value == 0:
            return
        else:
            button_dict[value + 1].pack_forget()
            button_dict[value].pack()
            value = value - 1


    if (i == 5):  # vytvoreni back tlacitka (davam jako posledni aby to bylo prehledne)
        button_dict[i] = ttk.Button(win, text=f"back{i}", command=menu_action_back)
    else:  # vytvoreni menu tlacitek
        button_dict[i] = ttk.Button(win, text=f"menu{i}", command=func)

button_dict[5].pack()  # back
button_dict[1].pack()  # menu_1
#print(f"OPT_MENU_THING:{opt_acit[1]}")
win.mainloop()
