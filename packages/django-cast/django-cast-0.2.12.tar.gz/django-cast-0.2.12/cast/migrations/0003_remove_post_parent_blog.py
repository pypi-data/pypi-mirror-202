# Generated by Django 3.1.2 on 2020-10-24 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cast", "0002_remove_blog_description"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="parent_blog",
        ),
    ]
