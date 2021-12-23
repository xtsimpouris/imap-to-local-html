#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013 Remy van Elst
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

from bs4 import BeautifulSoup
import imaplib
import email
import mailbox
from email.header import decode_header, make_header
from email.utils import parsedate
from slugify import slugify
import time
import re
from math import ceil
import os
import base64
import datetime
from quopri import decodestring
import getpass

from jinja2 import Environment
import hashlib
import sys
import yaml

from utils import normalize, removeDir, copyDir, humansize, simplifyEmailHeader
import remote2local

server = {}
try:
    with open('imap-to-local-html.yml', 'r') as file:
        server = yaml.safe_load(file)
        server = server.get('settings')
except Exception as e:
    pass

if not server:
    print("No yml was found or is not valid, exiting. Please check README file or imap-to-local-html.samle.yml for more details")
    exit()

IMAP_SERVER = server.get('domain')
IMAP_USERNAME = server.get('username')
IMAP_PASSWORD = server.get('password')
HTML_PRETTIFY = server.get('prettify', True)

if not IMAP_PASSWORD:
    IMAP_PASSWORD = getpass.getpass()

IMAP_FOLDERS_ORIG = server.get('folders')
IMAP_SSL = server.get('ssl', True)

mail = None
mailFolders = None
inc_location = "inc"

maildir = 'mailbox.%s@%s' % (IMAP_USERNAME, IMAP_SERVER)
if not os.path.exists(maildir):
    os.mkdir(maildir)

maildir_raw = "%s/raw" % maildir
if not os.path.exists(maildir_raw):
    os.mkdir(maildir_raw)

maildir_result = "%s/html" % maildir
if not os.path.exists(maildir_result):
    os.mkdir(maildir_result)


def getTitle(title = None):
    """
    Returns title for all pges
    """

    result = []
    if title:
        result.append(title)

    result.append('%s@%s' % (IMAP_USERNAME, IMAP_SERVER))
    result.append('IMAP to local HTML')

    return ' | '.join(result)


def renderTemplate(templateFrom, saveTo, **kwargs):
    """
    Helper function to render a tamplete with variables
    """
    global HTML_PRETTIFY

    templateContents = ''
    with open("templates/%s" % templateFrom, "r") as f:
        templateContents = f.read()

    env = Environment()
    env.filters["humansize"] = humansize
    env.filters["simplifyEmailHeader"] = simplifyEmailHeader

    template = env.from_string(templateContents)
    result = template.render(**kwargs)
    if saveTo:
        with open(saveTo, "w") as f:
            if HTML_PRETTIFY:
                soup = BeautifulSoup(result, "html.parser")
                f.write(soup.prettify())
            else:
                f.write(result)

    return result


def renderMenu(selectedFolder = '', currentParent = '', linkPrefix = '.'):
    """
    Renders the menu on the left

    Expects: selected folder (id), currentParent (for recursion)
    """

    menuToShow = []
    folders = getMailFolders()
    for folderID in folders:
        folder = folders[folderID]
        if folder["parent"] != currentParent:
            continue

        menuToAdd = folder
        menuToAdd["children"] = renderMenu(selectedFolder, currentParent=folderID, linkPrefix=linkPrefix)
        menuToShow.append(menuToAdd)

    if len(menuToShow) <= 0:
        return ""

    menuToShow.sort(key=lambda val: val["title"])

    return renderTemplate("nav-ul.tpl", None, menuToShow=menuToShow, linkPrefix=linkPrefix)


def renderPage(saveTo, **kwargs):
    """
    HTML page wrapper

    Expects: title, contentZ
    """
    kwargs['title'] = getTitle(kwargs.get('title'))
    kwargs['username'] = IMAP_USERNAME
    kwargs['linkPrefix'] = kwargs.get('linkPrefix', '.')
    kwargs['sideMenu'] = renderMenu(linkPrefix=kwargs['linkPrefix'])

    if (kwargs.get("headerTitle")):
        kwargs['header'] = renderHeader(kwargs.get("headerTitle"))

    return renderTemplate("html.tpl", saveTo, **kwargs)


def renderHeader(title):
    """
    Renders a simple header

    Expects: title
    """

    return renderTemplate("header-main.tpl", None, title=title)


