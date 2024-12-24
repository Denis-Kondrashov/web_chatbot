from django.urls import path
from .views import home, ask_question

urlpatterns = [
    path('', home, name='home'),
    path('ask/', ask_question, name='ask_question'),
]
