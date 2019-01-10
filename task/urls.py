from django.urls import include, path
from . import views
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:id>/', views.detail, name = 'detail'),
    path('addform/', views.addHabit, name = 'add_habit'),
    path('editform/<int:id>/', views.editHabit, name = 'edit_habit'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),

]
