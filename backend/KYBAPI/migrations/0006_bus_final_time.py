# Generated by Django 5.1.3 on 2025-04-08 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KYBAPI', '0005_destination_up_loc_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='final_time',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
