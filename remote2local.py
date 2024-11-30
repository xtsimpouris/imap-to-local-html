from email.header import decode_header
from email.utils import parsedate
import imaplib
import mailbox
import re
import sys
import time

from utils import normalize


def connectToImapMailbox(IMAP_SERVER, IMAP_USERNAME, IMAP_PASSWORD, IMAP_SSL):
    """
    Connects to remote server
    """
    if IMAP_SSL is True:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    if IMAP_SSL is False:
        mail = imaplib.IMAP4(IMAP_SERVER)
    mail.login(IMAP_USERNAME, IMAP_PASSWORD)

    try:
        mail.enable("UTF8=ACCEPT")
    except Exception as e:
        print("Server does not accept UTF8=ACCEPT")

    return mail


def getAllFolders(mail):
    """
    Returns all folders from remote server
    """
    folderList = []
    folderSeparator = ''

    maillist = mail.list()
    if not maillist or not maillist[0].lower() == 'ok':
        print("Unable to retrieve folder list")
        return folderList, folderSeparator

    for folderLine in maillist[1]:
        folderLine = folderLine.decode()
        parts = re.findall("(\(.*\)) \"(.)\" (.*)", folderLine)

        if not parts:
            print("Unable to decode filder structure: %s" % folderLine)
            continue

        folderList.append(parts[0][2].strip().strip('"'))

        if not folderSeparator:
            folderSeparator = parts[0][1]

    return folderList, folderSeparator


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
        raw_email = data[0][1].replace(b'\r\n', b'\n')
        maildir_folder = mailFolder.replace("/", ".")
        saveToMaildir(raw_email, maildir_folder, maildir_raw)
        sofar += 1

        if sofar % 10 == 0:
            print(sofar, end="")
        else:
            print('.', end="")
        sys.stdout.flush()
    
    print("..Done!")
