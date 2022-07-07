from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
import re
from utils.validacpf import valida_cpf


class Perfil(models.Model):
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='usuário')
    idade = models.PositiveIntegerField(verbose_name='idade')
    data_nacimento = models.DateField(verbose_name='data de nacimento')
    cpf = models.CharField(max_length=11, verbose_name='CPF')
    endereco = models.CharField(max_length=50, verbose_name='endereço')
    numero = models.CharField(max_length=12, verbose_name='telefone')
    complemento = models.CharField(max_length=30, verbose_name='complemento')
    bairro = models.CharField(max_length=30, verbose_name='bairro')
    cep = models.CharField(max_length=8, verbose_name='CEP')
    cidade = models.CharField(max_length=30, verbose_name='cidade')
    estado = models.CharField(
        verbose_name='estado',
        max_length=2,
        default='SP',
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self) -> str:
        return f'{self.usuario}'

    def clean(self) -> None:
        error_messages = {}
        
        if self.numero.isalpha():
            error_messages['numero'] = 'digite um telefone válido.'

        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'digite um CPF válido.'

        if re.search(r'[^0-9]', self.cep) or len(self.cep) != 8:
            error_messages['cep'] = 'CEP inválido, digite os 8 digitos do CEP.'

        if error_messages:
            raise ValidationError(error_messages)