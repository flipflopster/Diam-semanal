# Generated by Django 5.0.4 on 2024-05-05 15:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameapp', '0002_remove_comentario_data_remove_thread_data_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listautilizadorjogo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]