from tkinter import *
window = Tk()

screen_width = window.winfo_screenwidth()          ##get screen width
screen_height= window.winfo_screenheight()  
window.geometry("%dx%d" % (screen_width,screen_height))   
window.attributes('-fullscreen',True)
window.resizable(0,0)


messageLab = Label(window,text="Unfortunately, the work on the smail app has not been completed yet!!",font=('Times', 28))

closeButton=Button(window,text="Close",font=('Times', 25),
                        bd=1,overrelief = SUNKEN,
                        command=window.destroy) 
messageLab.pack(pady = 50)
closeButton.pack()


window.mainloop()
