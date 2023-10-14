import logging
import threading
import tkinter as tk
from tkinter import scrolledtext
from smail.connection.style import (font_config, search_mail,
                                    get_language, button_hover, button_leave, images, image_config, app_color, height_config)
from smail.connection.mail_connection import send_email, read_mail, check_email_for_spam
from demo.guiTemplate import guiTemplate as temp
from demo.guiTemplate import configActions as act

logger = logging.getLogger(__file__)


class one_frame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # background color
        self.background_color = app_color()
        self.configure(bg=self.background_color)

        # initiate logging
        logger.info("Initiated logging.")
        self.menu = temp.App(parent)

        # import buttons from GUI template
        self.redefine_template_buttons()
        self.button_state = None

        # number of displayed lines in textarea and listbox
        self.number_of_lines_listbox, self.number_of_lines_textarea = height_config(self)

        # grid configuration
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=3, uniform="a")
        self.l_frame = self.left_frame()
        self.r_frame = self.right_read_frame()

        self.l_frame.grid(
            column=0
        )
        self.r_frame.grid(
            column=1, row=0
        )
        self.pack()

        # Start a background thread to load emails
        self.loading_emails = threading.Thread(target=self.load_emails)
        self.loading_emails.start()

    def load_emails(self):
        self.insert_emails()

    def redefine_template_buttons(self):
        try:
            # width configuration
            self.six_height = temp.resolutionMath()[2]
            self.six_width = temp.resolutionMath()[1]
            num_opt = act.jsonRed('buttons_info', "num_of_opt_on_frame")
            padx_value = act.jsonRed('buttons_info', "padx_value")
            self.button_width = int(self.six_width - (padx_value * num_opt))

            # language configuration
            self.language, self.text = get_language()

            # image configuration
            self.img = images()
            self.exit_image = tk.PhotoImage(file=self.img["exit"])
            self.person1_image = image_config("Person1", self.six_height)
            self.person2_image = image_config("Person2", self.six_height)
            self.person3_image = image_config("Person3", self.six_height)
            self.person4_image = image_config("Person4", self.six_height)
            self.person5_image = image_config("Person5", self.six_height)
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
            self.exit_button = self.options_buttons_crt1.button_dict[1]
            self.send_email_button = self.options_buttons_crt1.button_dict[2]
            self.send_mail_person1 = self.options_buttons_crt1.button_dict[3]
            self.send_mail_person2 = self.options_buttons_crt1.button_dict[4]
            self.send_mail_person3 = self.options_buttons_crt2.button_dict[1]
            self.send_mail_person4 = self.options_buttons_crt2.button_dict[2]
            self.send_mail_person5 = self.options_buttons_crt2.button_dict[3]
            self.send_mail_to = self.options_buttons_crt2.button_dict[4]
            self.menu_button_1 = self.menu.menuFrameCreateButtonsVal.button_dict[1]
            self.menu_button_2 = self.menu.menuFrameCreateButtonsVal.button_dict[2]

            # audio configuration buttons
            self.audioConfigure(self.exit_button, "exitButton")
            self.audioConfigure(self.send_email_button, "sendEmailButton")
            self.audioConfigure(self.send_mail_person1, "person1")
            self.audioConfigure(self.send_mail_person2, "person2")
            self.audioConfigure(self.send_mail_person3, "person3")
            self.audioConfigure(self.send_mail_person4, "person4")
            self.audioConfigure(self.send_mail_person5, "person5")
            self.audioConfigure(self.send_mail_to, "sendToButton")
            self.audioConfigure(self.menu_button_1, "menu1")
            self.audioConfigure(self.menu_button_2, "menu2")

            self.exit_button.config(
                image=self.exit_image,
                text="",
                width=self.button_width

            )
            self.send_email_button.config(
                text = "",
                width=self.button_width

                # command=self.sendMail,
            )
            self.send_mail_person1.config(
                command=lambda: self.fillRecipient(1),
                image=self.person1_image,
                text="",
                width=self.button_width
            )
            self.send_mail_person2.config(
                command=lambda: self.fillRecipient(2),
                image=self.person2_image,
                text="",
                width=self.button_width
            )
            self.send_mail_person3.config(
                command=lambda: self.fillRecipient(3),
                image=self.person3_image,
                text="",
                width=self.button_width
            )
            self.send_mail_person4.config(
                command=lambda: self.fillRecipient(4),
                image=self.person4_image,
                text="",
                width=self.button_width
            )
            self.send_mail_person5.config(
                command=lambda: self.fillRecipient(5),
                image=self.person5_image,
                text="",
                width=self.button_width
            )
            self.send_mail_to.config(
                command=lambda: self.fillRecipient(0),
                text=self.text[f"smail_{self.language}_sendToButton"],
                width=self.button_width
            )
            logger.info("Buttons successfully redefined.")
        except AttributeError:
            logger.error("AttributeError:", exc_info=True)
        except KeyError:
            logger.error("KeyError:", exc_info=True)
        except Exception:
            logger.error("Error:", exc_info=True)

    def left_frame(self):

        self.frame = tk.Frame(self)
        self.frame.configure(bg=self.background_color)
        self.frame.columnconfigure(0, weight=1, uniform="a")
        self.frame.rowconfigure(0, weight=1, uniform="a")
        self.inbox_label = tk.Label(
            self.frame, text=self.text[f"smail_{self.language}_inboxLabel"],
            font=font_config(), bg=self.background_color
        )
        self.inbox_list = tk.Listbox(
            self.frame, font=font_config(), height=self.number_of_lines_listbox,
            activestyle="none", selectmode=tk.SINGLE
        )
        self.inbox_label.grid(
            row=0, column=0,
            sticky="nsew", padx=10, pady=10, ipady=5
        )
        self.inbox_list.grid(
            row=1, column=0,
            sticky="nsew", padx=20, pady=20
        )

        self.audioConfigure(self.inbox_list, "inbox")

        logger.info("Created left frame with received emails in listbox.")
        return self.frame

    def right_write_frame(self):
        self.rw_frame = tk.Frame(self)
        self.rw_frame.configure(bg=self.background_color)
        self.rw_frame.columnconfigure((0, 1), weight=1, uniform="a")
        self.rw_frame.rowconfigure((0, 1, 2, 4), weight=1, uniform="a")
        self.rw_frame.rowconfigure(3, weight=2, uniform="a")
        self.recipient_label = tk.Label(
            self.rw_frame,
            text=self.text[f"smail_{self.language}_recipientLabel"],
            font=font_config(), bg=self.background_color
        )
        self.subject_label = tk.Label(
            self.rw_frame,
            text=self.text[f"smail_{self.language}_subjectLabel"],
            font=font_config(), bg=self.background_color
        )
        self.content_label = tk.Label(
            self.rw_frame,
            text=self.text[f"smail_{self.language}_messageLabel"],
            font=font_config(), background=self.background_color
        )
        self.recipient_entry = tk.Entry(
            self.rw_frame, font=font_config()
        )
        self.subject_entry = tk.Entry(
            self.rw_frame, font=font_config()
        )
        self.content_entry = scrolledtext.ScrolledText(
            self.rw_frame, font=font_config(), height=self.number_of_lines_textarea
        )

        # audio configuration
        self.audioConfigure(self.recipient_entry, "recipient")
        self.audioConfigure(self.subject_entry, "subject")
        self.audioConfigure(self.content_entry, "write_message")

        # widget placement
        self.recipient_label.grid(
            row=0, column=0,
            sticky="e", padx=10, pady=10
        )
        self.subject_label.grid(
            row=1, column=0,
            sticky="e", padx=10, pady=10
        )
        self.content_label.grid(
            row=2, column=0,
            sticky="w", padx=10, pady=10
        )
        self.recipient_entry.grid(
            row=0, column=1,
            sticky="nsew", padx=10, pady=10
        )
        self.subject_entry.grid(
            row=1, column=1,
            sticky="nsew", padx=10, pady=10
        )
        self.content_entry.grid(
            row=3, column=0, columnspan=2, rowspan=2,
            padx=10, pady=10, ipady=10, sticky="new"
        )

        return self.rw_frame

    def right_read_frame(self):
        self.rr_frame = tk.Frame(self)
        self.rr_frame.configure(bg=self.background_color)
        self.rr_frame.columnconfigure(0, weight=2, uniform="a")
        self.rr_frame.rowconfigure(0, weight=1, uniform="a")
        self.message_label = tk.Label(
            self.rr_frame,
            text=self.text[f"smail_{self.language}_messageLabel"],
            font=font_config(), bg=self.background_color
        )
        self.message_area = scrolledtext.ScrolledText(
            self.rr_frame, font=font_config(), height=self.number_of_lines_listbox
        )

        # audio configuration
        self.audioConfigure(self.message_area, "read_message")


        # grid configuration
        self.message_label.grid(
            row=0, column=0, ipady=5,
            sticky="nsew", padx=10, pady=10
        )
        self.message_area.grid(
            row=1, column=0,
            sticky="nsew", padx=20, pady=20
        )

        return self.rr_frame

    # simplify
    def insert_emails(self):

        try:
            self.emails = read_mail()
            try:
                self.safe_emails = check_email_for_spam(self.emails)
                for n in self.safe_emails:
                    self.inbox_list.insert(tk.END, n.split("From:")[0])
                    # binding listbox to text area to view email
                    self.inbox_list.bind("<<ListboxSelect>>", self.showEmail)
            except Exception:
                logger.critical("Failed to apply anti-phishing filters."
                                "Omitting security steps.", exc_info=True)
                self.safe_emails = self.emails
                for n in self.emails:
                    self.inbox_list.insert(tk.END, n.split("From:")[0])
                    # binding listbox to text area to view email
                    self.inbox_list.bind("<<ListboxSelect>>", self.showEmail)
        except Exception:
            logger.error("Error when trying to fill in the listbox. ",
                         exc_info=True)

    def showEmail(self, event):
        # switch frames
        self.switch_to_reading_mail()

        if not self.inbox_list.curselection():
            # If no selection, use the last selected email
            if (self.last_selected_index is not None
                    and self.last_selected_email is not None):
                self.configure_message_area(self.last_selected_email)

        selected_index = self.inbox_list.curselection()[0]
        selected_email = self.safe_emails[selected_index]
        self.configure_message_area(selected_email)

        # Update the last selected index and email
        self.last_selected_index = selected_index
        self.last_selected_email = selected_email

    def configure_message_area(self, email):
        self.message_area.configure(state="normal")
        self.message_area.delete("1.0", tk.END)
        self.message_area.insert(tk.END, email)
        self.message_area.configure(state="disabled")

    def switch_to_reading_mail(self):
        self.r_frame = self.right_read_frame()
        self.r_frame.grid(
            column=1, row=0
        )
        self.pack()

    def switch_to_write_mail(self):
        self.r_frame = self.right_write_frame()
        self.r_frame.grid(
            column=1, row=0
        )
        self.pack()
        return self.recipient_entry

    def get_recipient_entry(self):
        return self.recipient_entry

    def send_email_status(self):

        succ = send_email(
            self.recipient_entry.get(), self.subject_entry.get(),
            self.content_entry.get("1.0", tk.END)
        )

        if succ == 1:
            self.recipient_entry.delete(0, tk.END)
            self.subject_entry.delete(0, tk.END)
            self.content_entry.delete("1.0", tk.END)

    def fillRecipient(self, id):

        if self.r_frame == self.rr_frame:
            self.r_frame = self.right_write_frame()
        # if every Entry obtains text, message will be sent
        # when pressing Person[id] button for the second time.
        if (self.recipient_entry.get() and self.subject_entry.get() and
                self.content_entry.get("1.0", tk.END).strip() and
                id == self.button_state):
            self.send_email_status()

        # if another Person[id] button is pressed,
        # Entries will be deleted,
        # new recipient entry will be filled in.
        elif (self.subject_entry.get() or
              self.content_entry.get("1.0", tk.END).strip()):
            if id != self.button_state:
                print("No content to send.")
                email = search_mail(id)
                recipient = self.switch_to_write_mail()
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
                recipient = self.switch_to_write_mail()
                recipient.delete(0, tk.END)
            # if Person[id] button is pressed for the second time,
            # but none of the entry is filled in.
            else:
                print("Button pressed for the second time,"
                      " no entry is filled in.")
                email = search_mail(id)
                recipient = self.switch_to_write_mail()
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
