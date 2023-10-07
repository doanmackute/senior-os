import tkinter as tk
from tkinter import ttk
import smtplib
from email.mime.text import MIMEText
import imaplib
import email
import json
from sgive.src.gui_template import configActions
from sgive.src.gui_template import guiTemplate

class defaultFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Fixed frame for main buttons that switch between writing email frame and reading email frame
        self.buttonFrame = ttk.Frame(self)
        self.buttonFrame.rowconfigure(0, weight=1, uniform="a")
        self.buttonFrame.columnconfigure((0, 1), weight=1, uniform="a")

        self.sendButton = ttk.Button(self.buttonFrame, text="Send email", style="my.TButton", command=self.showWriteMailFrame)
        self.readButton = ttk.Button(self.buttonFrame, text="Read email", style="my.TButton", command=self.showReadMailFrame)


        # button placement
        self.sendButton.grid(row=0, column=0, sticky="nsew", pady=10, padx=10, ipadx=80, ipady=80)
        self.readButton.grid(row=0, column=1, sticky="nsew", pady=10, padx=10, ipadx=80, ipady=80)
        self.buttonFrame.pack()

        # Frame that will be displayed under the button frame, switchable when button is pressed
        self.currentFrame = WriteMailFrame(self)
        self.pack()

    # switching frames
    def showWriteMailFrame(self):
        self.currentFrame.forget()
        self.currentFrame = WriteMailFrame(self)

    def showReadMailFrame(self):
        self.currentFrame.forget()
        self.currentFrame = readMailFrame(self)

class WriteMailFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # grid configuration
        self.columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform="a")

        self.createWidgets()
        self.pack(side="left")

    def createWidgets(self):
        # widgets for writing an email

        photo = tk.PhotoImage(file="img/exitButton.png")
        self.recipientLabel = ttk.Label(self, text="To: ", style="my.TLabel")
        self.subjectLabel = ttk.Label(self, text="Subject: ", style="my.TLabel")
        self.contentLabel = ttk.Label(self, text="Message: ", style="my.TLabel")
        self.recipientEntry = ttk.Entry(self, font=("Halvetica", 30))
        self.subjectEntry = ttk.Entry(self, font=("Halvetica", 30))
        self.contentEntry = tk.Text(self, font=("Halvetica", 30), height=8)
        self.sendMailButton = ttk.Button(self, text="Send email", style="my.TButton", command=self.sendMail, image=photo)

        self.recipientLabel.grid(row=0, column=0, sticky="e", padx=10, pady=10, ipady=50)
        self.recipientEntry.grid(row=0, column=1, sticky="nsew", pady=10)
        self.subjectLabel.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.subjectEntry.grid(row=1, column=1, sticky="nsew", pady=10)
        self.contentLabel.grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.contentEntry.grid(row=2, column=1, rowspan=2)
        self.sendMailButton.grid(row=4, column=1, pady=10, padx=10, sticky="new")
        self.createRecipientFrame()

    def createRecipientFrame(self):

        # future plan - buttons with images representing family members, when the senior clicks on the button the recipient's email address will be automatically filled in
        recipientFrame = ttk.Frame(self)
        recipientFrame.columnconfigure(1, weight=1, uniform="a")
        recipientFrame.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform="a")

        recipient1 = ttk.Button(recipientFrame, text="recipient 1", style="my.TButton")
        recipient2 = ttk.Button(recipientFrame, text="recipient 2", style="my.TButton")
        recipient3 = ttk.Button(recipientFrame, text="recipient 3", style="my.TButton")
        recipient4 = ttk.Button(recipientFrame, text="recipient 4", style="my.TButton")


        ttk.Label(recipientFrame, text="Recipient: ", style="my.TLabel").grid(row=0, column=0, sticky="ns")

        recipient1.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        recipient2.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")
        recipient3.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")
        recipient4.grid(row=4, column=0, pady=10, padx=10, sticky="nsew")

        recipientFrame.grid(row=0, rowspan=4, column=2, sticky="nsew", padx=10, pady=10)

    def sendMail(self):

        # connection to the smtp server and other information are taken from the credentials.json file
        # in order to be able to connect to the gmail mailbox, it is necessary to enter the email address and password for the appliaction
            # (password needs to be generated in google account via: google account -> security -> 2-step verification -> app passwords)

        with open("config/credentials.json", "r") as f:
            credentials = json.loads(f.read())
            self.username = credentials["username"]
            self.password = credentials["password"]
            self.server = credentials["server"]
            self.port = credentials["port"]
        f.close()

        self.recipient = self.recipientEntry.get()
        self.subject = self.subjectEntry.get()
        self.content = self.contentEntry.get("1.0", tk.END)

        msg = MIMEText(self.content)
        msg['Subject'] = self.subject
        msg['From'] = self.username
        msg['To'] = self.recipient

        try:

            with smtplib.SMTP_SSL(self.server, self.port) as smtp_server:
                smtp_server.login(self.username, self.password)
                smtp_server.sendmail(self.username, self.recipient, msg.as_string())

            self.recipientEntry.delete(0, tk.END)
            self.subjectEntry.delete(0, tk.END)
            self.contentEntry.delete("1.0", tk.END)

        except Exception as error:
            print("Error occured when trying to send email. Check your email and password.", error)

class readMailFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # grid configuration
        self.columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.rowconfigure((0, 1,2), weight=1, uniform="a")

        self.createWidgets()
        self.pack()

    def createWidgets(self):

        # widgets for reading an email
        self.inboxLabel = ttk.Label(self, text="Inbox: ", style="my.TLabel")
        self.inboxList = tk.Listbox(self, font=("Halvetica", 30), height=15, width=40, activestyle="none", selectmode=tk.SINGLE)
        self.textArea = tk.Text(self, font=("Halvetica", 30), height=15, borderwidth=1, relief=tk.SUNKEN, state="disabled")

        self.inboxLabel.grid(row=0, column=0, sticky="nsew", padx=10, ipady=50)
        self.inboxList.grid(row=1, column=0, sticky="new", padx=20, pady=20, rowspan=2)
        self.textArea.grid(row=1, rowspan=2, column=1, columnspan=2, padx=20, pady=20, sticky="new")


        self.insertEmails()

    def insertEmails(self):

        # connection to the imap server and other information are taken from the credentials.json file
        # in order to be able to connect to the gmail mailbox, it is necessary to enter the email address and password for the appliaction
            # (password needs to be generated in google account via: google account -> security -> 2-step verification -> app passwords)

        with open("config/credentials.json", "r") as f:
            credentials = json.loads(f.read())
            self.username = credentials["username"]
            self.password = credentials["password"]
            self.gmailHost = credentials["gmail_host"]
            self.imapPort = credentials["imap_port"]
        f.close()

        try:
            mail = imaplib.IMAP4_SSL(self.gmailHost, self.imapPort)
            mail.login(self.username, self.password)
            mail.select("INBOX")

            _, selected_mails = mail.search(None, 'ALL')

            self.emails = []

            for num in selected_mails[0].split():
                _, data = mail.fetch(num, '(RFC822)')
                _, bytes_data = data[0]

                # convert the byte data to message
                email_message = email.message_from_bytes(bytes_data)

                for part in email_message.walk():
                    if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                        message = part.get_payload(decode=True)

                        try:
                            message_deocde = message.decode("utf-8")
                        except:
                            message_deocde = message.decode("latino-1")


                        email_content = "Subject: "+ email_message["subject"] + "\nFrom: " + email_message["from"] + "\nDate: " + email_message["date"] + "\nMessage:\n" + message_deocde
                        self.emails.append(email_content)
                        break

            for n in self.emails:
                self.inboxList.insert(tk.END, n.split("From:")[0])
                # binding listbox to text area to view email
                self.inboxList.bind("<<ListboxSelect>>", self.showEmail)

        except Exception as error:
            print("Error occured when connecting to imap server. Check your email address and password.", error)

    def showEmail(self, event):
        selectedIndex = self.inboxList.curselection()[0]
        selectedEmail = self.emails[selectedIndex]
        self.textArea.configure(state="normal")
        self.textArea.delete("1.0", tk.END)
        self.textArea.insert(tk.END, selectedEmail)
        self.textArea.configure(state="disabled")

def main():

    window = tk.Tk()
    window.title("Smail - Mail Client for Seniors")

    with open("config/config.json", "r") as f:
        config = json.loads(f.read())
        fontName = config["data"]["fontName"]
        fontSize = config["data"]["fontSize"]
        fontWeight = config["data"]["fontWeight"]
    f.close()

    # window geometry
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    window.geometry(f"{screenWidth}x{screenHeight}")
    window.minsize(870, 800)

    # font configuration
    style = ttk.Style()
    style.configure("my.TButton", font = (fontName, fontSize, fontWeight))
    style.configure("my.TLabel", font = (fontName, fontSize, fontWeight))

    defFrame = defaultFrame(window)

    window.mainloop()

if __name__ == "__main__":
    main()

