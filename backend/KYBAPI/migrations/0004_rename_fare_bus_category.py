# Generated by Django 5.1.3 on 2025-01-12 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KYBAPI', '0003_bus_service_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bus',
            old_name='fare',
            new_name='category',
        ),
    ]
