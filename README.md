# HTML5 IMAP email backup script

This is a python script to backup any IMAP capable email account to a bowsable HTML archive and a Maildir folder. Not one huge file (mbox), only needing a web browser to view and no proprietary code, so you can make sure I won't steal your password. 

Fork from [RaymiiOrg/NoPriv](https://github.com/RaymiiOrg/NoPriv)

### Virtual environment
It is always better to use a virtual environment
1. Create one with python 2.x, for example `virtualenv --python=/usr/bin/python env`
2. Get into it, for example `. env/bin/activate`
3. Install dependencies from `requirements.txt`, for example `pip install -r requirements.txt`
4. Execute main program, for example `python nopriv.py`
4. Get out from the virtual environment, for example `deactivate`


### Screenshots

#### Running the program
![Execution](images/01. execution.png)

#### Index page
![Home page](images/02. Home page.png)

#### Folder Overview page 
![Folder view](images/03. Folder view.png)

#### Email itself
![Email view](images/04. Email view.png)


### Features

- Works with any IMAP/IMAPS account
- Supports multiple IMAP folders
- Supports text, HTML and multipart email
- Saves attachments
- Backups to HTML files for easy browsing
- Small HTML files can be backed up to external medium more easily, and can be sent over the internet more easily.
- Backs up to Maildir for [easy restoring](http://wiki.colar.net/ruby_script_to_upload_convert_a_maildir_inbox_to_an_imap_server)

### Changelog

New in version 7:
(18-12-2021)
- Refactored to extract mails in different folders per account
- Support bootstrap view

New in version 6 (up to fork):
(18-11-2013)

- Add support to download all folders without typing them all out. Using "NoPriv_All" as foldername now downloads all available folders.
- Fix quite a few HTML errors
- Converted layout from HTML Kickstart to Twitter Bootstrap
- Add offline mode (only converts the Maildir to HTML, does not try to download new email)

New in version 5:  
(13-11-2013)

- Fix issue #22, NoPriv does not crash on empty IMAP folders anymore
- Fix issue #23, NoPriv now tries a few times when the IMAP connection is reset. This happens with Google Mail sometimes.

New in version 4:

- INI style config, either per user or system wide (thanks to [https://github.com/brejoc](Jochen Breuer))

New in version 3.1:

- Added a sample `muttrc` file to view NoPriv with the Mutt mail client. 

New in version 3:

- Supports incremental backups
- If you stop the backup while running, it will now continue were it left off
- Unread mails stay unread, but are backed up (before they were marked as read)
- Restoring possible because it also creates a Maildir
- Better unicode support
- Attachment page is now also styled

New in version 2:

- Support for multiple IMAP folders
- Index page is generated
- Pages have menu now.
- On running it shows all available IMAP folders.

### Usage

1. Clone the repository:

    git clone git://github.com/RaymiiOrg/NoPriv.git

2. Set up your login details, imap server and ssl:

Edit the `nopriv.ini` file with your IMAP server, login and password:

    [nopriv]
    imap_server = imap.gmail.com
    imap_user = xyz@googlemail.com
    imap_password = my_secrept_password
    imap_folder = INBOX, Draft, Newletters
    
    #optional
    ssl = true
    incremental_backup = true

If you want to use SSL to connect to IMAP, or want to use incremental backups, enable or disable the options.

**If you want to backup all folders, enter `NoPriv_All` as imap_folder.**


`Nopriv.ini` can be in the following locations:
 
- './nopriv.ini'
- './.nopriv.ini'
- '~/.config/nopriv.ini'
- '/opt/local/etc/nopriv.ini'
- '/etc/nopriv.ini'

If you use gmail and want to backup all your email, use the "[Gmail]/All Mail" folder. It might be named different if you use another locale, for me with a Dutch gmail account it is named "[Gmail]/Alle Berichten".

3. Execute the script:

    python ./nopriv.py

4. Browse the generated backup:

Open the file `index.html` in your browser. There are all your folders and emails.

If you only have a console, it works just fine in Links2 (see above screenshot):
    
    links2 ./index.html


### Requirements

Python 2.7

Running debian 6 which has python 2.6.6? [See here how to install python 2.7 on debian 6.](https://raymii.org/s/tutorials/Install_Python_2.7_or_3_on_debian_6.html)

### Known issues

- Does not work with python3 (Feel free to port/fix it.)
- Does not handle all charsets. Works best with utf-8 and ascii.
- No search function.
- Not able to change default sorting (latest first).

### Info on incremental backups

If you disable incremental backups, the script will run over the folders, create a maildir, create the pages and then move the maildir to `$maildir.date` where date is a timestamp. 
If you enable incremental backup, it will create a text file `nopriv.txt` with the mail ID's of the folder, so that it know which ID it needs to continue on the next time it is ran. If you delete emails from the folder, the incremental function will not work as expected because of differing ID's.

## Info on restoring

Nopriv creates a Maildir folder, which houses all your email. You can restore this maildir folder to an IMAP account either by using the script [linked at the top on this page](http://wiki.colar.net/ruby_script_to_upload_convert_a_maildir_inbox_to_an_imap_server), or use a mail client like Mutt or Evolution and transport it to an imap account via there.
