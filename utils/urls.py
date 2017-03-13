import os
from urllib.parse import urlparse
import mimetypes


VALID_IMAGE_EXTENSIONS = [
    '.jpg',
    '.jpeg',
    '.png',
    '.gif',
]

VALID_IMAGE_MIMETYPES = [
    "image"
]


def valid_url_extension(url, extension_list=VALID_IMAGE_EXTENSIONS):
    # http://stackoverflow.com/a/10543969/396300
    return any([url.endswith(e) for e in extension_list])


def valid_url_mimetype(url, mimetype_list=VALID_IMAGE_MIMETYPES):
    # http://stackoverflow.com/a/10543969/396300
    mimetype, encoding = mimetypes.guess_type(url)
    if mimetype:
        return any([mimetype.startswith(m) for m in mimetype_list])
    else:
        return False


def split_url(url):
    parse_object = urlparse(url)
    return parse_object.netloc, parse_object.path


def get_url_tail(url):
    return url.split('/')[-1]


def get_extension(filename):
    return os.path.splitext(filename)[1]
