# Generated by Django 3.0.3 on 2020-02-12 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_post_pre_moderation'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]