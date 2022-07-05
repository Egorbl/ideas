from rest_framework import serializers

from authentication.serializers import AccountSerializer
from .models import (
    Tag, Idea, Comment, Like,
)
from .relations import TagRelatedField


class TagSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Tag
        fields = ('id', 'name',)


class IdeaSerializer(serializers.ModelSerializer):

    owner = AccountSerializer(read_only=True)
    likes = serializers.ReadOnlyField()
    tags = TagSerializer(many=True, read_only=True)

    is_liked = serializers.SerializerMethodField(
        read_only=True, method_name='get_is_liked')

    class Meta:
        model = Idea
        fields = (
            'id', 'owner', 'category', 'title', 'content', 'date_added',
            'date_updated', 'tags', 'likes', 'is_actual', 'is_liked',
        )

    def get_is_liked(self, obj):
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
            'id', 'idea_id', 'owner', 'content', 'date_added', 'is_updated', 'likes', 'is_liked',
        )

    def get_is_liked(self, obj):
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
