# Generated by Django 5.0.4 on 2024-05-05 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameapp', '0004_lista_amigos_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='jogo',
            name='media',
            field=models.FloatField(default=0),
        ),
    ]