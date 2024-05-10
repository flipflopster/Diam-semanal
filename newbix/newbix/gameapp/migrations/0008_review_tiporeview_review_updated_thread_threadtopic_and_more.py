# Generated by Django 5.0.4 on 2024-05-10 10:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameapp', '0007_listautilizadorjogo_last_altered'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='tipoReview',
            field=models.CharField(choices=[('MF', 'Mixed Feelings'), ('RC', 'Recommended'), ('DR', 'Not Recommended')], default=django.utils.timezone.now, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='thread',
            name='threadTopic',
            field=models.CharField(choices=[('GB', 'Game Build'), ('SG', 'Strategy'), ('CP', 'Competitive'), ('MO', 'Modding'), ('CO', 'Completion'), ('GU', 'Game Updates'), ('GE', 'Game Events'), ('LO', 'Lore'), ('ST', 'Soundtrack'), ('GR', 'Graphics'), ('GM', 'Game Mechanics'), ('EE', 'Easter Eggs'), ('OT', 'Other')], default='OT', max_length=2),
        ),
        migrations.AddField(
            model_name='thread',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='utilizador',
            name='genero',
            field=models.CharField(default='Not Specified', max_length=50),
        ),
    ]