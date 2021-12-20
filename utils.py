import base64
import chardet
import errno
import os
from quopri import decodestring
import shutil


def b64padanddecode(b):
    """
    Decode unpadded base64 data
    """
    b+=(-len(b)%4)*'=' #base64 padding (if adds '===', no valid padding anyway)
    return base64.b64decode(b,altchars='+,').decode('utf-16-be')


def imaputf7decode(s):
    """
    Decode a string encoded according to RFC2060 aka IMAP UTF7.
    Minimal validation of input, only works with trusted data
    """

    lst=s.split('&')
    out=lst[0]
    for e in lst[1:]:
        u,a=e.split('-',1) #u: utf16 between & and 1st -, a: ASCII chars folowing it
        if u=='' : out+='&'
        else: out+=b64padanddecode(u)
        out+=a
    return out


def normalize(unknown, encoding = None):
    """
    Tries hard to normalize anything to utf-8
    """
    if encoding:
        encoding = encoding.lower()

        if encoding in ("quoted-printable", "7bit", "8bit"):
            try:
                return normalize(decodestring(unknown))
            except Exception as e:
                return normalize(unknown)

        if encoding == 'base64':
            # Already decoded, do nothing
            return normalize(unknown)

        if encoding == 'utf7':
            return normalize(imaputf7decode(unknown))

        if isinstance(unknown, str):
            unknown = unknown.encode()

        return unknown.decode(encoding, errors="replace")

    if isinstance(unknown, str):
        unknown = unknown.encode()

    estimate = chardet.detect(unknown)

    if estimate["encoding"]:
        if estimate["encoding"] == "utf-8":
            return unknown.decode()

        return unknown.decode(estimate["encoding"])

    if not isinstance(unknown, str):
        unknown = unknown.decode()

    return unknown


def removeDir(src):
    """
    Removes a whole directory and all its contents
    """
    if os.path.exists(src):
        shutil.rmtree(src)


def copyDir(src, dst):
    """
    Copies a whole directory and all its contents
    """
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        elif exc.errno == errno.EEXIST:
            print("File %s already exists." % src)
        else: raise
