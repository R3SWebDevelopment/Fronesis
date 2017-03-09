from django.contrib.admin import register

from mezzanine.generic.admin import ThreadedCommentAdmin
from drum.links.admin import LinkAdmin, KeywordAdmin

from mezzanine.generic.models import ThreadedComment
from mezzanine.generic.models import Keyword
from drum.links.models import Link

from fronesis.admin import admin_site


@register(Link, site=admin_site)
class LinkModelAdmin(LinkAdmin):
    pass


@register(Keyword, site=admin_site)
class KeywordModelAdmin(KeywordAdmin):
    pass


@register(ThreadedComment, site=admin_site)
class ThreadedCommentModelAdmin(ThreadedCommentAdmin):
    pass
