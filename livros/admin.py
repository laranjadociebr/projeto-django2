from django.contrib import admin

from .models import Leitura, Livro, Resenha


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'paginas', 'adicionado_em')
    search_fields = ('titulo', 'autor')


@admin.register(Leitura)
class LeituraAdmin(admin.ModelAdmin):
    list_display = ('livro', 'status', 'pagina_atual', 'vezes_lida', 'data_termino')
    list_filter = ('status',)
    search_fields = ('livro__titulo',)


@admin.register(Resenha)
class ResenhaAdmin(admin.ModelAdmin):
    list_display = ('leitura', 'nota', 'criada_em')
    list_filter = ('nota',)
    search_fields = ('leitura__livro__titulo',)