def getMailFolders():
    """
    Returns mail folders
    """
    global mailFolders
    global IMAP_FOLDERS_ORIG

    if not mailFolders is None:
        return mailFolders

    if not mail:
        return mailFolders

    mailFolders = {}
    maillist = remote2local.getAllFolders(mail)
    count = 0
    for folderID in maillist:
        count += 1

        parts = folderID.split(".")

        fileName = "%03d-%s.html" % (count, slugify(normalize(folderID, "utf7")))

        isSelected = False
        for selectedFolder in IMAP_FOLDERS_ORIG:
            if re.search(selectedFolder, folderID):
                isSelected = True
                break

        mailFolders[folderID] = {
            "id": folderID,
            "title": normalize(parts[len(parts) - 1], "utf7"),
            "parent": '.'.join(parts[:-1]),
            "selected": '--all' in IMAP_FOLDERS_ORIG or isSelected,
            "file": fileName,
            "link": "/%s" % fileName,
        }

    # Single root folders do not matter really - usually it's just "INBOX"
    # Let's see how many menus exist with no parent
    menusWithNoParent = []
    for menu in mailFolders:
        if mailFolders[menu]["parent"] == "":
            menusWithNoParent.append(menu)

    # None found or more than one, go home
    if len(menusWithNoParent) == 1:
        # We remove it
        del mailFolders[menusWithNoParent[0]]

        # We change fatherhood for all children
        for menu in mailFolders:
            if mailFolders[menu]["parent"] == menusWithNoParent[0]:
                mailFolders[menu]["parent"] = ""

    return mailFolders


attCount = 0
lastAttName = ""
att_count = 0
last_att_filename = ""


def getLogFile():
    return "%s/%s" % (maildir_raw, 'proccess.txt')


def getHeader(raw, header):
    header = header.lower() + ':'

    lines = raw.split("\n")
    for line in lines:
        if not line.lower().startswith(header):
            continue


        response = line.strip()[len(header):]
        if header in ('from:', 'to:'):
            response = email.utils.parseaddr(response)[1]

        return response


def renderIndexPage():
    global IMAP_USERNAME
    global IMAP_SERVER
    now = datetime.datetime.now()

    allInfo = []
    allInfo.append({
        "title": "IMAP Server",
        "value": IMAP_SERVER,
    })

    allInfo.append({
        "title": "Username",
        "value": IMAP_USERNAME,
    })

    allInfo.append({
        "title": "Date of backup",
        "value": str(now),
    })

    renderPage(
        "%s/%s" % (maildir_result, "index.html"),
        headerTitle="Email Backup index page",
        linkPrefix=".",
        content=renderTemplate(
            "page-index.html.tpl",
            None,
            allInfo=allInfo,
            linkPrefix=".",
        )
    )


def printImapFolders(currentParent = '', intend = '  '):
    """
    Prints list of folders
    """

    if not currentParent:
        print("All folders")

    allFolders = getMailFolders()
    for folderID in allFolders:
        folder = allFolders[folderID]
        if folder["parent"] != currentParent:
            continue

        if allFolders[folderID]["selected"]:
            print("%s**%s (%s)" % (intend, allFolders[folderID]["title"], folderID))
        else:
            print("%s%s (%s)" % (intend, allFolders[folderID]["title"], folderID))
        printImapFolders(folderID, intend + "    ")


def returnWelcome():
    print("########################################################")
    print("# IMAP to Local HTML Backup by Charalampos Tsmipouris  #")
    print("########################################################")
    print("")
    print("Runtime Information:")
    print(sys.version)
    print("")


def extract_date(email):
    date = email.get('Date')
    return parsedate(date)


