import logging

logger = logging.getLogger(__file__)

import imaplib
import json
import smtplib
from email.mime.text import MIMEText
import email
import ssl
import re


# connection to the smtp/imap server and other information are taken from
# credentials.json file, in order to be able to connect to the gmail mailbox,
# it is necessary to enter the email address and password for the application
# (password needs to be generated in google account via:
#   google account -> security -> 2-step verification -> app passwords)

try:
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
    logger.info("Email Credentials read successfully.")
except Exception:
    logger.error("Couldn't read email credentials and server names.")




def sendEmail(recipient, subject, content):

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = login
    msg['To'] = recipient

    try:
        with smtplib.SMTP_SSL(
                smtp_server, smtp_port, context=sslContext
        ) as server:
            server.login(login, password)
            server.sendmail(login, recipient, msg.as_string())
        return 1

    except Exception as error:
        logger.error("Error occurred when trying to send email. "
                     "Check email and password configuration.", exc_info=True)
        return error


def readMail():

    try:
        mail = imaplib.IMAP4_SSL(
            imap_server, imap_port, ssl_context=sslContext
        )
        mail.login(login, password)
        logger.info("Successful connection to IMAP server.")

        # selecting folder from which to read e-mails
        mail.select("INBOX")

        _, selected_mails = mail.search(None, 'ALL')

        emails = []

        for num in selected_mails[0].split():
            _, data = mail.fetch(num, '(RFC822)')
            _, bytes_data = data[0]

            # convert the byte data to message
            email_message = email.message_from_bytes(bytes_data)

            for part in email_message.walk():
                if (part.get_content_type() == "text/plain"
                        or part.get_content_type() == "text/html"):
                    message = part.get_payload(decode=True)

                    try:
                        message_deocde = message.decode("utf-8")

                    except Exception as error:
                        logger.warning(f"trying different formatting for email "
                                     f"from {email_message['from']};"
                                    f" error: {error}")
                        message_deocde = message.decode("latin-1")

                    email_content = ("Subject: " + email_message["subject"]
                                     + "\nFrom: " + email_message["from"]
                                     + "\nDate: " + email_message["date"]
                                     + "\nMessage:\n" + message_deocde)
                    emails.append(email_content)
                    break
        logger.info("Emails successfully loaded.")
        return emails

    except Exception as error:
        logger.error("Error when trying to connect to imap server,"
                     " check your username and password!", exc_info=True)
        print("Error when trying to connect to imap server,"
              " check your username and password!", error)


def checkCustomDB(email_address):
    try:
        with open("antiphishing/custom_email_block.json", "r") as f:
            data = json.loads(f.read())
        f.close()
    except Exception:
        logger.error("Couldn't load custom_email_block.json", exc_info=True)

    if email_address in data:
        print(email_address, " is in custom blacklist.")
        return False
    else:
        print(email_address, " is not in custom blacklist.")
        return True


def checkDomainBP(email_address):
    try:
        with open("antiphishing/domains.json", "r") as f:
            data = json.loads(f.read())
        f.close()
    except Exception:
        logger.error("Couldn't read domains.json.", exc_info=True)

    email = email_address.split("@")[1]

    if email in data:
        print(email_address, " is in database of phishing domains.")
        return False
    else:
        print(email_address, " is not present in the phishing database.")
        return True


def checkContentOfEmail(content):

    url_pattern = r"https?://(?:www\.)?\S+|www\.\S+"
    urls = re.findall(url_pattern, content)

    if urls:
        print("found urls in email message:")
        for url in urls:
            print(url)
        return False
    else:
        print("no urls in email message.")
        return True


def checkEmailForSpam(email_messages):

    with open("antiphishing/permitted_emails.json", "r") as f:
        emails = json.loads(f.read())
    f.close()

    safe_emails = []

    # getting email address
    for email_content in email_messages:
        email_parts = email_content.split("\n")

        # Extract relevant information
        sender = email_parts[1].replace("From: ", "")
        message = "".join([s.strip("\r") for s in email_parts[4:]])

        # modify sender address
        if '<' in sender and '>' in sender:
            start_index = sender.find('<')
            end_index = sender.find('>')
            if start_index < end_index:
                modified_sender = sender[start_index + 1:end_index]
        else:
            modified_sender = sender

        # antiphishing process
        if modified_sender in emails:
            print("Received email from permitted email address.")
            customBlock = True
            domainBlock = True
            contentBlock = True
        else:
            customBlock = checkCustomDB(modified_sender)
            domainBlock = checkDomainBP(modified_sender)
            contentBlock = checkContentOfEmail(message)

        if customBlock and domainBlock and contentBlock:
            safe_emails.append(email_content)
            print("email address and content of an email are safe"
                  " or are sent by an permitted email address.\n")
        else:
            print("email address found in one of the databases\n")
            if not contentBlock:
                print("there is a security vulnerability in message.")

    print(len(safe_emails))
    return safe_emails
