from django.core.files.base import ContentFile
import httplib
import requests
import StringIO
import magic


def image_exists(domain, path):
    # http://stackoverflow.com/questions/2486145/python-check-if-url-to-jpg-exists
    try:
        conn = httplib.HTTPConnection(domain)
        conn.request('HEAD', path)
        response = conn.getresponse()
        conn.close()
    except:
        return False
    return response.status == 200


def retrieve_image(url):
    response = requests.get(url)
    return StringIO.StringIO(response.content)


def get_mimetype(fobject):
    mime = magic.Magic(mime=True)
    mimetype = mime.from_buffer(fobject.read(1024))
    fobject.seek(0)
    return mimetype


def valid_image_mimetype(fobject):
    # http://stackoverflow.com/q/20272579/396300
    mimetype = get_mimetype(fobject)
    if mimetype:
        return mimetype.startswith('image')
    else:
        return False


def pil_to_django(image, format="JPEG"):
    # http://stackoverflow.com/questions/3723220/how-do-you-convert-a-pil-image-to-a-django-file
    fobject = StringIO.StringIO()
    image.save(fobject, format=format)
    return ContentFile(fobject.getvalue())
