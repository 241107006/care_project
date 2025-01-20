# Generated by Django 5.1.3 on 2024-12-23 01:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('care_app', '0010_ordertaken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertaken',
            name='order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='taken_orders', to='care_app.order'),
        ),
    ]
