from drum.links.models import Link
from taggit.managers import TaggableManager
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from versatileimagefield.fields import VersatileImageField, PPOIField
import os

UPLOAD_PATH = "image_uploader/"


class UploadedImage(models.Model):
    def generate_upload_path(self, filename):
        filename, ext = os.path.splitext(filename.lower())
        filename = '{}.{}{}'.format(
            slugify(filename),
            timezone.now().strftime('%Y-%m-%d.%H-%M-%S'),
            ext)
        return '%s/%s' % (UPLOAD_PATH, filename)

    image = models.ImageField(
        blank=True, null=True, upload_to=generate_upload_path)


def generate_upload_path(post, filename):
    filename, ext = os.path.splitext(filename.lower())
    filename = '{}.{}{}'.format(
        slugify(filename),
        timezone.now().strftime('%Y-%m-%d.%H-%M-%S'),
        ext)
    return '%s/%s' % (UPLOAD_PATH, filename)


class Post(Link):
    tags = TaggableManager()
    image = VersatileImageField(
        null=True, blank=True, ppoi_field='ppoi')
    ppoi = PPOIField('Image PPOI', default=(0.5, 0.5))
