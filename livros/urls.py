from django.urls import path

from . import views

urlpatterns = [
    # Livro: listar (estante), criar, detalhar, editar
    path('', views.LivroListView.as_view(), name='livro_list'),
    path('livro/novo/', views.LivroCreateView.as_view(), name='livro_create'),
    path('livro/<int:pk>/', views.LivroDetailView.as_view(), name='livro_detail'),
    path('livro/<int:pk>/editar/', views.LivroUpdateView.as_view(), name='livro_update'),

    # Leitura e Resenha
    path('livro/<int:livro_pk>/leitura/nova/', views.LeituraCreateView.as_view(), name='leitura_create'),
    path('leitura/<int:pk>/editar/', views.LeituraUpdateView.as_view(), name='leitura_update'),
    path('leitura/<int:leitura_pk>/resenha/nova/', views.ResenhaCreateView.as_view(), name='resenha_create'),
    path('resenha/<int:pk>/editar/', views.ResenhaUpdateView.as_view(), name='resenha_update'),

    # Busca no Google Books
    path('buscar/', views.buscar, name='buscar'),
    path('buscar/adicionar/<str:google_id>/', views.adicionar, name='adicionar'),
]
