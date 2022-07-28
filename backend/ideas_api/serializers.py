from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.serializers import AccountSerializer
from .models import (
    Tag, Idea, Comment, Like, Category,
)


class TagSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Tag
        fields = ('id', 'name',)


class CategorySerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ('id', 'name',)


class IdeaSerializer(serializers.ModelSerializer):

    owner = AccountSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    likes = serializers.ReadOnlyField()
    category = CategorySerializer(read_only=True)

    is_liked = serializers.SerializerMethodField(
        read_only=True, method_name='get_is_liked')

    class Meta:
        model = Idea
        # required: id, category, title, content. Optional: tags
        fields = (
            'id', 'owner', 'category', 'title', 'content', 'date_added',
            'date_updated', 'tags', 'likes', 'is_actual', 'is_liked',
        )

    def get_is_liked(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False

        idea_id = obj.id
        like = Like.objects.filter(
            owner=self.context['request'].user,
            publication_id=idea_id
        ).first()

        return True if like else False


class CommentSerializer(serializers.ModelSerializer):

    owner = AccountSerializer(read_only=True)
    likes = serializers.ReadOnlyField()
    is_updated = serializers.ReadOnlyField()

    is_liked = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_is_liked')

    class Meta:
        model = Comment
        fields = (
            'id', 'idea_id', 'content', 'date_added', 'is_liked', 'is_updated', 'likes', 'owner',
        )

    def get_is_liked(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False

        comment_id = obj.id
        like = Like.objects.filter(
            owner=self.context['request'].user,
            publication_id=comment_id
        ).first()

        return True if like else False


class LikeSerializer(serializers.ModelSerializer):

    owner = AccountSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'publication_id', 'owner')
