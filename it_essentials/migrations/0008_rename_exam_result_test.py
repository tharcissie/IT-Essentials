# Generated by Django 3.2 on 2021-05-03 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('it_essentials', '0007_auto_20210503_1556'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='exam',
            new_name='test',
        ),
    ]