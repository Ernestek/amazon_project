# Generated by Django 4.2.2 on 2023-07-13 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=512, unique=True)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
        ),
        migrations.CreateModel(
            name='ReviewsInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=256)),
                ('text', models.TextField()),
                ('date', models.CharField(max_length=100)),
                ('count_stars', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Review Info',
                'verbose_name_plural': 'Reviews Info',
            },
        ),
    ]
