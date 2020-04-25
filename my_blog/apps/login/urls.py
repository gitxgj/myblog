from django.urls import path
from . import views
urlpatterns = [
    path('qq/login/', views.QQAutoView.as_view()),
    
    
    
]