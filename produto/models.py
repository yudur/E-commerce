from distutils.command.upload import upload
from email.policy import default
from pickletools import optimize
from tabnanny import verbose
from django.db import models
from PIL import Image
import os
from django.conf import settings


class Produto(models.Model):
    nome = models.CharField(max_length=255, verbose_name='nome')
    descricao_curta = models.TextField(max_length=100, verbose_name='descrição curta')
    descricao_longa = models.TextField(verbose_name='descrição longa')
    imagem_1 = models.ImageField(upload_to='produto_imagem/%Y/%m')
    imagem_2 = models.ImageField(upload_to='produto_imagem/%Y/%m', blank=True, null=True)
    imagem_3 = models.ImageField(upload_to='produto_imagem/%Y/%m', blank=True, null=True)
    slug = models.SlugField(unique=True)
    preco_marketing = models.FloatField(verbose_name='preço marketing')
    preco_marketing_promocional = models.FloatField(default=0, verbose_name='preço marketing promocional')
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variação'),
            ('S', 'Simples'),
        ),
    )


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.imagem_1:
            self.resize_img(self.imagem_1, 800)

        if self.imagem_2:
            self.resize_img(self.imagem_2, 800)

        if self.imagem_3:
            self.resize_img(self.imagem_3, 800)


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
    nome = models.CharField(max_length=100)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)


    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'


    def __str__(self) -> str:
        return self.nome or self.produto.nome
