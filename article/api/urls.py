from django.urls import path, include
from rest_framework.routers import DefaultRouter
from article.api.viewsets import ArticleViewSet, WriterListViewSet

router = DefaultRouter()
router.register("article", ArticleViewSet, basename='article')
router.register("summary", WriterListViewSet, basename='writer')


urlpatterns = [
    path("", include(router.urls)),
]
