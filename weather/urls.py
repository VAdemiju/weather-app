from django.urls import path
from weather import views

app_name = 'weather'
urlpatterns = [
    path('', views.home, name="home"),
    path('delete/<name_slug>/<int:id>/', views.delete, name="delete"),
]