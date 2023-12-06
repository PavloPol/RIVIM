from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/new/', views.article_new, name='article_new'),
    path('article/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('article/<int:pk>/delete/', views.article_delete, name='article_delete'),
    path('article_list/', views.article_list, name='article_list'),
    path('login/', LoginView.as_view(template_name='registration/login.html', success_url='article_list'), name='login'),
]