def getMailContent(mail):
    """
    Walks mail and returns mail content
    """
    content_of_mail_text = ""
    content_of_mail_html = ""
    attachments = []

    for part in mail.walk():
        part_content_maintype = part.get_content_maintype()
        part_content_type = part.get_content_type()
        part_charset = part.get_charsets()

        part_transfer_encoding = part.get_all("Content-Transfer-Encoding")
        if part_transfer_encoding:
            part_transfer_encoding = part_transfer_encoding[0]

        if part_content_type in ('text/plain', 'text/html'):
            part_decoded_contents = part.get_payload(decode=True)
            if part_transfer_encoding is None or part_transfer_encoding == "binary":
                part_transfer_encoding = part_charset[0]

            part_decoded_contents = normalize(part_decoded_contents, part_transfer_encoding)

            if part_content_type == 'text/plain':
                content_of_mail_text += part_decoded_contents
                continue

            if part_content_type == 'text/html':
                content_of_mail_html += part_decoded_contents
                continue

        # Attachment
        if not part.get('Content-Disposition') is None:
            if part.get_content_maintype() == 'multipart':
                continue

            attachment_content = part.get_payload(decode=True)
            # Empty file?
            if not attachment_content:
                continue

            attachment_filename_default = 'no-name-%d' % (len(attachments) + 1)

            if part.get_filename():
                attachment_filename = str(make_header(decode_header(part.get_filename())))
            else:
                attachment_filename = attachment_filename_default

            filename_parts = attachment_filename.split(".")

            filename_ext = filename_parts[-1]
            filename_rest = filename_parts[:-1]
            filename_slug = "%s.%s" % (slugify('.'.join(filename_rest)), filename_ext.lower())

            # slugify may produce really long names due to encoding
            # for such cases let't go with the fedault approach
            if len(filename_slug) > 50:
                filename_slug = attachment_filename_default

            attachments.append({
                "title": attachment_filename,
                "slug": filename_slug,
                "filename": attachment_filename,
                "mimetype": part_content_type,
                "maintype": part_content_maintype,
                "content": attachment_content,
                "size": len(attachment_content),
            })

    if content_of_mail_text:
        content_of_mail_text = re.sub(r"(?i)<html>.*?<head>.*?</head>.*?<body>", "", content_of_mail_text, flags=re.DOTALL)
        content_of_mail_text = re.sub(r"(?i)</body>.*?</html>", "", content_of_mail_text, flags=re.DOTALL)
        content_of_mail_text = re.sub(r"(?i)<!DOCTYPE.*?>", "", content_of_mail_text, flags=re.DOTALL)
        content_of_mail_text = re.sub(r"(?i)POSITION: absolute;", "", content_of_mail_text, flags=re.DOTALL)
        content_of_mail_text = re.sub(r"(?i)TOP: .*?;", "", content_of_mail_text, flags=re.DOTALL)


    if content_of_mail_html:
        content_of_mail_html = re.sub(r"(?i)<html>.*?<head>.*?</head>.*?<body>", "", content_of_mail_html, flags=re.DOTALL)
        content_of_mail_html = re.sub(r"(?i)</body>.*?</html>", "", content_of_mail_html, flags=re.DOTALL)
        content_of_mail_html = re.sub(r"(?i)<!DOCTYPE.*?>", "", content_of_mail_html, flags=re.DOTALL)
        content_of_mail_html = re.sub(r"(?i)POSITION: absolute;", "", content_of_mail_html, flags=re.DOTALL)
        content_of_mail_html = re.sub(r"(?i)TOP: .*?;", "", content_of_mail_html, flags=re.DOTALL)

    return content_of_mail_text, content_of_mail_html, attachments


