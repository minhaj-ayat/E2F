from django.contrib.auth import views as auth_views
try:
    from django.urls import include, url
except ImportError:
    from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from . import views as local_views


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    # url(r'^accounts/login/$', auth_views.LoginView, {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/login/$', local_views.loginView, name='loginView'),
    url(r'^accounts/logout/$', auth_views.LogoutView, {'next_page': '/'}, name='logout'),
    url(r'^', include('oidc_provider.urls', namespace='oidc_provider')),
    url(r'^admin/', admin.site.urls),
]
