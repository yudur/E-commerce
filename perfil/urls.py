from django.urls import path
from . import views


app_name = 'perfil'  # perfil:create

urlpatterns = [
    path('', views.Create.as_view(), name='create'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
