# Generated by Django 3.2.7 on 2021-09-20 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abhi', '0004_alter_blogposts_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogposts',
            name='image',
            field=models.ImageField(default='', upload_to='home/images'),
        ),
    ]