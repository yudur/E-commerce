# Generated by Django 2.2.4 on 2022-07-21 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0010_auto_20220718_2118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='imagem_2',
        ),
        migrations.RemoveField(
            model_name='produto',
            name='imagem_3',
        ),
    ]
