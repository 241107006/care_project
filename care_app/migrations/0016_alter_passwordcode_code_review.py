# Generated by Django 5.1.3 on 2025-03-26 19:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('care_app', '0015_passwordcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordcode',
            name='code',
            field=models.CharField(max_length=6, unique=True),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.PositiveIntegerField(blank=True, null=True, verbose_name='Звезды')),
                ('text', models.TextField()),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='care_app.order')),
            ],
        ),
    ]
