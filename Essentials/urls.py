from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from django.contrib import admin
from core.views import homepage
from core.views import signup
from core.views import account

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),

    path('signup', signup, name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account', account, name='account'),

]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
