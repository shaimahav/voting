# Generated by Django 3.0.3 on 2020-03-02 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteadmin', '0008_symbol'),
    ]

    operations = [
        migrations.AddField(
            model_name='symbol',
            name='symbolname',
            field=models.CharField(default='name', max_length=20),
        ),
    ]
