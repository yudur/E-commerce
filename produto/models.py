from distutils.command.upload import upload
from django.db import models
from PIL import Image
import os
from django.conf import settings
from django.utils.text import slugify
from random import randint


class Produto(models.Model):
    nome = models.CharField(max_length=255, verbose_name='nome')
    descricao_curta = models.TextField(
        max_length=200, verbose_name='descrição curta')
    descricao_longa = models.TextField(verbose_name='descrição longa')
    imagem_1 = models.ImageField(upload_to='produto_imagem/%Y/%m')
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=265)
    preco_marketing = models.FloatField(verbose_name='preço marketing')
    preco_marketing_promocional = models.FloatField(
        default=0, verbose_name='preço marketing promocional')
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        ),
    )

    def save(self, *args, **kwargs):
        preco_formatado, preco_promo_formatado = round(
            self.preco_marketing, 2), round(self.preco_marketing_promocional, 2)

        self.preco_marketing = preco_formatado
        self.preco_marketing_promocional = preco_promo_formatado

        if not self.slug:
            slug = f'{slugify(self.nome)}-{randint(100000, 999999)}'
            self.slug = slug

        super().save(*args, **kwargs)

        if self.imagem_1:
            self.resize_img(self.imagem_1, 800)

    @staticmethod
    def resize_img(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_heigth = img_pil.size

        if original_width <= new_width:
            img_pil.close()
            return

        new_heigth = round((new_width * original_heigth) / original_width)

        new_img = img_pil.resize((new_heigth, new_heigth), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=60
        )

    def __str__(self) -> str:
        return self.nome


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'

    def save(self, *args, **kwargs):
        preco_formatado, preco_promo_formatado = round(
            self.preco, 2), round(self.preco_promocional, 2)

        self.preco = preco_formatado
        self.preco_promocional = preco_promo_formatado

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.nome or self.produto.nome
