# Generated by Django 2.2.4 on 2022-07-19 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0002_auto_20220707_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='numero',
            field=models.CharField(max_length=12, verbose_name='Número'),
        ),
    ]
