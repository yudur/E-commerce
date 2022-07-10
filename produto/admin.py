from django.contrib import admin
from .models import Produto, Variacao


class VariacaoInline(admin.TabularInline):
    model = Variacao
    extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco_marketing', 'preco_marketing_promocional']
    list_display_links = ['nome']
    list_editable = ('preco_marketing', 'preco_marketing_promocional')
    list_filter = ['tipo']
    list_per_page = 10
    search_fields = ['nome', 'slug', 'descricao_curta', 'descricao_longa']
    inlines = [VariacaoInline]


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao)
