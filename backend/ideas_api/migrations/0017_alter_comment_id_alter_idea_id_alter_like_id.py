# Generated by Django 4.0.5 on 2022-08-03 12:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ideas_api', '0016_alter_comment_id_alter_idea_id_alter_like_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('fdd7138c-55ad-4e07-a7be-9bfad69000a7'), primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='idea',
            name='id',
            field=models.UUIDField(default=uuid.UUID('398a5408-5c42-4fbe-8448-bfc020fd545d'), primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='like',
            name='id',
            field=models.UUIDField(default=uuid.UUID('fe4add21-243a-467d-a91d-ba97720bc038'), primary_key=True, serialize=False, unique=True),
        ),
    ]
