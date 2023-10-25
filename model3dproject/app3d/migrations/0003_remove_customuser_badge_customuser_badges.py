# Generated by Django 4.2.6 on 2023-10-24 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app3d', '0002_model3d_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='badge',
        ),
        migrations.AddField(
            model_name='customuser',
            name='badges',
            field=models.ManyToManyField(blank=True, to='app3d.badge'),
        ),
    ]
