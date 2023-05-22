# Generated by Django 3.0.3 on 2020-03-02 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('siteadmin', '0009_symbol_symbolname'),
        ('candidates', '0009_auto_20200302_1231'),
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
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('assemblyname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteadmin.assembly')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteadmin.district')),
                ('partyid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteadmin.party')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteadmin.landmark')),
                ('stateid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteadmin.state')),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteadmin.symbol')),
            ],
        ),
        migrations.CreateModel(
            name='voteridcopy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voteridcopy', models.FileField(upload_to='')),
                ('candidateregisterid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidates.candidateregister')),
            ],
        ),
        migrations.CreateModel(
            name='proposertb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname1', models.CharField(max_length=20)),
                ('voterid1', models.CharField(max_length=20)),
                ('pname2', models.CharField(max_length=20)),
                ('voterid2', models.CharField(max_length=20)),
                ('candidateregisterid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidates.candidateregister')),
            ],
        ),
        migrations.CreateModel(
            name='photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.FileField(upload_to='')),
                ('candidateregisterid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidates.candidateregister')),
            ],
        ),
        migrations.CreateModel(
            name='adhar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adhar', models.FileField(upload_to='')),
                ('candidateregisterid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidates.candidateregister')),
            ],
        ),
    ]
