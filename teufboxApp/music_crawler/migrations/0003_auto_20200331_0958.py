# Generated by Django 3.0 on 2020-03-31 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_crawler', '0002_auto_20200331_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='bands',
            field=models.ManyToManyField(related_name='artists', to='music_crawler.Band'),
        ),
    ]
