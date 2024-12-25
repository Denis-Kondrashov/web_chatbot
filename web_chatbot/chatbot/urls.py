from django.urls import path
from .views import home, answer

urlpatterns = [
    path('', home, name='home'),
    path('answer/', answer, name='answer'),
]
