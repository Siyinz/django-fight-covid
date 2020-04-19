# Generated by Django 3.0.4 on 2020-04-18 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0011_auto_20200418_2215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hit',
            name='ip',
        ),
        migrations.RemoveField(
            model_name='hit',
            name='session',
        ),
        migrations.AddField(
            model_name='hit',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
