# Generated by Django 4.2.3 on 2023-08-05 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easy_drive', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='price',
            field=models.PositiveIntegerField(default=3434),
            preserve_default=False,
        ),
    ]
