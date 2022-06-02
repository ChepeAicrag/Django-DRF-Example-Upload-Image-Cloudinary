from django.urls import path
from . import views

urlpatterns = [
    path('', views.CrearListarUser.as_view()),
    path('<int:id>/', views.ActualizarListarEliminarUserById.as_view()),
]