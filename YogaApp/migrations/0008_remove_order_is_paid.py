# Generated by Django 5.0 on 2024-01-05 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('YogaApp', '0007_order_is_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_paid',
        ),
    ]
