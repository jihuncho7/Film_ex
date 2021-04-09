

from django.urls import path, include

from film.views import Film

urlpatterns = [
 path('',Film.as_view()),
]
