# Generated by Django 3.0.3 on 2020-02-11 07:13

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_post_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='text',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
