import tkinter as tk
from tkinter import ttk, scrolledtext
from smail.config.style import (font_config, button_config, search_mail,
                                getLanguage, button_hover, button_leave)
from smail.config.mail_connection import sendEmail, readMail, checkEmailForSpam
from smail.template import guiTemplate as temp


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
        self.inboxLabel = ttk.Label(
            self, text="Inbox: ", font=font_config()
        )
        self.inboxList = tk.Listbox(
            self, font=font_config(), height=15, width=40,
            activestyle="none", selectmode=tk.SINGLE
        )
        self.textArea = tk.Text(
            self, font=font_config(), height=15, borderwidth=1,
            relief=tk.SUNKEN, state="disabled"
        )

        self.inboxLabel.grid(
            row=0, column=0,
            sticky="nsew", padx=10, ipady=50
        )
        self.inboxList.grid(
            row=1, column=0, rowspan=2,
            sticky="new", padx=20, pady=20
        )
        self.textArea.grid(
            row=1, rowspan=2, column=1, columnspan=2,
            sticky="new", padx=20, pady=20
        )

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


class writeMailFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        # grid configuration
        self.columnconfigure((0, 1, 2), weight=2, uniform="a")
        self.columnconfigure((3, 4), weight=1, uniform="a")
        self.rowconfigure((0, 1), weight=1, uniform="a")
        self.rowconfigure(2, weight=3, uniform="a")
        self.rowconfigure(3, weight=2, uniform="a")
        self.createWidgets()
        self.pack(side="left")

    def createWidgets(self):
        # widgets for writing an email
        self.recipientLabel = ttk.Label(
            self, text="To: ", font=font_config()
        )
        self.subjectLabel = ttk.Label(
            self, text="Subject: ", font=font_config()
        )
        self.contentLabel = ttk.Label(
            self, text="Message: ", font=font_config()
        )
        self.recipientEntry = ttk.Entry(
            self, font=font_config()
        )
        self.subjectEntry = ttk.Entry(
            self, font=font_config()
        )
        self.contentEntry = tk.Text(
            self, font=font_config()
        )
        self.sendMailButton = ttk.Button(
            self, text="Send email", style=button_config(),
            command=self.sendMail
        )

        self.recipientLabel.grid(
            row=0, column=1,
            sticky="e", padx=10, pady=10, ipady=50
        )
        self.recipientEntry.grid(
            row=0, column=2,
            sticky="nsew", padx=10, pady=10
        )
        self.subjectLabel.grid(
            row=1, column=1,
            sticky="e", padx=10, pady=10
        )
        self.subjectEntry.grid(
            row=1, column=2,
            sticky="nsew", padx=10, pady=10
        )
        self.contentLabel.grid(
            row=2, column=0,
            sticky="e", padx=10, pady=10
        )
        self.contentEntry.grid(
            row=2, column=1, columnspan=3,
            padx=10, pady=10)
        self.sendMailButton.grid(
            row=3, column=1, columnspan=3,
            sticky="nsew", pady=10, padx=10
        )

    def getRecipientEntry(self):
        return self.recipientEntry

    def sendMail(self):

        succ = sendEmail(
            self.recipientEntry.get(), self.subjectEntry.get(),
            self.contentEntry.get("1.0", tk.END)
        )

        if succ == 1:
            self.recipientEntry.delete(0, tk.END)
            self.subjectEntry.delete(0, tk.END)
            self.contentEntry.delete("1.0", tk.END)
        else:
            print("Error occurred when trying to send email. "
                  "Check your email and password.", succ)


class oneFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.menu = temp.App(parent)
        # import buttons from GUI template
        self.redefineTemplateButtons()
        self.language, self.text = getLanguage()
        # grid configuration
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=3, uniform="a")
        self.lFrame = self.leftFrame()
        self.rFrame = self.rightWriteFrame()
        self.lFrame.grid(
            column=0
        )
        self.rFrame.grid(
            column=1, row=0
        )
        self.pack()

    def leftFrame(self):
        self.frame = tk.Frame(self)
        self.frame.columnconfigure(0, weight=1, uniform="a")
        self.frame.rowconfigure(0, weight=1, uniform="a")
        self.inboxLabel = tk.Label(
            self.frame, text=self.text[f"smail_{self.language}_inboxLabel"],
            font=font_config()
        )
        self.inboxList = tk.Listbox(
            self.frame, font=font_config(), height=13, width=40,
            activestyle="none", selectmode=tk.SINGLE
        )
        self.inboxLabel.grid(
            row=0, column=0,
            sticky="nsew", padx=10, pady=10, ipady=5
        )
        self.inboxList.grid(
            row=1, column=0,
            sticky="nsew", padx=20, pady=20
        )
        self.insertEmails()

        return self.frame

    def insertEmails(self):

        try:
            self.emails = readMail()
            try:
                self.safe_emails = checkEmailForSpam(self.emails)
                for n in self.safe_emails:
                    self.inboxList.insert(tk.END, n.split("From:")[0])
                    # binding listbox to text area to view email
                    self.inboxList.bind("<<ListboxSelect>>", self.showEmail)
            except Exception as error:
                print("Failed to apply anti-phishing filters. "
                      "Omitting security steps. ", error)
                self.safe_emails = self.emails
                for n in self.emails:
                    self.inboxList.insert(tk.END, n.split("From:")[0])
                    # binding listbox to text area to view email
                    self.inboxList.bind("<<ListboxSelect>>", self.showEmail)
        except Exception as error:
            print("Error when trying to fill in the listbox. ", error)

    def showEmail(self, event):
        # switch frames
        self.switchToReadingMail()

        if not self.inboxList.curselection():
            # If no selection, use the last selected email
            if (self.lastSelectedIndex is not None
                    and self.lastSelectedEmail is not None):
                self.messageArea.configure(state="normal")
                self.messageArea.delete("1.0", tk.END)
                self.messageArea.insert(tk.END, self.lastSelectedEmail)
                self.messageArea.configure(state="disabled")
            return

        self.selectedIndex = self.inboxList.curselection()[0]
        selectedEmail = self.safe_emails[self.selectedIndex]
        self.messageArea.configure(state="normal")
        self.messageArea.delete("1.0", tk.END)
        self.messageArea.insert(tk.END, selectedEmail)
        self.messageArea.configure(state="disabled")

        # Update the last selected index and email
        self.lastSelectedIndex = self.selectedIndex
        self.lastSelectedEmail = selectedEmail

    def switchToReadingMail(self):
        self.rFrame = self.rightReadFrame()
        self.rFrame.grid(
            column=1, row=0
        )
        self.pack()

    def switchToWriteMail(self):
        self.rFrame = self.rightWriteFrame()
        self.rFrame.grid(
            column=1, row=0
        )
        self.pack()
        return self.recipientEntry

    def rightWriteFrame(self):
        self.rframe = tk.Frame(self)
        self.rframe.columnconfigure((0, 1), weight=1, uniform="a")
        self.rframe.rowconfigure((0, 1, 2, 4), weight=1, uniform="a")
        self.rframe.rowconfigure(3, weight=2, uniform="a")
        self.recipientLabel = tk.Label(
            self.rframe,
            text=self.text[f"smail_{self.language}_recipientLabel"],
            font=font_config()
        )
        self.subjectLabel = tk.Label(
            self.rframe,
            text=self.text[f"smail_{self.language}_subjectLabel"],
            font=font_config()
        )
        self.contentLabel = tk.Label(
            self.rframe,
            text=self.text[f"smail_{self.language}_messageLabel"],
            font=font_config()
        )
        self.recipientEntry = tk.Entry(
            self.rframe, font=font_config()
        )
        self.subjectEntry = tk.Entry(
            self.rframe, font=font_config()
        )
        self.contentEntry = scrolledtext.ScrolledText(
            self.rframe, font=font_config(), height=10
        )
        # widget placement
        self.recipientLabel.grid(
            row=0, column=0,
            sticky="nse", padx=10, pady=10
        )
        self.subjectLabel.grid(
            row=1, column=0,
            sticky="nse", padx=10, pady=10
        )
        self.contentLabel.grid(
            row=2, column=0,
            sticky="nsw", padx=10, pady=10
        )
        self.recipientEntry.grid(
            row=0, column=1,
            sticky="nsew", padx=10, pady=10
        )
        self.subjectEntry.grid(
            row=1, column=1,
            sticky="nsew", padx=10, pady=10
        )
        self.contentEntry.grid(
            row=3, column=0, columnspan=2, rowspan=2,
            padx=10, pady=10, ipady=10, sticky="new"
        )
        return self.rframe

    def rightReadFrame(self):
        self.rrframe = tk.Frame(self)
        self.rrframe.columnconfigure(0, weight=2, uniform="a")
        self.rrframe.rowconfigure(0, weight=1, uniform="a")
        self.messageLabel = tk.Label(
            self.rrframe,
            text=self.text[f"smail_{self.language}_messageLabel"],
            font=font_config()
        )
        self.messageArea = scrolledtext.ScrolledText(
            self.rrframe, font=font_config(), height=13
        )
        self.messageLabel.grid(
            row=0, column=0, ipady=5,
            sticky="nsew", padx=10, pady=10
        )
        self.messageArea.grid(
            row=1, column=0,
            sticky="nsew", padx=20, pady=20
        )
        return self.rrframe

    def getRecipientEntry(self):
        return self.recipientEntry

    def sendMail(self):

        succ = sendEmail(
            self.recipientEntry.get(), self.subjectEntry.get(),
            self.contentEntry.get("1.0", tk.END)
        )

        if succ == 1:
            self.recipientEntry.delete(0, tk.END)
            self.subjectEntry.delete(0, tk.END)
            self.contentEntry.delete("1.0", tk.END)
        else:
            print("Error occurred when trying to send email. "
                  "Check your email and password.", succ)

    def redefineTemplateButtons(self):

        self.options_buttons_crt1 = (
            self.menu.menuFrameCreateButtonsVal.optButtons1
        )
        self.options_buttons_crt2 = (
            self.menu.menuFrameCreateButtonsVal.optButtons2
        )
        self.exitButton = self.options_buttons_crt1.button_dict[1]
        self.audioConfigure(self.exitButton, "exitButton")
        self.sendEmailButton = self.options_buttons_crt1.button_dict[2]
        self.audioConfigure(self.sendEmailButton, "sendEmailButton")
        self.sendMailPerson1 = self.options_buttons_crt1.button_dict[3]
        self.audioConfigure(self.sendMailPerson1, "person1")
        self.sendMailPerson2 = self.options_buttons_crt1.button_dict[4]
        self.audioConfigure(self.sendMailPerson2, "person2")
        self.sendMailPerson3 = self.options_buttons_crt2.button_dict[1]
        self.audioConfigure(self.sendMailPerson3, "person3")
        self.sendMailPerson4 = self.options_buttons_crt2.button_dict[2]
        self.audioConfigure(self.sendMailPerson4, "person4")
        self.sendMailPerson5 = self.options_buttons_crt2.button_dict[3]
        self.audioConfigure(self.sendMailPerson5, "person5")
        self.sendMailTo = self.options_buttons_crt2.button_dict[4]
        self.audioConfigure(self.sendMailTo, "sendToButton")

        self.sendEmailButton.config(
            command=self.sendMail,
        )
        self.sendMailPerson1.config(
            command=lambda: self.fillRecipient(1),
        )
        self.sendMailPerson2.config(
            command=lambda: self.fillRecipient(2),
        )
        self.sendMailPerson3.config(
            command=lambda: self.fillRecipient(3),
        )
        self.sendMailPerson4.config(
            command=lambda: self.fillRecipient(4),
        )
        self.sendMailPerson5.config(
            command=lambda: self.fillRecipient(5),
        )
        self.sendMailTo.config(
            command=self.switchToWriteMail,
        )

    def fillRecipient(self, id):
        email = search_mail(id)
        recipient = self.switchToWriteMail()
        recipient.delete(0, tk.END)
        recipient.insert(0, email)
        recipient.configure(state="disabled")

    def audioConfigure(self, button, button_name):
        enter_time = [None]
        # This event is triggered when the mouse cursor enters the button.
        button.bind("<Enter>",
                    lambda event, name=button_name,
                    et=enter_time: button_hover(button, name, et)
                    )
        # This event is triggered when the mouse cursor leaves the button.
        button.bind("<Leave>",
                    lambda event, et=enter_time: button_leave(button, et)
                    )
