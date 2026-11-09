# projeto-django2: Minha Estante

Estante de livros local feita com Django (MTV). Busca livros no Google Books, guarda na estante, registra leituras (status, página onde parou, quantas vezes leu) e resenhas (contexto, pontos fortes e fracos, nota de 0 a 10). Roda só no seu computador, sem login (o `/admin` usa o superusuário).

## Como rodar (Windows / PowerShell)

```powershell
git clone https://github.com/laranjadociebr/projeto-django2.git
cd projeto-django2
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env             # depois coloque a chave: GOOGLE_BOOKS_API_KEY=sua_chave
python manage.py migrate
python manage.py createsuperuser   # para acessar o /admin
python manage.py runserver
```

Acesse http://127.0.0.1:8000/ (admin em http://127.0.0.1:8000/admin/).

A chave da API é opcional: sem ela a busca funciona com uma cota diária menor. Nunca coloque a chave no Git (o `.env` já está no `.gitignore`).

## Telas

| Endereço | Tela |
|---|---|
| `/` | Estante (listar livros) + resumo do mês e do ano |
| `/livro/novo/` | Cadastrar livro à mão |
| `/livro/<id>/` | Detalhes do livro, leituras e resenhas |
| `/livro/<id>/editar/` | Editar livro |
| `/livro/<id>/leitura/nova/` e `/leitura/<id>/editar/` | Registrar e atualizar leitura |
| `/leitura/<id>/resenha/nova/` e `/resenha/<id>/editar/` | Escrever e editar resenha |
| `/buscar/?q=...` | Busca no Google Books e botão "Adicionar à estante" |
| `/admin/` | Painel administrativo |

## Testes

```powershell
python manage.py test livros
```

Os testes simulam a API do Google, então rodam sem internet.
