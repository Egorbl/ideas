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

    # tagList = TagRelatedField(many=True, required=False, source='tags')

    class Meta:
        model = Idea
        fields = (
            'id', 'owner', 'category', 'title', 'content', 'date_added',
            'date_updated', 'tags', 'likes', 'is_actual',
        )


class CommentSerializer(serializers.ModelSerializer):

    owner = AccountSerializer(read_only=True)
    likes = serializers.ReadOnlyField()
    is_updated = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = (
            'id', 'idea_id', 'owner', 'content', 'date_added', 'is_updated', 'likes',
        )


class LikeSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField()

    class Meta:
        model = Like
        fields = ('idea_id', 'owner')
