# Generated by Django 3.0.5 on 2021-03-06 11:22

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Random',
            fields=[
                ('post_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(blank=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('post_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=80)),
                ('description', models.CharField(max_length=200)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.CharField(choices=[('ทั่วไป', 'ทั่วไป'), ('ความรัก', 'ความรัก'), ('ปรึกษา', 'ปรึกษา'), ('การเรียน', 'การเรียน')], default='ทั่วไป', max_length=200)),
                ('user_id', models.IntegerField(blank=True, default=None)),
                ('picture', models.CharField(max_length=200, null=True)),
                ('pic_name', models.CharField(max_length=100)),
                ('like_count', models.BigIntegerField(default='0')),
                ('liked', models.ManyToManyField(blank=True, default=None, related_name='like', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]