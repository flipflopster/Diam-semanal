# Generated by Django 5.0.3 on 2024-04-12 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votacao', '0002_aluno'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='profile_picture',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]