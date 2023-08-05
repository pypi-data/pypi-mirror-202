# Generated by Django 4.1.4 on 2023-01-19 05:50

import cast.blocks
from django.db import migrations
import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("cast", "0025_add_performance_indicators"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Request",
        ),
        migrations.AlterField(
            model_name="post",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "overview",
                        wagtail.blocks.StreamBlock(
                            [
                                ("heading", wagtail.blocks.CharBlock(form_classname="full title")),
                                ("paragraph", wagtail.blocks.RichTextBlock()),
                                (
                                    "code",
                                    wagtail.blocks.StructBlock(
                                        [
                                            (
                                                "language",
                                                wagtail.blocks.CharBlock(help_text="The language of the code block"),
                                            ),
                                            (
                                                "source",
                                                wagtail.blocks.TextBlock(
                                                    help_text="The source code of the block", rows=8
                                                ),
                                            ),
                                        ],
                                        icon="code",
                                    ),
                                ),
                                ("image", wagtail.images.blocks.ImageChooserBlock(template="cast/image/image.html")),
                                ("gallery", cast.blocks.GalleryBlock(wagtail.images.blocks.ImageChooserBlock())),
                                ("embed", wagtail.embeds.blocks.EmbedBlock()),
                                (
                                    "video",
                                    cast.blocks.VideoChooserBlock(icon="media", template="cast/video/video.html"),
                                ),
                                (
                                    "audio",
                                    cast.blocks.AudioChooserBlock(icon="media", template="cast/audio/audio.html"),
                                ),
                            ]
                        ),
                    ),
                    (
                        "detail",
                        wagtail.blocks.StreamBlock(
                            [
                                ("heading", wagtail.blocks.CharBlock(form_classname="full title")),
                                ("paragraph", wagtail.blocks.RichTextBlock()),
                                (
                                    "code",
                                    wagtail.blocks.StructBlock(
                                        [
                                            (
                                                "language",
                                                wagtail.blocks.CharBlock(help_text="The language of the code block"),
                                            ),
                                            (
                                                "source",
                                                wagtail.blocks.TextBlock(
                                                    help_text="The source code of the block", rows=8
                                                ),
                                            ),
                                        ],
                                        icon="code",
                                    ),
                                ),
                                ("image", wagtail.images.blocks.ImageChooserBlock(template="cast/image/image.html")),
                                ("gallery", cast.blocks.GalleryBlock(wagtail.images.blocks.ImageChooserBlock())),
                                ("embed", wagtail.embeds.blocks.EmbedBlock()),
                                (
                                    "video",
                                    cast.blocks.VideoChooserBlock(icon="media", template="cast/video/video.html"),
                                ),
                                (
                                    "audio",
                                    cast.blocks.AudioChooserBlock(icon="media", template="cast/audio/audio.html"),
                                ),
                            ]
                        ),
                    ),
                ],
                use_json_field=True,
            ),
        ),
    ]
