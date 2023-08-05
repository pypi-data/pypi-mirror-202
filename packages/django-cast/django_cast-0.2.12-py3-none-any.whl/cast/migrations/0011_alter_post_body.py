# Generated by Django 3.2.6 on 2021-08-13 08:40

import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks
from django.db import migrations

import cast.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("cast", "0010_rename_intro_blog_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "overview",
                        wagtail.core.blocks.StreamBlock(
                            [
                                ("heading", wagtail.core.blocks.CharBlock(form_classname="full title")),
                                ("paragraph", wagtail.core.blocks.RichTextBlock()),
                                ("image", wagtail.images.blocks.ImageChooserBlock(template="cast/image/image.html")),
                                ("gallery", cast.blocks.GalleryBlock(wagtail.images.blocks.ImageChooserBlock())),
                                ("embed", wagtail.embeds.blocks.EmbedBlock()),
                                (
                                    "video",
                                    cast.blocks.VideoChooserBlock(icon="media", template="cast/video/video.html"),
                                ),
                            ]
                        ),
                    ),
                    (
                        "detail",
                        wagtail.core.blocks.StreamBlock(
                            [
                                ("heading", wagtail.core.blocks.CharBlock(form_classname="full title")),
                                ("paragraph", wagtail.core.blocks.RichTextBlock()),
                                ("image", wagtail.images.blocks.ImageChooserBlock(template="cast/image.html")),
                                ("gallery", cast.blocks.GalleryBlock(wagtail.images.blocks.ImageChooserBlock())),
                                ("embed", wagtail.embeds.blocks.EmbedBlock()),
                                (
                                    "video",
                                    cast.blocks.VideoChooserBlock(icon="media", template="cast/video.html"),
                                ),
                            ]
                        ),
                    ),
                ]
            ),
        ),
    ]
