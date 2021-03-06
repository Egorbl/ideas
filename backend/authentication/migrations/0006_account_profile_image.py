# Generated by Django 4.0.5 on 2022-07-18 12:37

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_remove_account_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_image',
            field=models.ImageField(blank=True, default=authentication.models.get_default_profile_image, max_length=255, null=True, upload_to=''),
        ),
    ]
