# Generated by Django 3.2.7 on 2021-09-11 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abhi', '0002_auto_20210911_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogposts',
            name='author_name',
            field=models.CharField(default=' ', max_length=120),
        ),
    ]