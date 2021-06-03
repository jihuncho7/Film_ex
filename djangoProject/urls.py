import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from allauth.account.views import LoginView



urlpatterns = [
    path('admin/', admin.site.urls), # 관리자
    path('film/', include('film.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api/',include("api.urls")),
    path('login/', include('login.urls')),
    path('account/', include('rest_auth.urls')),
    path('account/registration/', include('rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),
    # url(r'account/registration/confirm-email/(?P<key>.+)/$', confirm_email, name='confirm_email'),
    path('', include('django.contrib.auth.urls')),
    # path('',LoginView.as_view(template_name="login/index.html"))
    #path('social/', include('social_django.urls')),
    #path('google/', include('google_app.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
