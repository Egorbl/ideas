# Generated by Django 4.0.5 on 2022-07-18 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_account_is_stuff_account_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='hide_email',
            field=models.BooleanField(default=True),
        ),
    ]