def backup_mails_to_html_from_local_maildir(folder):
    """
    Creates HTML files and folder index from a mailbox folder
    """
    print("Processing folder: %s" % normalize(folderID, "utf7"), end="")

    global maildir_raw

    mailList = {}

    local_maildir_folder = folder.replace("/", ".")
    local_maildir = mailbox.Maildir(os.path.join(maildir_raw), factory=None, create=True)
    try:
        maildir_folder = local_maildir.get_folder(local_maildir_folder)
    except mailbox.NoSuchMailboxError as e:
        renderPage(
            "%s/%s" % (maildir_result, mailFolders[folder]["file"]),
            headerTitle="Folder %s" % mailFolders[folder]["title"],
            linkPrefix=".",
            content=renderTemplate(
                "page-mail-list.tpl",
                None,
                mailList=mailList,
                linkPrefix=".",
            )
        )

        print("..Done!")
        return

    print("(%d)" % len(maildir_folder), end="")
    sofar = 0
    for mail in maildir_folder:
        mail_id = mail.get('Message-Id')
        if mail_id in mailList:
            continue

        mail_subject = str(make_header(decode_header(mail.get('Subject'))))

        if not mail_subject:
            mail_subject = "(No Subject)"

        mail_from = str(make_header(decode_header(mail.get('From'))))
        mail_to = str(make_header(decode_header(mail.get('To'))))
        mail_date = email.utils.parsedate(decode_header(mail.get('Date'))[0][0])

        mail_id_hash = hashlib.md5(mail_id.encode()).hexdigest()
        mail_folder = str(time.strftime("%Y/%m/%d", mail_date))
        mail_raw = ""
        error_decoding = ""

        try:
            mail_raw = normalize(mail.as_bytes())
        except Exception as e:
            error_decoding += "~> Error in mail.as_bytes(): %s" % str(e)

        try:
            os.makedirs("%s/%s" % (maildir_result, mail_folder))
        except:
            pass

        fileName = "%s/%s.html" % (mail_folder, mail_id_hash)
        content_of_mail_text, content_of_mail_html, attachments = "", "", []

        try:
            content_of_mail_text, content_of_mail_html, attachments = getMailContent(mail)
        except Exception as e:
            error_decoding += "~> Error in getMailContent: %s" % str(e)

        data_uri_to_download = ''
        try:
            data_uri_to_download = "data:text/plain;base64,%s" % base64.b64encode(mail_raw.encode())
        except Exception as e:
            error_decoding += "~> Error in data_uri_to_download: %s" % str(e)

        content_default = "raw"
        if content_of_mail_text:
            content_default = "text"
        if content_of_mail_html:
            content_default = "html"

        attachment_count = 0
        for attachment in attachments:
            attachment_count += 1
            attachment["path"] = "%s/%s-%02d-%s" % (mail_folder, mail_id_hash, attachment_count, attachment["slug"])
            attachment["link"] = "%s/%s-%02d-%s" % (mail_folder, mail_id_hash, attachment_count, attachment["slug"])
            try:
                with open("%s/%s" % (maildir_result, attachment["path"]), 'wb') as att_file:
                    att_file.write(attachment["content"])
            except Exception as e:
                error_decoding += "~> Error writing attachment: %s" % str(e)
                print("Error writing attachment: " + str(e) + ".\n")

        mailList[mail_id] = {
            "id": mail_id,
            "from": mail_from,
            "to": mail_to,
            "subject": mail_subject,
            "date": str(time.strftime("%Y-%m-%d %H:%m", mail_date)),
            "size": len(mail_raw),
            "file": fileName,
            "link": "/%s" % fileName,
            "content": {
                "html": content_of_mail_html,
                "text": content_of_mail_text,
                "raw": mail_raw,
                "default": content_default,
            },
            "download": {
                "filename": "%s.eml" % mail_id_hash,
                "content": data_uri_to_download,
            },
            "attachments": attachments,
            "error_decoding": error_decoding,
        }

        renderPage(
            "%s/%s" % (maildir_result, mailList[mail_id]["file"]),
            headerTitle=mailList[mail_id]["subject"],
            linkPrefix="../../..",
            content=renderTemplate(
                "page-mail.tpl",
                None,
                mail=mailList[mail_id],
                linkPrefix="../../..",
            )
        )

        # No need to keep it in memory
        del mailList[mail_id]["content"]
        del mailList[mail_id]["download"]
        mailList[mail_id]["attachments"] = len(mailList[mail_id]["attachments"])

        sofar += 1
        if sofar % 10 == 0:
            print(sofar, end="")
        else:
            print('.', end="")
        sys.stdout.flush()
    print("Done!")

    print("    > Creating index file..", end="")
    sys.stdout.flush()
    renderPage(
        "%s/%s" % (maildir_result, mailFolders[folder]["file"]),
        headerTitle="Folder %s (%d)" % (mailFolders[folder]["title"], len(mailList)),
        linkPrefix=".",
        content=renderTemplate(
            "page-mail-list.tpl",
            None,
            mailList=mailList,
            linkPrefix=".",
        )
    )

    print("Done!")

returnWelcome()
mail = remote2local.connectToImapMailbox(IMAP_SERVER, IMAP_USERNAME, IMAP_PASSWORD, IMAP_SSL)
printImapFolders()

allFolders = getMailFolders()
for folderID in allFolders:
    if not allFolders[folderID]["selected"]:
        continue

    print(("Getting messages from server from folder: %s.") % normalize(folderID, "utf7"))
    retries = 0
    if IMAP_SSL:
        try:
            remote2local.getMessageToLocalDir(folderID, mail, maildir_raw)
        except imaplib.IMAP4_SSL.abort:
            if retries < 5:
                print(("SSL Connection Abort. Trying again (#%i).") % retries)
                retries += 1
                mail = remote2local.connectToImapMailbox(IMAP_SERVER, IMAP_USERNAME, IMAP_PASSWORD, IMAP_SSL)
                remote2local.getMessageToLocalDir(folderID, mail, maildir_raw)
            else:
                print("SSL Connection gave more than 5 errors. Not trying again")
    else:
        try:
            remote2local.getMessageToLocalDir(folderID, mail, maildir_raw)
        except imaplib.IMAP4.abort:
            if retries < 5:
                print(("Connection Abort. Trying again (#%i).") % retries)
                retries += 1
                mail = remote2local.connectToImapMailbox(IMAP_SERVER, IMAP_USERNAME, IMAP_PASSWORD)
                remote2local.getMessageToLocalDir(folderID, mail, maildir_raw)
            else:
                print("Connection gave more than 5 errors. Not trying again")

    print(("Done with folder: %s.") % normalize(folderID, "utf7"))

renderIndexPage()
removeDir("%s/inc" % maildir_result)
copyDir(inc_location, "%s/inc" % maildir_result)

for folderID in allFolders:
    if not allFolders[folderID]["selected"]:
        continue

    backup_mails_to_html_from_local_maildir(folderID)
