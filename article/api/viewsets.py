from datetime import datetime, timedelta
from rest_framework import mixins, status, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from article.api.serializer import CreateArticleSerializer, UpdateArticleSerializer, \
    WriterSerializer, UserSerializer
from article.models import Article
from writer.models import Writer
from django.db.models import Count, Q


class ArticleViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = CreateArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = CreateArticleSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = UpdateArticleSerializer(instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


class CreateUserView(CreateAPIView):

    model = Writer
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer


class WriterListViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = WriterSerializer
    queryset = Writer.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        date = datetime.now() - timedelta(days=30)
        return Writer.objects.all().prefetch_related('writer').annotate(last_30_days=Count('writer', filter=Q(writer__created_at__gte=date)))


