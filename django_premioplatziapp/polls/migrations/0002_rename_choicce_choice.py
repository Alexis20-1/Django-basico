# Generated by Django 5.0.4 on 2024-04-22 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Choicce',
            new_name='Choice',
        ),
    ]