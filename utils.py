import base64
import chardet
import html
import re
import errno
import os
import time
from quopri import decodestring
import shutil
from slugify import slugify
from email.header import decode_header


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

    if unknown is None:
        return ''

    if encoding and not encoding in ("unknown-8bit",):
        encoding = encoding.lower()

        # Can't see how to decode such locale otherwise
        if encoding == "el_gr.utf8":
            encoding = "windows-1253"

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

        # This comes from email module where result is a list of tuples (text, encoding)
        if encoding == 'header':
            header = decode_header(unknown)
            result = ''
            for header_text, header_encoding in header:
                result += ' ' + normalize(header_text, header_encoding).strip()

            return result.strip()

        if isinstance(unknown, str):
            unknown = unknown.encode()

        return unknown.decode(encoding, errors="replace")

    if isinstance(unknown, str):
        unknown = unknown.encode()

    estimate = chardet.detect(unknown)

    if estimate["encoding"]:
        if estimate["encoding"] == "utf-8":
            return unknown.decode()

        try:
            return unknown.decode(estimate["encoding"])
        except Exception as e:
            # Maybe https://github.com/SSilence/php-imap-client/issues/112 ?
            if estimate["encoding"].lower() == "Windows-1254".lower():
                return unknown.decode()

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


suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    """
    Idea taken from
    https://stackoverflow.com/a/14996816
    """
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def simplifyEmailHeader(header):
    """
    Tries to minimize email header
    """
    emails = re.findall("(\"?<?\"?([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)\"?>?\"?)", header)
    already = []
    result = header
    rest = header
    for mail in emails:
        if mail in already:
            continue

        already.append(mail[0])
        toReplace = '<i class="bi bi-envelope-fill" title="%s"></i><span class="hide">%s</span>' % (mail[1], mail[1])

        result = result.replace(mail[0], toReplace)
        rest = rest.replace(mail[0], '').strip().strip(",").strip()
    
    if rest == "":
        return html.escape(header)
    
    return result


def slugify_safe(val, defaultVal = '', maxSize = 50):
    """
    Wraps slugify function in cases result is way too big
    """
    result = slugify(val)

    if not result or len(result) > maxSize:
        result = defaultVal

    return result


def strftime(val, format="%Y-%m-%d %H:%m"):
    """
    Formats a date within Jinja env
    """

    if not val:
        return "?"

    return str(time.strftime(format, val))
