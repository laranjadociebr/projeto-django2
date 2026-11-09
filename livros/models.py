from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Livro(models.Model):
    """Um livro da estante. Vem da busca no Google Books ou do cadastro manual."""

    google_id = models.CharField('ID no Google Books', max_length=50, unique=True, null=True, blank=True)
    titulo = models.CharField('título', max_length=200)
    autor = models.CharField(max_length=200, blank=True)
    capa_url = models.URLField('capa (URL)', blank=True)
    paginas = models.PositiveIntegerField('páginas', null=True, blank=True)
    sinopse = models.TextField(blank=True)
    adicionado_em = models.DateTimeField('adicionado em', auto_now_add=True)

    class Meta:
        ordering = ['titulo']

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        # Para onde as telas de criar/editar mandam depois de salvar.
        return reverse('livro_detail', args=[self.pk])


class Leitura(models.Model):
    """Uma leitura de um livro: status, onde parei e quantas vezes já li."""

    class Status(models.TextChoices):
        QUERO_LER = 'quero_ler', 'Quero ler'
        LENDO = 'lendo', 'Lendo'
        LIDO = 'lido', 'Lido'

    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='leituras')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.QUERO_LER)
    pagina_atual = models.PositiveIntegerField('página atual', default=0)
    vezes_lida = models.PositiveIntegerField('vezes que já li', default=0)
    data_inicio = models.DateField('início', null=True, blank=True)
    data_termino = models.DateField('término', null=True, blank=True)

    class Meta:
        ordering = ['-id']  # a leitura mais recente primeiro

    def __str__(self):
        return f'{self.livro} ({self.get_status_display()})'

    def get_absolute_url(self):
        return self.livro.get_absolute_url()

    def progresso(self):
        """Porcentagem lida (0 a 100), usada na barra de progresso."""
        if not self.livro.paginas:
            return 0
        return min(100, round(self.pagina_atual * 100 / self.livro.paginas))


class Resenha(models.Model):
    """O que achei do livro em uma leitura: contexto, pontos fortes e fracos, nota."""

    leitura = models.ForeignKey(Leitura, on_delete=models.CASCADE, related_name='resenhas')
    contexto = models.TextField(blank=True, help_text='Por que li, em que momento, o que esperava.')
    pontos_fortes = models.TextField('pontos fortes', blank=True)
    pontos_fracos = models.TextField('pontos fracos', blank=True)
    nota = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text='De 0 a 10.',
    )
    criada_em = models.DateTimeField('criada em', auto_now_add=True)

    class Meta:
        ordering = ['-criada_em']

    def __str__(self):
        return f'Resenha de {self.leitura.livro} (nota {self.nota})'

    def get_absolute_url(self):
        return self.leitura.livro.get_absolute_url()
