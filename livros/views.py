import requests
from django.contrib import messages
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import LeituraForm, ResenhaForm
from .models import Leitura, Livro, Resenha
from .services import buscar_livros, buscar_por_id

CAMPOS_LIVRO = ['titulo', 'autor', 'capa_url', 'paginas', 'sinopse']


# ---------- Livro: as 4 telas do enunciado (listar, detalhar, criar, editar) ----------

class LivroListView(ListView):
    """A estante: todos os livros + um resumo do mês e do ano."""
    model = Livro
    template_name = 'livros/livro_list.html'
    context_object_name = 'livros'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        hoje = timezone.localdate()
        lidos = Leitura.objects.filter(status=Leitura.Status.LIDO)
        contexto['lidos_no_ano'] = lidos.filter(data_termino__year=hoje.year).count()
        contexto['lidos_no_mes'] = lidos.filter(
            data_termino__year=hoje.year, data_termino__month=hoje.month
        ).count()
        contexto['media_notas'] = Resenha.objects.aggregate(media=Avg('nota'))['media']
        return contexto


class LivroDetailView(DetailView):
    model = Livro
    template_name = 'livros/livro_detail.html'


class LivroCreateView(CreateView):
    model = Livro
    fields = CAMPOS_LIVRO
    template_name = 'livros/form.html'
    extra_context = {'titulo_pagina': 'Cadastrar livro'}
    # sem success_url: o Django usa Livro.get_absolute_url() depois de salvar


class LivroUpdateView(UpdateView):
    model = Livro
    fields = CAMPOS_LIVRO
    template_name = 'livros/form.html'
    extra_context = {'titulo_pagina': 'Editar livro'}


# ---------- Leitura e Resenha (criar e editar) ----------

class LeituraCreateView(CreateView):
    model = Leitura
    form_class = LeituraForm
    template_name = 'livros/form.html'
    extra_context = {'titulo_pagina': 'Registrar leitura'}

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['livro'] = get_object_or_404(Livro, pk=self.kwargs['livro_pk'])
        return contexto

    def form_valid(self, form):
        # O livro vem da URL (livro/<livro_pk>/leitura/nova/), não do formulário.
        form.instance.livro = get_object_or_404(Livro, pk=self.kwargs['livro_pk'])
        return super().form_valid(form)


class LeituraUpdateView(UpdateView):
    model = Leitura
    form_class = LeituraForm
    template_name = 'livros/form.html'
    extra_context = {'titulo_pagina': 'Atualizar leitura'}


class ResenhaCreateView(CreateView):
    model = Resenha
    form_class = ResenhaForm
    template_name = 'livros/form.html'
    extra_context = {'titulo_pagina': 'Escrever resenha'}

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['livro'] = get_object_or_404(Leitura, pk=self.kwargs['leitura_pk']).livro
        return contexto

    def form_valid(self, form):
        form.instance.leitura = get_object_or_404(Leitura, pk=self.kwargs['leitura_pk'])
        return super().form_valid(form)


class ResenhaUpdateView(UpdateView):
    model = Resenha
    form_class = ResenhaForm
    template_name = 'livros/form.html'
    extra_context = {'titulo_pagina': 'Editar resenha'}


# ---------- Busca no Google Books ----------

def buscar(request):
    """Lê o ?q= da URL, consulta a API e mostra os resultados."""
    termo = request.GET.get('q', '').strip()
    resultados = []
    erro = ''
    if termo:
        try:
            resultados = buscar_livros(termo)
        except requests.RequestException:
            erro = 'Não foi possível consultar o Google Books agora. Verifique a internet e tente de novo.'

    # IDs que já estão salvos, para mostrar "Já está na estante".
    na_estante = set(Livro.objects.exclude(google_id=None).values_list('google_id', flat=True))
    return render(request, 'livros/busca.html', {
        'termo': termo,
        'resultados': resultados,
        'erro': erro,
        'na_estante': na_estante,
    })


@require_POST
def adicionar(request, google_id):
    """Salva na estante o livro escolhido na busca (se ainda não estiver lá)."""
    livro = Livro.objects.filter(google_id=google_id).first()
    if livro is None:
        try:
            dados = buscar_por_id(google_id)
        except requests.RequestException:
            messages.error(request, 'Não foi possível buscar os dados desse livro. Tente de novo.')
            return redirect('buscar')
        livro = Livro.objects.create(**dados)
        messages.success(request, f'"{livro.titulo}" foi adicionado à estante.')
    return redirect(livro)  # vai para a página de detalhes (get_absolute_url)
