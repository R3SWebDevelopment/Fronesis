from drum.links.models import Link
from taggit.managers import TaggableManager


class Post(Link):
    tags = TaggableManager()
