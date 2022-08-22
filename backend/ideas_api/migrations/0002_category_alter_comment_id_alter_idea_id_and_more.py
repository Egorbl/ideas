# Generated by Django 4.1 on 2022-08-19 14:38

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("ideas_api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=60, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name="comment",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="idea",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="idea",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="ideas", to="ideas_api.tag"
            ),
        ),
        migrations.AlterField(
            model_name="like",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="idea",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ideas",
                to="ideas_api.category",
            ),
        ),
    ]