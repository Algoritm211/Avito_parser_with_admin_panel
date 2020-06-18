# Generated by Django 3.0.3 on 2020-06-17 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avito_parser_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AddField(
            model_name='product',
            name='currency',
            field=models.TextField(default='₽', verbose_name='Валюта'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.URLField(unique=True, verbose_name='Cсылка на объявление'),
        ),
    ]
