# Generated by Django 3.0.3 on 2020-03-02 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0008_auto_20200226_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidateregister',
            name='assemblyname',
        ),
        migrations.RemoveField(
            model_name='candidateregister',
            name='partyid',
        ),
        migrations.RemoveField(
            model_name='candidateregister',
            name='symbol',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='candidateregisterid',
        ),
        migrations.RemoveField(
            model_name='proposertb',
            name='candidateregisterid',
        ),
        migrations.RemoveField(
            model_name='voteridcopy',
            name='candidateregisterid',
        ),
        migrations.DeleteModel(
            name='adhar',
        ),
        migrations.DeleteModel(
            name='candidateregister',
        ),
        migrations.DeleteModel(
            name='photo',
        ),
        migrations.DeleteModel(
            name='proposertb',
        ),
        migrations.DeleteModel(
            name='voteridcopy',
        ),
    ]
