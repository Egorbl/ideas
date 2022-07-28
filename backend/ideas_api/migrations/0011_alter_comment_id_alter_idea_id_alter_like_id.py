# Generated by Django 4.0.5 on 2022-07-28 01:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ideas_api', '0010_category_alter_comment_id_alter_idea_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('17fedc22-c7ad-4d61-9f21-3d4217db0d3b'), primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='idea',
            name='id',
            field=models.UUIDField(default=uuid.UUID('ffd2f329-c18a-41c7-b803-a38f63e61f45'), primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='like',
            name='id',
            field=models.UUIDField(default=uuid.UUID('137b7324-2c00-492e-b9c5-625a10b2999a'), primary_key=True, serialize=False, unique=True),
        ),
    ]
