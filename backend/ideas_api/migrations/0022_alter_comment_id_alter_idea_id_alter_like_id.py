# Generated by Django 4.0.5 on 2022-08-08 12:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ideas_api', '0021_alter_comment_id_alter_idea_id_alter_like_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('906b818f-5ad6-4015-8af1-85cea00b1940'), primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='idea',
            name='id',
            field=models.UUIDField(default=uuid.UUID('2956b42e-a877-47d3-9a9d-e1dafd853e1d'), primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='like',
            name='id',
            field=models.UUIDField(default=uuid.UUID('97e7b64c-02d6-4d73-bb06-60edf066e8f7'), primary_key=True, serialize=False, unique=True),
        ),
    ]
