from turtle import pu
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.exceptions import ValidationError, ObjectDoesNotExist

import datetime

from .models import (
    Idea, Tag, Comment, Like
)
from .serializers import (
    IdeaSerializer, TagSerializer, CommentSerializer, LikeSerializer
)
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .pagination import IdeaPagination, CommentPagination, TagPagination


class IdeaAPIView(APIView):

    model = Idea
    serializer_class = IdeaSerializer
    validation_error = {"error": "Validation error"}
    not_found_error = {"error": "Item not found"}
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = IdeaPagination

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
        serializer = self.serializer_class(result_queryset, many=True, context={
            'request': request
        })
        serializer_data = serializer.data
        return Response(serializer_data)

    def post(self, request):
        idea = request.data
        tags_id = idea.pop("tags", [])
        tags = self.get_tags(tags_id)

        if isinstance(tags, Response):
            return tags

        serializer = self.serializer_class(data=idea, context={
            'request': request
        })
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
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = TagPagination

    def get(self, request):
        queryset = self.model.objects.all()
        serializer = self.serializer_class(queryset, many=True,  context={
            'request': request
        })
        return Response(serializer.data)

    def post(self, request):
        tag = request.data
        serializer = self.serializer_class(data=tag,  context={
            'request': request
        })
        if not serializer.is_valid():
            return Response(self.validation_error, status=400)

        serializer.save()
        return Response(serializer.data)


class IdeaDetailAPIView(APIView):
    model_queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    validation_error = {'error': 'Validation error'}
    not_found_error = {'error': 'Item not found'}
    permission_classes = (IsOwnerOrReadOnly, )

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

        serializer = self.serializer_class(idea, context={
            'request': request
        })
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
        serializer = self.serializer_class(data=new_idea, instance=idea, context={
            'request': request
        })
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
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CommentPagination

    def filter_queryset(self, **filters):
        queryset = self.model.objects.all()

        new_or_popular = filters.get('ordering', 'new')
        if new_or_popular == 'new':
            queryset = queryset.order_by('-date_added')
        elif new_or_popular == 'popular':
            queryset = queryset.order_by('-likes')
            time_delta = filters.get('time_delta')
            if time_delta is not None:
                now = datetime.datetime.now()
                lower_date = now - datetime.timedelta(days=time_delta)
                queryset = queryset.filter(date__range=[lower_date, now])

        return queryset

    def get(self, request, *args, **kwargs):
        idea_id = kwargs.get("pk")
        try:
            Idea.objects.get(id=idea_id)
        except ValidationError:
            return Response(self.validation_error, status=400)
        except ObjectDoesNotExist:
            return Response(self.not_found_error, status=404)

        filters = {**request.query_params, **kwargs}
        try:
            queryset = self.filter_queryset(**filters)
        except ValidationError:
            return Response(self.validation_error, status=400)

        serializer = self.serializer_class(queryset, many=True, context={
            'request': request
        })
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        idea_id = kwargs.get("pk")

        try:
            Idea.objects.get(id=idea_id)
        except ValidationError:
            return Response(self.validation_error, status=400)
        except ObjectDoesNotExist:
            return Response(self.not_found_error, status=404)

        comment = request.data
        comment['idea_id'] = idea_id

        serializer = self.serializer_class(data=comment, context={
            'request': request
        })
        if not serializer.is_valid():
            return Response(self.validation_error, status=400)
        serializer.save(owner=request.user)

        return Response(serializer.data)


class CommentDetailAPIView(APIView):

    model = Comment
    serializer_class = CommentSerializer
    validation_error = {'error': 'Validation error'}
    not_found_error = {'error': 'Item not found'}
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object_or_error(self, *args, **kwargs):
        pk = kwargs.get('comment_pk')
        comment = self.model.objects.filter(id=pk).first()

        if not comment:
            raise ObjectDoesNotExist

        return comment

    def patch(self, request, *args, **kwargs):
        try:
            comment = self.get_object_or_error(**kwargs)
        except ValidationError:
            return Response(self.validation_error, status=400)
        except ObjectDoesNotExist:
            return Response(self.not_found_error, status=404)

        new_comment = request.data

        serializer = self.serializer_class(
            data=new_comment, instance=comment, partial=True, context={
                'request': request
            })
        if not serializer.is_valid():
            return Response(self.validation_error, status=400)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        try:
            comment = self.get_object_or_error(**kwargs)
        except ValidationError:
            return Response(self.validation_error, status=400)
        except ObjectDoesNotExist:
            return Response(self.not_found_error, status=404)

        comment.delete()
        return Response()


class LikeAPIView(APIView):
    model = Like
    serializer_class = LikeSerializer
    validation_error = {'error': 'Validation error'}
    not_found_error = {'error': 'Item not found'}
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def validate_publication_id(self, publication_id):
        idea = Idea.objects.filter(id=publication_id).first()
        comment = Comment.objects.filter(id=publication_id).first()

        if not (idea or comment):
            raise ObjectDoesNotExist

    def get(self, request, *args, **kwargs):
        queryset = self.model.objects.all()
        serializer = self.serializer_class(queryset, many=True, context={
            'request': request
        })
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        new_like = request.data
        publication_id = kwargs.get("pk")

        try:
            self.validate_publication_id(publication_id)
        except ValidationError:
            return Response(self.validation_error, status=400)
        except ObjectDoesNotExist:
            return Response(self.not_found_error, status=404)

        if user_liked(request.user, publication_id):
            return Response()

        new_like['publication_id'] = publication_id
        serializer = self.serializer_class(data=new_like, context={
            'request': request
        })
        if not serializer.is_valid():
            return Response(self.validation_error, status=400)

        serializer.save(owner=request.user)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        publication_id = kwargs.get("pk")

        try:
            self.validate_publication_id(publication_id)
        except ValidationError:
            return Response(self.validation_error, status=400)
        except ObjectDoesNotExist:
            return Response(self.not_found_error, status=404)

        if not user_liked(request.user, publication_id):
            return Response()

        like = self.model.objects.filter(
            publication_id=publication_id, owner=request.user).first()
        like.delete()
        return Response()


def user_liked(user, publication_id):
    query = Like.objects.filter(
        owner=user, publication_id=publication_id).first()

    return True if query else False
