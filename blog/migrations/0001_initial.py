# Generated by Django 3.2.15 on 2022-09-18 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='タイトル')),
                ('content', models.TextField(blank=True, verbose_name='本文')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('nickname', models.CharField(default=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL), max_length=200, verbose_name='ニックネーム')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(default='etc', on_delete=django.db.models.deletion.CASCADE, to='blog.category')),
            ],
        ),
    ]