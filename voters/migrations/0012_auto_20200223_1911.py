# Generated by Django 3.0.3 on 2020-02-23 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voters', '0011_auto_20200223_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voterregister',
            name='confirmpassword',
            field=models.CharField(default='confirm', max_length=20),
        ),
    ]
