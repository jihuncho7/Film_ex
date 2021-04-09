from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView

from film.models import Film


class Film(ListView):
    model = Film
    #paginate_by = 100  # if pagination is desired
