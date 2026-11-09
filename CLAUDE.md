# Regras do projeto

Trabalho de faculdade em dupla (entrega 16/11/2026). Estante de livros LOCAL, sem login (só o admin). Apenas Python + Django (MTV), sem React. Windows/PowerShell, venv em `venv/`.

- Models: Livro, Leitura (FK livro), Resenha (FK leitura). Admin com list_display, search_fields, list_filter.
- Feito: CBVs de listar/detalhar/criar/editar (Livro) e criar/editar (Leitura, Resenha); busca no Google Books em `livros/services.py` (requests, chave no `.env` via python-dotenv); estante com rolagem horizontal; modo claro/escuro; resumo do mês/ano; testes em `livros/tests.py` (API simulada).
- Templates: `templates/base.html` (projeto) e `livros/templates/livros/`. CSS em `livros/static/livros/estilo.css`. Sem CDN: tudo funciona offline, menos a busca.

## Como trabalhar
- Apresentar plano e esperar aprovação antes de editar.
- Ser econômico: não explorar o repo inteiro, não instalar pacotes não pedidos, respostas curtas.
- Explicar cada passo em 1–2 linhas (usuário está aprendendo).
- Git: commits pequenos em português; sem push sem pedido; trabalho novo em `feature/<nome>`; nunca versionar `.env` nem `db.sqlite3`.
