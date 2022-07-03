# Generated by Django 4.0.5 on 2022-07-03 19:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=60, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, unique=True)),
                ('publication_id', models.CharField(max_length=36)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, unique=True)),
                ('category', models.CharField(choices=[('programming', 'Programming'), ('art', 'Art'), ('science', 'Science')], max_length=60)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(max_length=10000)),
                ('date_added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('likes', models.IntegerField(default=0)),
                ('is_actual', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ideas', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(related_name='ideas', to='ideas_api.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, unique=True)),
                ('content', models.TextField(max_length=1000)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('is_updated', models.BooleanField(default=False)),
                ('likes', models.IntegerField(default=0)),
                ('idea_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ideas_api.idea')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
