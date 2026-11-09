"""Conversa com a API do Google Books (a única parte do app que usa a internet)."""
import requests
from django.conf import settings
from django.utils.html import strip_tags

URL_API = 'https://www.googleapis.com/books/v1/volumes'


def _parametros(extra=None):
    """Junta os parâmetros da requisição e a chave, se houver uma no .env."""
    params = dict(extra or {})
    if settings.GOOGLE_BOOKS_API_KEY:
        params['key'] = settings.GOOGLE_BOOKS_API_KEY
    return params


def _para_dicionario(item):
    """Transforma um volume do JSON do Google nos campos do model Livro."""
    info = item.get('volumeInfo', {})
    capa = info.get('imageLinks', {}).get('thumbnail', '')
    return {
        'google_id': item.get('id', ''),
        'titulo': info.get('title', 'Sem título')[:200],
        'autor': ', '.join(info.get('authors', []))[:200],
        'capa_url': capa.replace('http://', 'https://'),
        'paginas': info.get('pageCount') or None,
        'sinopse': strip_tags(info.get('description', '')),
    }


def buscar_livros(termo, quantidade=12):
    """Pesquisa um termo (título, autor...) e devolve uma lista de livros."""
    resposta = requests.get(
        URL_API,
        params=_parametros({'q': termo, 'maxResults': quantidade, 'printType': 'books'}),
        timeout=10,
    )
    resposta.raise_for_status()  # erro HTTP (ex.: 429 = cota estourada) vira exceção
    return [_para_dicionario(item) for item in resposta.json().get('items', [])]


def buscar_por_id(google_id):
    """Busca um único livro pelo ID do Google (usado ao adicionar à estante)."""
    resposta = requests.get(f'{URL_API}/{google_id}', params=_parametros(), timeout=10)
    resposta.raise_for_status()
    return _para_dicionario(resposta.json())
