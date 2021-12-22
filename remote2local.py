from email.header import decode_header
from email.utils import parsedate
import imaplib
import mailbox
import re
import sys
import time

from utils import normalize


def connectToImapMailbox(IMAPSERVER, IMAPLOGIN, IMAPPASSWORD, ssl):
    """
    Connects to remote server
    """
    if ssl is True:
        mail = imaplib.IMAP4_SSL(IMAPSERVER)
    if ssl is False:
        mail = imaplib.IMAP4(IMAPSERVER)
    mail.login(IMAPLOGIN, IMAPPASSWORD)
    mail.enable("UTF8=ACCEPT")
    return mail


def getAllFolders(IMAPFOLDER_ORIG, mail):
    """
    Returns all folders from remote server
    """
    response = []
    if len(IMAPFOLDER_ORIG) == 1 and IMAPFOLDER_ORIG[0] == "all":
        maillist = mail.list()
        for imapFolder in sorted(maillist[1]):
            imapFolder = imapFolder.decode()
            imapFolder = re.sub(r"(?i)\(.*\)", "", imapFolder, flags=re.DOTALL)
            imapFolder = re.sub(r"(?i)\".\"", "", imapFolder, flags=re.DOTALL)
            imapFolder = re.sub(r"(?i)\"", "", imapFolder, flags=re.DOTALL)
            imapFolder = imapFolder.strip()
            response.append(imapFolder)
    else:
        response = IMAPFOLDER_ORIG
    return response


def saveToMaildir(msg, mailFolder, maildir_raw):
    """
    Saves a single email to local clone
    """
    mbox = mailbox.Maildir(maildir_raw, factory=mailbox.MaildirMessage, create=True) 
    folder = mbox.add_folder(mailFolder)    
    folder.lock()
    try:
        message_key = folder.add(msg)
        folder.flush()

        maildir_message = folder.get_message(message_key)
        try:
            message_date_epoch = time.mktime(parsedate(decode_header(maildir_message.get("Date"))[0][0]))
        except TypeError as typeerror:
            message_date_epoch = time.mktime((2000, 1, 1, 1, 1, 1, 1, 1, 0))
        maildir_message.set_date(message_date_epoch)
        maildir_message.add_flag("s")


    finally:
        folder.unlock()
        folder.close()
        mbox.close()


def getMessageToLocalDir(mailFolder, mail, maildir_raw):
    """
    Goes over a folder and save all emails
    """
    print("Selecting folder %s" % normalize(mailFolder, "utf7"), end="")
    mail.select(mail._quote(mailFolder), readonly=True)
    print("..Done!")

    try:
        typ, mdata = mail.search(None, "ALL")
    except Exception as imaperror:
        print("Error in IMAP Query: %s." % imaperror)
        print("Does the imap folder \"%s\" exists?" % mailFolder)
        return

    messageList = mdata[0].decode().split()
    sofar = 0
    print("Copying folder %s (%s)" % (normalize(mailFolder, "utf7"), len(messageList)), end="")
    for message_id in messageList:
        result, data = mail.fetch(message_id , "(RFC822)")
        raw_email = data[0][1]
        maildir_folder = mailFolder.replace("/", ".")
        saveToMaildir(raw_email, maildir_folder, maildir_raw)
        sofar += 1

        if sofar % 10 == 0:
            print(sofar, end="")
        else:
            print('.', end="")
        sys.stdout.flush()
    
    print("..Done!")
