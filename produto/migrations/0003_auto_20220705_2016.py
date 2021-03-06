# Generated by Django 2.2.4 on 2022-07-05 23:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0002_auto_20220705_2000'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produto',
            old_name='imagem',
            new_name='imagem_2',
        ),
        migrations.AddField(
            model_name='produto',
            name='imagem_1',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='produto_imagem/%Y/%m'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produto',
            name='imagem_3',
            field=models.ImageField(blank=True, null=True, upload_to='produto_imagem/%Y/%m'),
        ),
        migrations.CreateModel(
            name='Variacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('preco', models.FloatField()),
                ('preco_promocional', models.FloatField(default=0)),
                ('estoque', models.PositiveIntegerField(default=1)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produto.Produto')),
            ],
            options={
                'verbose_name': 'Variação',
                'verbose_name_plural': 'Variações',
            },
        ),
    ]
