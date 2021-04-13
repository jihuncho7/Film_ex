from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView

from film.models import Film


@login_required
def review(request):
    film_newest = Film.objects.all().order_by('-created_at')
    film_list = Film.objects.all().order_by('like_user_set')


    return render(request, "instagram/index.html", {
        "film_list": film_list,
    })