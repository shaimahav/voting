# Generated by Django 3.0.3 on 2020-02-19 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voters', '0005_adhar_photo_voteridcopy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='voterregisterid',
        ),
        migrations.RemoveField(
            model_name='voteridcopy',
            name='voterregisterid',
        ),
        migrations.DeleteModel(
            name='adhar',
        ),
        migrations.DeleteModel(
            name='photo',
        ),
        migrations.DeleteModel(
            name='voteridcopy',
        ),
        migrations.DeleteModel(
            name='voterregister',
        ),
    ]
