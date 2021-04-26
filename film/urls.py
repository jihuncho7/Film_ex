

from django.urls import path, include
from django.views.generic import TemplateView

from film import views

app_name = 'film'

urlpatterns = [
path('',TemplateView.as_view(template_name="film/index.html"), name='index'),
path('review/', views.review, name='review'),

]



