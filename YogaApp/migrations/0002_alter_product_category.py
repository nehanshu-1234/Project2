# Generated by Django 5.0 on 2023-12-29 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YogaApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.IntegerField(choices=[(1, 'Common'), (2, 'Yoga Essentials'), (3, 'Clothing'), (4, 'Food'), (5, 'bodycare'), (6, 'Books'), (7, 'Blog')]),
        ),
    ]
