import logging
import threading
import tkinter as tk
from tkinter import scrolledtext
from smail.connection.style import (font_config, search_mail,
                                    getLanguage, button_hover, button_leave, images, imageConfig, app_color, height_config)
from smail.connection.mail_connection import sendEmail, readMail, checkEmailForSpam
from demo.guiTemplate import guiTemplate as temp
from demo.guiTemplate import configActions as act

logger = logging.getLogger(__file__)


class oneFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # background color
        self.background_color = app_color()
        self.configure(bg=self.background_color)

        # initiate logging
        logger.info("Initiated logging.")
        self.menu = temp.App(parent)

        # import buttons from GUI template
        self.redefineTemplateButtons()
        self.button_state = None

        # number of displayed lines in textarea and listbox
        self.number_of_lines_listbox, self.number_of_lines_textarea = height_config(self)

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

        # Start a background thread to load emails
        self.loadingEmails = threading.Thread(target=self.loadEmails)
        self.loadingEmails.start()

    def loadEmails(self):
        self.insertEmails()

    def redefineTemplateButtons(self):
        try:
            # width configuration
            self.sixHeight = temp.resolutionMath()[2]
            self.sixWidth = temp.resolutionMath()[1]
            numOPT = act.jsonRed('buttons_info', "num_of_opt_on_frame")
            padxValue = act.jsonRed('buttons_info', "padx_value")
            self.buttonWidth = int(self.sixWidth - (padxValue * numOPT))

            # language configuration
            self.language, self.text = getLanguage()

            # image configuration
            self.img = images()
            self.exitImage = tk.PhotoImage(file=self.img["exit"])
            self.person1Image = imageConfig("Person1", self.sixHeight)
            self.person2Image = imageConfig("Person2", self.sixHeight)
            self.person3Image = imageConfig("Person3", self.sixHeight)
            self.person4Image = imageConfig("Person4", self.sixHeight)
            self.person5Image = imageConfig("Person5", self.sixHeight)
        except Exception:
            logger.error("Failed loading language and images")

        try:
            # access menu 1
            self.options_buttons_crt1 = (
                self.menu.menuFrameCreateButtonsVal.optButtons1
            )

            # access menu 2
            self.options_buttons_crt2 = (
                self.menu.menuFrameCreateButtonsVal.optButtons2
            )

            # saving buttons to local variables
            self.exitButton = self.options_buttons_crt1.button_dict[1]
            self.sendEmailButton = self.options_buttons_crt1.button_dict[2]
            self.sendMailPerson1 = self.options_buttons_crt1.button_dict[3]
            self.sendMailPerson2 = self.options_buttons_crt1.button_dict[4]
            self.sendMailPerson3 = self.options_buttons_crt2.button_dict[1]
            self.sendMailPerson4 = self.options_buttons_crt2.button_dict[2]
            self.sendMailPerson5 = self.options_buttons_crt2.button_dict[3]
            self.sendMailTo = self.options_buttons_crt2.button_dict[4]
            self.menu_button_1 = self.menu.menuFrameCreateButtonsVal.button_dict[1]
            self.menu_button_2 = self.menu.menuFrameCreateButtonsVal.button_dict[2]

            # audio configuration buttons
            self.audioConfigure(self.exitButton, "exitButton")
            self.audioConfigure(self.sendEmailButton, "sendEmailButton")
            self.audioConfigure(self.sendMailPerson1, "person1")
            self.audioConfigure(self.sendMailPerson2, "person2")
            self.audioConfigure(self.sendMailPerson3, "person3")
            self.audioConfigure(self.sendMailPerson4, "person4")
            self.audioConfigure(self.sendMailPerson5, "person5")
            self.audioConfigure(self.sendMailTo, "sendToButton")
            self.audioConfigure(self.menu_button_1, "menu1")
            self.audioConfigure(self.menu_button_2, "menu2")

            self.exitButton.config(
                image=self.exitImage,
                text="",
                width=self.buttonWidth

            )
            self.sendEmailButton.config(
                text = "",
                width=self.buttonWidth

                # command=self.sendMail,
            )
            self.sendMailPerson1.config(
                command=lambda: self.fillRecipient(1),
                image=self.person1Image,
                text="",
                width=self.buttonWidth
            )
            self.sendMailPerson2.config(
                command=lambda: self.fillRecipient(2),
                image=self.person2Image,
                text="",
                width=self.buttonWidth
            )
            self.sendMailPerson3.config(
                command=lambda: self.fillRecipient(3),
                image=self.person3Image,
                text="",
                width=self.buttonWidth
            )
            self.sendMailPerson4.config(
                command=lambda: self.fillRecipient(4),
                image=self.person4Image,
                text="",
                width=self.buttonWidth
            )
            self.sendMailPerson5.config(
                command=lambda: self.fillRecipient(5),
                image=self.person5Image,
                text="",
                width=self.buttonWidth
            )
            self.sendMailTo.config(
                command=lambda: self.fillRecipient(0),
                text=self.text[f"smail_{self.language}_sendToButton"],
                width=self.buttonWidth
            )
            logger.info("Buttons successfully redefined.")
        except AttributeError:
            logger.error("AttributeError:", exc_info=True)
        except KeyError:
            logger.error("KeyError:", exc_info=True)
        except Exception:
            logger.error("Error:", exc_info=True)

    def leftFrame(self):

        self.frame = tk.Frame(self)
        self.frame.configure(bg=self.background_color)
        self.frame.columnconfigure(0, weight=1, uniform="a")
        self.frame.rowconfigure(0, weight=1, uniform="a")
        self.inboxLabel = tk.Label(
            self.frame, text=self.text[f"smail_{self.language}_inboxLabel"],
            font=font_config(), bg=self.background_color
        )
        self.inboxList = tk.Listbox(
            self.frame, font=font_config(), height=self.number_of_lines_listbox,
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

        self.audioConfigure(self.inboxList, "inbox")

        logger.info("Created left frame with received emails in listbox.")
        return self.frame

    def rightWriteFrame(self):
        self.rwframe = tk.Frame(self)
        self.rwframe.configure(bg=self.background_color)
        self.rwframe.columnconfigure((0, 1), weight=1, uniform="a")
        self.rwframe.rowconfigure((0, 1, 2, 4), weight=1, uniform="a")
        self.rwframe.rowconfigure(3, weight=2, uniform="a")
        self.recipientLabel = tk.Label(
            self.rwframe,
            text=self.text[f"smail_{self.language}_recipientLabel"],
            font=font_config(), bg=self.background_color
        )
        self.subjectLabel = tk.Label(
            self.rwframe,
            text=self.text[f"smail_{self.language}_subjectLabel"],
            font=font_config(), bg=self.background_color
        )
        self.contentLabel = tk.Label(
            self.rwframe,
            text=self.text[f"smail_{self.language}_messageLabel"],
            font=font_config(), background=self.background_color
        )
        self.recipientEntry = tk.Entry(
            self.rwframe, font=font_config()
        )
        self.subjectEntry = tk.Entry(
            self.rwframe, font=font_config()
        )
        self.contentEntry = scrolledtext.ScrolledText(
            self.rwframe, font=font_config(), height=self.number_of_lines_textarea
        )

        # audio configuration
        self.audioConfigure(self.recipientEntry,"recipient")
        self.audioConfigure(self.subjectEntry, "subject")
        self.audioConfigure(self.contentEntry, "write_message")

        # widget placement
        self.recipientLabel.grid(
            row=0, column=0,
            sticky="e", padx=10, pady=10
        )
        self.subjectLabel.grid(
            row=1, column=0,
            sticky="e", padx=10, pady=10
        )
        self.contentLabel.grid(
            row=2, column=0,
            sticky="w", padx=10, pady=10
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

        return self.rwframe

    def rightReadFrame(self):
        self.rrframe = tk.Frame(self)
        self.rrframe.configure(bg=self.background_color)
        self.rrframe.columnconfigure(0, weight=2, uniform="a")
        self.rrframe.rowconfigure(0, weight=1, uniform="a")
        self.messageLabel = tk.Label(
            self.rrframe,
            text=self.text[f"smail_{self.language}_messageLabel"],
            font=font_config(), bg=self.background_color
        )
        self.messageArea = scrolledtext.ScrolledText(
            self.rrframe, font=font_config(), height=self.number_of_lines_listbox
        )

        # audio configuration
        self.audioConfigure(self.messageArea, "read_message")


        # grid configuration
        self.messageLabel.grid(
            row=0, column=0, ipady=5,
            sticky="nsew", padx=10, pady=10
        )
        self.messageArea.grid(
            row=1, column=0,
            sticky="nsew", padx=20, pady=20
        )

        return self.rrframe

    def insertEmails(self):

        try:
            self.emails = readMail()
            try:
                self.safe_emails = checkEmailForSpam(self.emails)
                for n in self.safe_emails:
                    self.inboxList.insert(tk.END, n.split("From:")[0])
                    # binding listbox to text area to view email
                    self.inboxList.bind("<<ListboxSelect>>", self.showEmail)
                logger.info("Anti-phishing filters applied.")
            except Exception:
                logger.critical("Failed to apply anti-phishing filters."
                                "Omitting security steps.", exc_info=True)
                self.safe_emails = self.emails
                for n in self.emails:
                    self.inboxList.insert(tk.END, n.split("From:")[0])
                    # binding listbox to text area to view email
                    self.inboxList.bind("<<ListboxSelect>>", self.showEmail)
        except Exception:
            logger.error("Error when trying to fill in the listbox. ",
                         exc_info=True)

    def showEmail(self, event):
        # switch frames
        self.switchToReadingMail()

        if not self.inboxList.curselection():
            # If no selection, use the last selected email
            if (self.lastSelectedIndex is not None
                    and self.lastSelectedEmail is not None):
                self.configureMessageArea(self.lastSelectedEmail)

        selectedIndex = self.inboxList.curselection()[0]
        selectedEmail = self.safe_emails[selectedIndex]
        self.configureMessageArea(selectedEmail)

        # Update the last selected index and email
        self.lastSelectedIndex = selectedIndex
        self.lastSelectedEmail = selectedEmail

    def configureMessageArea(self, email):
        self.messageArea.configure(state="normal")
        self.messageArea.delete("1.0", tk.END)
        self.messageArea.insert(tk.END, email)
        self.messageArea.configure(state="disabled")

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

    def getRecipientEntry(self):
        return self.recipientEntry

    def sendEmailStatus(self):

        succ = sendEmail(
            self.recipientEntry.get(), self.subjectEntry.get(),
            self.contentEntry.get("1.0", tk.END)
        )

        # this logging in mail_connection.py
        if succ == 1:
            logger.info(f"Email successfully sent to "
                        f"{self.recipientEntry.get()}.")
            self.recipientEntry.delete(0, tk.END)
            self.subjectEntry.delete(0, tk.END)
            self.contentEntry.delete("1.0", tk.END)
        # else:
        #     logger.error("Error occurred when trying to send email."
        #                   "Check email and password configuration.")
        #     # print("Error occurred when trying to send email. "
        #     #       "Check email and password configuration.", succ)

    def fillRecipient(self, id):
        # if every Entry obtains text, message will be sent
        # when pressing Person[id] button for the second time.
        if (self.recipientEntry.get() and self.subjectEntry.get() and
                self.contentEntry.get("1.0", tk.END).strip() and
                id == self.button_state):
            self.sendEmailStatus()

        # if another Person[id] button is pressed,
        # Entries will be deleted,
        # new recipient entry will be filled in.
        elif (self.subjectEntry.get() or
              self.contentEntry.get("1.0", tk.END).strip()):
            if id != self.button_state:
                print("No content to send.")
                email = search_mail(id)
                recipient = self.switchToWriteMail()
                recipient.delete(0, tk.END)
                recipient.insert(0, email)
                recipient.configure(state="disabled")
            # if Person[id] button is pressed for the second time,
            # but one of the entry is not filled in, nothing will happen
            else:
                print("one of the entries is not filled in.")

        else:
            # if Send To button is pressed, frame is switched and
            # recipient entry is deleted.
            if id == 0:
                print("Send To button pressed")
                recipient = self.switchToWriteMail()
                recipient.delete(0, tk.END)
            # if Person[id] button is pressed for the second time,
            # but none of the entry is filled in.
            else:
                print("Button pressed for the second time,"
                      " no entry is filled in.")
                email = search_mail(id)
                recipient = self.switchToWriteMail()
                recipient.delete(0, tk.END)
                recipient.insert(0, email)
                recipient.configure(state="disabled")

        self.button_state = id

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
