# Generated by Django 5.0 on 2024-01-05 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YogaApp', '0008_remove_order_is_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.IntegerField(choices=[(1, 'Yoga Essentials'), (2, 'Clothing'), (3, 'Food'), (4, 'bodycare'), (5, 'Books'), (6, 'Blog')]),
        ),
    ]