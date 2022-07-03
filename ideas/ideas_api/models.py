from django.db import models

from authentication.models import Account


programming = "programming"
art = "art"
science = "science"

IDEA_CATEGORY_CHOICES = (
    (programming, "Programming"),
    (art, "Art"),
    (science, "Science"),
)


class Tag(models.Model):
    """Model for Tag"""
    name = models.CharField(max_length=60, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Idea(models.Model):
    id = models.UUIDField(primary_key=True, unique=True)
    owner = models.ForeignKey(
        to=Account, related_name="ideas", on_delete=models.CASCADE)
    category = models.CharField(max_length=60, choices=IDEA_CATEGORY_CHOICES)
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=10000)
    date_added = models.DateTimeField(auto_now_add=True, db_index=True)
    date_updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(to=Tag, related_name="ideas")
    likes = models.IntegerField(default=0)
    is_actual = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, unique=True)
    idea_id = models.ForeignKey(
        to=Idea, related_name="comments", on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        to=Account, related_name="comments", on_delete=models.CASCADE
    )
    content = models.TextField(max_length=1000)
    date_added = models.DateTimeField(auto_now_add=True)
    is_updated = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.content


class Like(models.Model):
    id = models.UUIDField(primary_key=True, unique=True)
    owner = models.ForeignKey(
        to=Account, related_name="likes", on_delete=models.CASCADE
    )
    publication_id = models.CharField(max_length=36)
