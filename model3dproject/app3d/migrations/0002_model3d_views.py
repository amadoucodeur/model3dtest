# Generated by Django 4.2.6 on 2023-10-23 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app3d', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='model3d',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]