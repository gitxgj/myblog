from django.urls import path,re_path
from . import views


urlpatterns = (
    path("", views.demo1),
    path('user<str:username>/', views.demo),
    path('login/', views.LoginView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('changepassword/', views.ChangePassword.as_view()),


)
