# Generated by Django 3.0.4 on 2020-04-10 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_article_content_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='content_type',
        ),
    ]
