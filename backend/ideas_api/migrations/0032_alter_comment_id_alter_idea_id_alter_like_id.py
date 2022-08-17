# Generated by Django 4.1 on 2022-08-15 20:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ideas_api', '0031_alter_comment_id_alter_idea_id_alter_like_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('6c546de8-7112-4a1e-a986-eae8903fbdb4'), primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='idea',
            name='id',
            field=models.UUIDField(default=uuid.UUID('963b481d-3403-48c3-8e6c-19ffb37f2b86'), primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='like',
            name='id',
            field=models.UUIDField(default=uuid.UUID('2f2c9496-19f1-406a-a411-ec6bc22b5df0'), primary_key=True, serialize=False, unique=True),
        ),
    ]