from django.core.files.base import ContentFile
from io import BytesIO
import magic
import requests


def image_exists(url):
    r = requests.head(url, allow_redirects=True)
    print(r)
    return r.status_code == requests.codes.ok


def retrieve_image(url):
    response = requests.get(url, allow_redirects=True)
    return BytesIO(response.content)


def get_mimetype(fobject):
    mime = magic.Magic(mime=True)
    mimetype = mime.from_buffer(fobject.read(1024))
    fobject.seek(0)
    return mimetype


def valid_image_mimetype(fobject):
    # http://stackoverflow.com/q/20272579/396300
    mimetype = get_mimetype(fobject)
    if mimetype:
        return mimetype, mimetype.startswith('image')
    else:
        return mimetype, False


def pil_to_django(image, mimetype):
    # http://stackoverflow.com/questions/3723220/how-do-you-convert-a-pil-image-to-a-django-file
    fobject = BytesIO()
    image.save(fobject, format=mimetype.split('/')[1].lower())
    return ContentFile(fobject.getvalue())
