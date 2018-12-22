from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name = "Habits"),
    path('<int:id>/', views.detail, name = 'detail'),
]
