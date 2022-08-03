# Generated by Django 4.0.5 on 2022-08-03 12:42

import authentication.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('id', models.UUIDField(default=uuid.UUID('d060a053-41ec-4c86-bfa5-5cbefec81720'), primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=60, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('hide_email', models.BooleanField(default=True)),
                ('profile_image', models.ImageField(blank=True, default=authentication.models.get_default_profile_image, max_length=255, null=True, upload_to=authentication.models.get_profile_image_filepath)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
