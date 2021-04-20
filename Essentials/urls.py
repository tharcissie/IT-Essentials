from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from django.contrib import admin
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', homepage, name='homepage'),
    path('it-essentials/<int:id>/take-exam', take_exam, name='take_exam'),
    path('it-essentials/<int:id>/start-exam', start_exam, name='start-exam'),
    path('it/calculate-marks', calculate_marks,name='calculate-marks'),
    path('it/result/<int:id>', results,name='results'),
    path('view_result', view_result, name='view_result'),
    path('chapter/<int:id>', chapter, name='chapter'),  

    path('signup', signup, name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # path('exam/<int:id>', exam, name='exam'),





    
    
    
    
    
    
    
    
    
    path('take_test/<int:chapter_id>', take_test, name='take_test'),


























]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
