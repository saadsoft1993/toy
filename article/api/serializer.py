from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from article.models import Article
from writer.models import Writer


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class CreateArticleSerializer(serializers.ModelSerializer):
    written_by = serializers.SerializerMethodField('_user')

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'written_by']

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user.id


class UpdateArticleSerializer(serializers.ModelSerializer):
    edited_by = serializers.SerializerMethodField('_user')

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'edited_by']

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user.id


class WriterSerializer(serializers.ModelSerializer):
    article = serializers.IntegerField(source='writer.count', read_only=True)
    last_30_days = serializers.IntegerField()

    class Meta:
        model = Writer
        fields = ['id', 'username', 'article', 'last_30_days']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Writer
        fields = ['id', 'name', 'username', 'password', 'is_editor']
        read_only_fields = ('id',)

