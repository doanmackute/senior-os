import tkinter as tk
from tkinter import ttk
from style import font_config, button_config
from mail_connection import sendEmail, readMail

class defaultFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.currentFrame = readMailFrame(self)
        self.pack()

    # switching frames
    def showWriteMailFrame(self):
        self.currentFrame.forget()
        self.currentFrame = writeMailFrame(self)

    def showReadMailFrame(self):
        self.currentFrame.forget()
        self.currentFrame = readMailFrame(self)
class readMailFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # grid configuration
        self.columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.rowconfigure((0, 1, 2), weight=1, uniform="a")
        self.createWidgets()
        self.pack()

    def createWidgets(self):
        # widgets for reading an email
        self.inboxLabel = ttk.Label(self, text="Inbox: ", font=font_config())
        self.inboxList = tk.Listbox(self, font=font_config(), height=15, width=40, activestyle="none", selectmode=tk.SINGLE)
        self.textArea = tk.Text(self, font=font_config(), height=15, borderwidth=1, relief=tk.SUNKEN, state="disabled")

        self.inboxLabel.grid(row=0, column=0, sticky="nsew", padx=10, ipady=50)
        self.inboxList.grid(row=1, column=0, sticky="new", padx=20, pady=20, rowspan=2)
        self.textArea.grid(row=1, rowspan=2, column=1, columnspan=2, padx=20, pady=20, sticky="new")

        self.insertEmails()

    def insertEmails(self):

        self.emails = readMail()

        for n in self.emails:
            self.inboxList.insert(tk.END, n.split("From:")[0])
            # binding listbox to text area to view email
            self.inboxList.bind("<<ListboxSelect>>", self.showEmail)
    def showEmail(self, event):
        selectedIndex = self.inboxList.curselection()[0]
        selectedEmail = self.emails[selectedIndex]
        self.textArea.configure(state="normal")
        self.textArea.delete("1.0", tk.END)
        self.textArea.insert(tk.END, selectedEmail)
        self.textArea.configure(state="disabled")
class writeMailFrame(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        # grid configuration
        self.columnconfigure((0, 1, 2), weight=2, uniform="a")
        self.columnconfigure((3,4), weight=1, uniform="a")
        self.rowconfigure((0, 1), weight=1, uniform="a")
        self.rowconfigure(2, weight=3, uniform="a")
        self.rowconfigure(3, weight=2, uniform="a")
        self.createWidgets()
        self.pack(side="left")

    def createWidgets(self):
        # widgets for writing an email
        self.recipientLabel = ttk.Label(self, text="To: ", font=font_config())
        self.subjectLabel = ttk.Label(self, text="Subject: ", font=font_config())
        self.contentLabel = ttk.Label(self, text="Message: ", font=font_config())
        self.recipientEntry = ttk.Entry(self, font=font_config())
        self.subjectEntry = ttk.Entry(self, font=font_config())
        self.contentEntry = tk.Text(self, font=font_config())
        self.sendMailButton = ttk.Button(self, text="Send email", style=button_config(), command=self.sendMail)

        self.recipientLabel.grid(row=0, column=1, sticky="e", padx=10, pady=10, ipady=50)
        self.recipientEntry.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        self.subjectLabel.grid(row=1, column=1, sticky="e", padx=10, pady=10)
        self.subjectEntry.grid(row=1, column=2, sticky="nsew", padx=10,pady=10)
        self.contentLabel.grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.contentEntry.grid(row=2, column=1, columnspan = 3, padx=10, pady=10)
        self.sendMailButton.grid(row=3, column=1, columnspan=3, sticky="nsew", pady=10, padx=10)

    def sendMail(self):

        succ = sendEmail(self.recipientEntry.get(), self.subjectEntry.get(), self.contentEntry.get("1.0", tk.END))

        if succ == 1:
            self.recipientEntry.delete(0, tk.END)
            self.subjectEntry.delete(0, tk.END)
            self.contentEntry.delete("1.0", tk.END)
        else:
            print("Error occured when trying to send email. Check your email and password.", succ)


