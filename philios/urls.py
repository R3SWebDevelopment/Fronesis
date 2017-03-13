from .views import PostViewSet, RatingViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'posts', PostViewSet)
router.register(r'ratings', RatingViewSet)
urlpatterns = router.urls
