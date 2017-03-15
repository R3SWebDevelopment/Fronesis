from django.contrib.admin import register

from mezzanine.generic.admin import ThreadedCommentAdmin
from drum.links.admin import LinkAdmin, KeywordAdmin

from mezzanine.generic.models import ThreadedComment
from mezzanine.generic.models import Keyword

from fronesis.admin import admin_site
from .models import Post


@register(Post, site=admin_site)
class PostModelAdmin(LinkAdmin):
    list_editable = ()
    fieldsets = (
        (None, {
            'fields': (
                'title', 'description', 'link',
                'link_type', 'status', 'publish_date',
                'user',
            ),
        }),
    )


@register(Keyword, site=admin_site)
class KeywordModelAdmin(KeywordAdmin):
    pass


@register(ThreadedComment, site=admin_site)
class ThreadedCommentModelAdmin(ThreadedCommentAdmin):
    pass
