# Generated by Django 5.1.3 on 2024-12-08 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('care_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMSCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('code', models.CharField(max_length=6)),
            ],
        ),
    ]
