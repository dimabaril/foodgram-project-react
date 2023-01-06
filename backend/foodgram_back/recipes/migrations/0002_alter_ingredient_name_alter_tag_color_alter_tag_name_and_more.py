# Generated by Django 4.1.4 on 2023-01-04 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(default='#ffffff', max_length=7, unique=True, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.CharField(max_length=50, unique=True, verbose_name='Slug'),
        ),
    ]
