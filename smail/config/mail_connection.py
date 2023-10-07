import imaplib
import json
import smtplib
from email.mime.text import MIMEText
import email
import ssl

# connection to the smtp/imap server and other information are taken from the credentials.json file
# in order to be able to connect to the gmail mailbox, it is necessary to enter the email address and password for the appliaction
# (password needs to be generated in google account via: google account -> security -> 2-step verification -> app passwords)


# reading credentials from json file
with open("config/credentials.json", "r") as f:
    credentials = json.loads(f.read())
    login = credentials["username"]
    password = credentials["password"]
    smtp_server = credentials["smtp_server"]
    smtp_port = credentials["smtp_port"]
    imap_server = credentials["imap_server"]
    imap_port = credentials["imap_port"]

f.close()

sslContext = ssl.create_default_context()


def sendEmail(recipient, subject, content):

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = login
    msg['To'] = recipient

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=sslContext) as server:
            server.login(login, password)
            server.sendmail(login, recipient, msg.as_string())
        return 1

    except Exception as error:
        return error

def readMail():

    try:
        mail = imaplib.IMAP4_SSL(imap_server, imap_port, ssl_context= sslContext)
        mail.login(login, password)

        #selecting folder from which to read e-mails
        mail.select("INBOX")

        _, selected_mails = mail.search(None, 'ALL')

        emails = []

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
                        message_deocde = message.decode("latin-1")

                    email_content = "Subject: " + email_message["subject"] + "\nFrom: " + email_message["from"] + "\nDate: " + email_message["date"] + "\nMessage:\n" + message_deocde
                    emails.append(email_content)
                    break

        return emails

    except Exception as error:
        print(error)
        return error