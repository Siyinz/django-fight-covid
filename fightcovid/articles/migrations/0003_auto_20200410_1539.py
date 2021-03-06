# Generated by Django 3.0.4 on 2020-04-10 15:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20200410_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='source',
            field=models.CharField(default='SOME STRING', max_length=200),
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(5, 'Author name must be greater than 5 characters')]),
        ),
    ]
