# Generated by Django 4.1 on 2022-08-15 17:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ideas_api', '0026_alter_comment_id_alter_idea_id_alter_like_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('72e09232-a625-4ce6-abbc-970cbc75668b'), primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='idea',
            name='id',
            field=models.UUIDField(default=uuid.UUID('0d750fb7-c3a1-4e0f-be70-8db6d49b906f'), primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='like',
            name='id',
            field=models.UUIDField(default=uuid.UUID('ad5db732-3c97-4063-b260-121bd7d350f7'), primary_key=True, serialize=False, unique=True),
        ),
    ]
