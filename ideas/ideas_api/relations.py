from rest_framework.serializers import RelatedField
from .models import Tag


class TagRelatedField(RelatedField):

    def to_representation(self, tag):
        return tag.name

    def get_queryset(self):
        return Tag.objects.all()
