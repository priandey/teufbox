# Generated by Django 3.0 on 2020-05-19 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_crawler', '0008_delete_downloadlogs'),
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
            ],
        ),
    ]