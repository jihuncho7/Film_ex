import film.views
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from allauth.account.views import LoginView
urlpatterns = [
    path('admin/', admin.site.urls), # 관리자
    path('',include('film.urls')), #메인
    path('film/', include('film.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('accounts/', include('allauth.urls')),

    path('api/',include("api.urls")),
    # path('',LoginView.as_view(template_name="login/index.html"))
    #path('social/', include('social_django.urls')),
    #path('google/', include('google_app.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
