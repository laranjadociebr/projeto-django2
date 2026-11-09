from unittest.mock import Mock, patch

import requests
from django.test import TestCase
from django.urls import reverse

from .models import Leitura, Livro, Resenha

# Um volume no formato que o Google Books devolve (resumido).
VOLUME = {
    'id': 'abc123',
    'volumeInfo': {
        'title': 'Color and Light',
        'authors': ['James Gurney'],
        'pageCount': 224,
        'description': '<p>Um guia para pintores realistas.</p>',
        'imageLinks': {'thumbnail': 'http://books.google.com/capa.jpg'},
    },
}


def resposta_falsa(json):
    """Simula o requests.get sem usar a internet."""
    return Mock(status_code=200, json=Mock(return_value=json), raise_for_status=Mock())


class TelasTests(TestCase):
    def test_estante_vazia(self):
        resposta = self.client.get(reverse('livro_list'))
        self.assertContains(resposta, 'Nenhum livro na estante')

    def test_cadastrar_livro_a_mao(self):
        resposta = self.client.post(reverse('livro_create'), {'titulo': 'Dom Casmurro', 'autor': 'Machado de Assis'})
        livro = Livro.objects.get()
        self.assertRedirects(resposta, reverse('livro_detail', args=[livro.pk]))

    def test_leitura_resenha_e_resumo(self):
        livro = Livro.objects.create(titulo='Dom Casmurro', paginas=200)
        self.client.post(reverse('leitura_create', args=[livro.pk]), {
            'status': 'lido', 'pagina_atual': 200, 'vezes_lida': 1, 'data_termino': '2026-11-01',
        })
        leitura = Leitura.objects.get()
        self.assertEqual(leitura.progresso(), 100)
        self.client.post(reverse('resenha_create', args=[leitura.pk]), {'nota': 9, 'pontos_fortes': 'Capitu'})
        self.assertEqual(Resenha.objects.get().nota, 9)
        resposta = self.client.get(reverse('livro_detail', args=[livro.pk]))
        self.assertContains(resposta, 'Nota 9/10')


class BuscaTests(TestCase):
    @patch('livros.services.requests.get')
    def test_busca_mostra_resultados(self, get_falso):
        get_falso.return_value = resposta_falsa({'items': [VOLUME]})
        resposta = self.client.get(reverse('buscar'), {'q': 'color and light'})
        self.assertContains(resposta, 'Color and Light')
        self.assertContains(resposta, 'Adicionar à estante')

    @patch('livros.services.requests.get', side_effect=requests.ConnectionError)
    def test_busca_sem_internet(self, get_falso):
        resposta = self.client.get(reverse('buscar'), {'q': 'qualquer'})
        self.assertContains(resposta, 'Não foi possível consultar o Google Books')

    @patch('livros.services.requests.get')
    def test_adicionar_nao_duplica(self, get_falso):
        get_falso.return_value = resposta_falsa(VOLUME)
        self.client.post(reverse('adicionar', args=['abc123']))
        self.client.post(reverse('adicionar', args=['abc123']))
        livro = Livro.objects.get()  # falha se tiver criado dois
        self.assertEqual(livro.autor, 'James Gurney')
        self.assertEqual(livro.sinopse, 'Um guia para pintores realistas.')
        self.assertTrue(livro.capa_url.startswith('https://'))
