from .serializers import (
    PostSerializer, RatingSerializer, CommentSerializer,
    get_post_content_type
)
from utils.urls import (
    split_url, get_url_tail
)
from utils.images import (
    retrieve_image, image_exists, valid_image_mimetype,
    pil_to_django
)
from utils.mixins import OnlyAlterOwnObjectsViewSet
from versatileimagefield.image_warmer import VersatileImageFieldWarmer
from mezzanine.generic.models import Rating
from django_comments.models import Comment
from django.conf import settings
from rest_framework import viewsets
from django.db import transaction
from .models import Post
from .serializers import _invalidate
from PIL import Image


class PostViewSet(OnlyAlterOwnObjectsViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def _process_image_link(self, serializer):
        # now download the image and validate it
        url = serializer.validated_data['link']
        domain, path = split_url(url)
        filename = get_url_tail(path)

        # try to download
        if not image_exists(url):
            _invalidate(
                (
                    'Couldnt retreive image. '
                    '(There was an error reaching the server)'
                )
            )

        # validate downloaded image
        fobject = retrieve_image(url)
        mimetype, valid_mimetype = valid_image_mimetype(fobject)
        if not valid_mimetype:
            return _invalidate('Downloaded file was not a valid image')

        # convert and save the image
        pil_image = Image.open(fobject)
        django_file = pil_to_django(pil_image, mimetype)

        # save to database
        instance = None
        with transaction.atomic():
            instance = self._do_creation(serializer)
            instance.image.save(filename, django_file)

            # create thumbnails
            num_created, failed_to_create = VersatileImageFieldWarmer(
                instance_or_queryset=instance,
                rendition_key_set='post_image',
                image_attr='image',
                verbose=True
            ).warm()

            # save model
            instance.save()
        return instance

    def _process_video_link(self, serializer):
        return self._do_creation(serializer)

    def _process_regular_link(self, serializer):
        return self._do_creation(serializer)

    def _do_creation(self, serializer):
        return serializer.save(user=self.request.user)

    def perform_create(self, serializer):
        # set link processing depending on link type
        t = serializer.validated_data['link_type']
        p = self._process_image_link if t == Post.IMAGE \
            else self._process_video_link if t == Post.VIDEO \
            else self._process_regular_link

        return p(serializer)  # do the processing


class CommentViewSet(OnlyAlterOwnObjectsViewSet):
    serializer_class = CommentSerializer
    filter_fields = CommentSerializer.Meta.filter_fields
    queryset = Comment.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        return Comment.objects.filter(
            content_type=get_post_content_type()
        )

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user,
            content_type=get_post_content_type(),
            is_removed=False,
            site_id=settings.SITE_ID
        )


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    filter_fields = RatingSerializer.Meta.filter_fields
    queryset = Rating.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        return Rating.objects.filter(
            content_type=get_post_content_type()
        )

    def perform_create(self, serializer):
        with transaction.atomic():
            # TODO: move this to signals
            # delete previous ratings from the same user to the same object
            rating = serializer.validated_data
            Rating.objects.filter(
                user=self.request.user,
                content_type=get_post_content_type(),
                object_pk=rating['object_pk']
            ).delete()

            return serializer.save(
                user=self.request.user,
                content_type=get_post_content_type()
            )
