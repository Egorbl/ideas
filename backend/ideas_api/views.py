from operator import not_
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.exceptions import ValidationError, ObjectDoesNotExist

import datetime

from .models import (
    Idea, Tag, Comment, Like, Category
)
from .serializers import (
    IdeaSerializer, TagSerializer, CommentSerializer, LikeSerializer, CategorySerializer
)
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .pagination import IdeaPagination, CommentPagination, TagPagination


class ErrorsMixin:
    validation_error = {"detail": "Validation error"}
    not_found_error = {"detail": "Item not found"}


class SerializerMixin:

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer_context(self):
        return {
            'request': self.request,
            'views': self,
        }


class IdeaAPIView(APIView, ErrorsMixin, SerializerMixin):

    model = Idea
    serializer_class = IdeaSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = IdeaPagination

    # tag, only_me, category, only_actual, new_or_popular
    def filter_queryset(self, user=None, **filters):
        queryset = self.model.objects.all()

        tag = filters.get("tag")
        if tag is not None:
            queryset = queryset.filter(tags__name=tag[0])

        only_my = filters.get("only_me")
        if only_my is not None and user.is_authenticated:
            queryset = queryset.filter(owner=user)

        category_id = filters.get('category')
        if category_id is not None:
            category = Category.objects.filter(id=category_id[0]).first()
            queryset = queryset.filter(category=category)

        only_actual = filters.get("only_actual", 'true')
        if only_actual[0] == 'true':
            queryset = queryset.filter(is_actual=True)

        sort_by = filters.get("sort_by", 'date')
        if sort_by[0] == 'likes':
            queryset = queryset.order_by('-likes')
        else:
            queryset = queryset.order_by('-date_added')

        return queryset

    # tag: None, only_my: None, category: None, new_or_popular: 'new', only_actual: True
    def get(self, request):
        filters = request.query_params
        user = request.user
        result_queryset = self.filter_queryset(user, **filters)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(
            result_queryset, request)

        serializer = self.get_serializer(paginated_queryset, many=True)
        serializer_data = serializer.data

        return paginator.get_paginated_response(serializer_data)

    def post(self, request):
        idea = request.data
        tags_id = idea.pop('tags', [])
        tags = self.get_tags(tags_id)

        if isinstance(tags, Response):
            return tags

        category_id = idea.pop('category', None)
        category = self.get_category(category_id)

        if not category:
            return Response(self.validation_error, status=400)

        serializer = self.get_serializer(data=idea)
        if not serializer.is_valid():
            self.validation_error['fields'] = serializer.errors
            return Response(self.validation_error, status=400)
        serializer.save(owner=request.user, tags=tags, category=category)
        return Response(serializer.data)

    def get_tags(self, tags_id):
        tags = []
        for tag_id in tags_id:
            tag = Tag.objects.filter(id=tag_id).first()
            if not tag:
                return Response(self.validation_error, status=400)
            tags.append(tag)
        return tags

    def get_category(self, category_id):
        category = Category.objects.filter(id=category_id).first()
        return category


class TagAPIView(APIView, ErrorsMixin, SerializerMixin):

    model = Tag
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request):
        queryset = self.model.objects.all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):

        tag = request.data
        serializer = self.get_serializer(data=tag)
        if not serializer.is_valid():
            return Response(self.validation_error, status=400)

        serializer.save()
        return Response(serializer.data)


class CategoryAPIView(APIView, ErrorsMixin, SerializerMixin):

    model = Category
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request):
        queryset = self.model.objects.all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):

        tag = request.data
        serializer = self.get_serializer(data=tag)
        if not serializer.is_valid():
            return Response(self.validation_error, status=400)

        serializer.save()
        return Response(serializer.data)


