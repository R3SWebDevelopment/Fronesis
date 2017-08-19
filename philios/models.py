from drum.links.models import Link
from taggit.managers import TaggableManager
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from versatileimagefield.fields import VersatileImageField, PPOIField
from django.contrib.contenttypes.models import ContentType
from django_comments.models import Comment
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
    return '{}/{}'.format(UPLOAD_PATH, filename)


class Post(Link):
    LINK = 'LI'
    IMAGE = 'IM'
    VIDEO = 'VI'
    LINK_TYPES = (
        (LINK, 'Link'),
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
    )

    tags = TaggableManager()
    image = VersatileImageField(
        null=True, blank=True, ppoi_field='ppoi')
    ppoi = PPOIField('Image PPOI', default=(0.5, 0.5))
    link_type = models.CharField(
        max_length=2,
        choices=LINK_TYPES,
        default='LI'
    )

    @property
    def up_rating_count(self):
        return self.rating.filter(value=1).count()

    @property
    def down_rating_count(self):
        return self.rating.filter(value=-1).count()

    def get_comments_count(self):
        content_type = ContentType.objects.get_for_model(Post)
        return Comment.objects.filter(content_type=content_type, object_pk=self.pk).count()

    def get_tags_list(self):
        return [t.get('name') for t in self.tags.all().values('name')]

