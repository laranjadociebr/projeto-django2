# projeto-django2

Estante de livros local feita com Django (MTV).

## Como rodar

```powershell
git clone https://github.com/laranjadociebr/projeto-django2.git
cd projeto-django2
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env   # preencha GOOGLE_BOOKS_API_KEY
python manage.py migrate
python manage.py createsuperuser   # para acessar o /admin
python manage.py runserver
```

Acesse http://127.0.0.1:8000/ (admin em /admin/).