class IdeaDetailAPIView(APIView, ErrorsMixin, SerializerMixin):
    model_queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)

        if self.request.method == "PATCH":
            serializer.fields['category'].read_only = True
        return serializer

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

        serializer = self.get_serializer(idea)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        try:
            idea = self.get_object_or_error(*args, **kwargs)
        except ValueError:
            return Response(self.not_found_error, status=404)
        except ValidationError:
            return Response(self.validation_error, status=400)

        self.check_object_permissions(request, idea)

        new_idea = request.data
        tags = new_idea.pop("tags", [])
        category_id = new_idea.pop("category", None)
        if category_id == None:
            return Response(self.validation_error, status=400)

        serializer = self.get_serializer(
            data=new_idea, instance=idea, partial=True)
        if not serializer.is_valid():
            return Response(self.validation_error, status=400)

        category = self.get_category(category_id)
        print(category)

        if tags:
            tags = self.get_tags(tags)
            if isinstance(tags, Response):
                return tags
            serializer.save(tags=tags, category=category)
        else:
            serializer.save(category=category)

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        try:
            idea = self.get_object_or_error(*args, **kwargs)
        except ValueError:
            return Response(self.not_found_error, status=404)
        except ValidationError:
            return Response(self.validation_error, status=400)
        self.check_object_permissions(request, idea)

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

    def get_category(self, category_id):
        category = Category.objects.filter(id=category_id).first()
        return category


class CommentAPIView(APIView, ErrorsMixin, SerializerMixin):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CommentPagination

    def filter_queryset(self, **filters):
        queryset = self.model.objects.all()

        idea_id = filters.get("pk")
        queryset = queryset.filter(idea_id=idea_id)

        sort_by = filters.get('ordering', 'date')
        if sort_by == 'likes':
            queryset = queryset.order_by('-likes')

        return queryset

    def get(self, request, *args, **kwargs):
        idea_id = kwargs.get("pk")
        try:
            Idea.objects.get(id=idea_id)
        except ValidationError:
            validation_error = self.validation_error
            validation_error['fields'] = [
                {"idea_pk": "Needs to be uuid"}
            ]
            return Response(self.validation_error, status=400)
        except ObjectDoesNotExist:
            not_found_error = self.not_found_error
            not_found_error['fields'] = [
                {"idea_pk": "No idea with that uuid"}
            ]
            return Response(self.not_found_error, status=404)

        filters = {**request.query_params, **kwargs}
        try:
            queryset = self.filter_queryset(**filters)
        except ValidationError:
            return Response(self.validation_error, status=400)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        idea_id = kwargs.get("pk")

        try:
            Idea.objects.get(id=idea_id)
        except ValidationError:
            validation_error = self.validation_error
            validation_error['fields'] = [
                {"idea_pk": "Needs to be uuid"}
            ]
            return Response(self.validation_error, status=400)
        except ObjectDoesNotExist:
            not_found_error = self.not_found_error
            not_found_error['fields'] = [
                {"idea_pk": "No idea with that uuid"}
            ]
            return Response(self.not_found_error, status=404)

        comment = request.data
        comment['idea_id'] = idea_id

        serializer = self.get_serializer(data=comment)
        if not serializer.is_valid():
            return Response(self.validation_error, status=400)
        serializer.save(owner=request.user)

        return Response(serializer.data)


class CommentDetailAPIView(APIView, ErrorsMixin, SerializerMixin):

    model = Comment
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        if self.request.method == 'PATCH':
            serializer.fields['idea_id'].read_only = True
        return serializer

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

        self.check_object_permissions(request, comment)
        new_comment = request.data

        serializer = self.get_serializer(
            data=new_comment, instance=comment, partial=True)
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
        self.check_object_permissions(request, comment)

        comment.delete()
        return Response()


class LikeAPIView(APIView, ErrorsMixin, SerializerMixin):
    model = Like
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def validate_publication_id(self, publication_id):
        idea = Idea.objects.filter(id=publication_id).first()
        comment = Comment.objects.filter(id=publication_id).first()

        if not (idea or comment):
            return ObjectDoesNotExist

        return idea or comment

    def get(self, request, *args, **kwargs):
        queryset = self.model.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        new_like = request.data
        publication_id = kwargs.get("pk")

        try:
            publication = self.validate_publication_id(publication_id)
        except ValidationError:
            return Response(self.validation_error, status=400)
        except ObjectDoesNotExist:
            return Response(self.not_found_error, status=404)

        like = user_liked(request.user, publication_id)

        if like:
            publication.likes = publication.likes - 1
            publication.save()
            like.delete()
            return Response()

        new_like['publication_id'] = publication_id
        serializer = self.get_serializer(data=new_like)
        if not serializer.is_valid():
            return Response(self.validation_error, status=400)

        publication.likes = publication.likes + 1
        publication.save()

        serializer.save(owner=request.user)
        return Response(serializer.data)


def user_liked(user, publication_id):
    query = Like.objects.filter(
        owner=user, publication_id=publication_id).first()

    return query
