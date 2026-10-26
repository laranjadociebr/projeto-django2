# Regras do projeto

Trabalho de faculdade em dupla (entrega 16/11/2026). Estante de livros LOCAL, sem login (só o admin). Apenas Python + Django (MTV), sem React. Windows/PowerShell, venv em `venv/`.

- Models: Livro, Leitura (FK livro), Resenha (FK leitura). Admin com list_display, search_fields, list_filter. Templates de listar/detalhar/criar/editar/excluir via CBVs.
- Planejado: busca na API Google Books (requests, chave no `.env`, atribuição ao Google), estante com rolagem horizontal, modo claro/escuro, cadastro manual.

## Como trabalhar
- Apresentar plano e esperar aprovação antes de editar.
- Ser econômico: não explorar o repo inteiro, não instalar pacotes não pedidos, respostas curtas.
- Explicar cada passo em 1–2 linhas (usuário está aprendendo).
- Git: commits pequenos em português; sem push sem pedido; trabalho novo em `feature/<nome>`; nunca versionar `.env` nem `db.sqlite3`.
