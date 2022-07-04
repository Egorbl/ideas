from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from .models import (
    Idea, Tag, Comment, Like
)
from .serializers import (
    IdeaSerializer, TagSerializer, CommentSerializer, LikeSerializer
)


class IdeaAPIView(APIView):

    model = Idea
    serializer_class = IdeaSerializer
    validation_error = {"error": "Validation error"}
    not_found_error = {"error": "Item not found"}

    def filter_queryset(self, **filters):
        queryset = self.model.objects.all()

        tag = filters.get("tag")
        if tag is not None:
            queryset = queryset.filter(tags__name=tag)

        only_my = filters.get("only_me")
        if only_my is not None:
            queryset = queryset.filter()

        category = filters.get('category')
        if category is not None:
            queryset = queryset.filter(category=category)

        only_actual = filters.get("only_actual", True)
        if only_actual is True:
            queryset = queryset.filter(is_actual=True)

        new_or_popular = filters.get("new_or_popular", 'new')
        if new_or_popular == 'new':
            queryset = queryset.order_by('date_added')
        elif new_or_popular == 'popular':
            queryset = queryset.order_by('likes')

        return queryset

    # tag: None, only_my: None, category: None, new_or_popular: 'new', only_actual: True
    def get(self, request):
        filters = request.query_params
        result_queryset = self.filter_queryset(**filters)
        serializer = self.serializer_class(result_queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        idea = request.data
        tags_id = idea.pop("tags", [])
        tags = self.get_tags(tags_id)

        if isinstance(tags, Response):
            return tags

        serializer = self.serializer_class(data=idea)
        if not serializer.is_valid():
            return Response(self.validation_error, status=400)
        serializer.save(owner=request.user, tags=tags)
        return Response(serializer.data)

    def get_tags(self, tags_id):
        tags = []
        for tag_id in tags_id:
            tag = Tag.objects.filter(id=tag_id).first()
            if not tag:
                return Response(self.validation_error)
            tags.append(tag)
        return tags


class TagAPIView(APIView):

    model = Tag
    serializer_class = TagSerializer
    validation_error = {"error": "Validation error"}
    not_found_error = {"error": "Item not found"}

    def get(self, request):
        queryset = self.model.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        tag = request.data
        serializer = self.serializer_class(data=tag)
        if not serializer.is_valid():
            return Response(self.validation_error, status=400)

        serializer.save()
        return Response(serializer.data)


class IdeaDetailAPIView(APIView):
    model_queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    validation_error = {'error': 'Validation error'}
    not_found_error = {'error': 'Item not found'}

    def get_object_or_error(self, *args, **kwargs):
        pk = kwargs.get('pk')
        idea = self.model_queryset.filter(id=pk).first()

        if not idea:
            raise ValueError

        return idea

    def get(self, request, *args, **kwargs):
        try:
            idea = self.get_object_or_error(*args, **kwargs)
        except ValueError:
            return Response(self.not_found_error, status=404)
        except ValidationError:
            return Response(self.validation_error, status=400)

        serializer = self.serializer_class(idea)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        try:
            idea = self.get_object_or_error(*args, **kwargs)
        except ValueError:
            return Response(self.not_found_error, status=404)
        except ValidationError:
            return Response(self.validation_error, status=400)

        new_idea = request.data
        tags = new_idea.pop("tags", [])
        serializer = self.serializer_class(data=new_idea, instance=idea)
        if not serializer.is_valid():
            return Response(self.validation_error, status=400)

        if tags:
            tags = self.get_tags(tags)
            serializer.save(tags=tags)
        else:
            serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        try:
            idea = self.get_object_or_error(*args, **kwargs)
        except ValueError:
            return Response(self.not_found_error, status=404)
        except ValidationError:
            return Response(self.validation_error, status=400)

        idea.delete()
        return Response()

    def get_tags(self, tags_id):
        tags = []
        for tag_id in tags_id:
            tag = Tag.objects.filter(id=tag_id).first()
            if not tag:
                return Response(self.validation_error)
            tags.append(tag)
        return tags


class CommentAPIView(APIView):
    model = Comment
    serializer_class = CommentSerializer
    validation_error = {'error': 'Validation error'}
    not_found_error = {'error': 'Item not found'}

    def filter_queryset(self, **filters):
        queryset = self.model.objects.all()

        idea = filters.get('idea')
        queryset = queryset.filter(idea_id=idea.id)

        new_or_popular = filters.get('ordering', 'popular')
        if new_or_popular == 'new':
            queryset = queryset.order_by('-date_added')
        elif new_or_popular == 'popular':
            queryset = queryset.order_by('-likes')

        return queryset

    def get(self, request, *args, **kwargs):
        try:
            idea = IdeaDetailAPIView().get_object_or_error(*args, **kwargs)
        except ValidationError:
            return Response(self.validation_error, status=400)
        except ValueError:
            return Response(self.not_found_error, status=404)

        filters = {**request.query_params, 'idea': idea}

        queryset = self.filter_queryset(**filters)
        return Response(queryset)
