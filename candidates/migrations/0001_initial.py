# Generated by Django 3.0.3 on 2020-02-23 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='candidateregister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=20)),
                ('dateofbirth', models.CharField(max_length=20)),
                ('adharno', models.CharField(max_length=20)),
                ('voterid', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=20)),
                ('mobile', models.CharField(max_length=20)),
            ],
        ),
    ]
