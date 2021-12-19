import chardet
from quopri import decodestring

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
