# Generated by Django 3.0.3 on 2020-02-12 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_post_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='created_date',
        ),
    ]