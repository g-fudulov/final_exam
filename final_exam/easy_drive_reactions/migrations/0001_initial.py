# Generated by Django 4.2.3 on 2023-08-16 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('easy_drive_profile', '0001_initial'),
        ('easy_drive_blog', '0001_initial'),
        ('easy_drive_ad', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='easy_drive_blog.blogpost')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='easy_drive_profile.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=100)),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='easy_drive_ad.ad')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='easy_drive_profile.profile')),
            ],
        ),
    ]