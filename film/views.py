from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView

from film.models import Film



def review(request):
    film_newest = Film.objects.all().order_by('-created_at')
    film_list = Film.objects.all().order_by('like_user_set')

    return render(request, 'film/film_list.html', {
        "film_list": film_list,
        "flim_newset" : film_newest,
    })