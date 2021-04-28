from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from django.contrib import admin
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('it-essentials/<slug:slug>', chapter_content, name='chapter_content'),
    path('it-essentials/<int:id>/take-exam', take_exam, name='take_exam'),
    path('it-essentials/<int:id>/start-exam', start_exam, name='start-exam'),
    path('it/calculate-marks', calculate_marks,name='calculate-marks'),
    path('result/<int:id>', results,name='results'),
    path('view_result', view_result, name='view_result'),
    path('chapter/<int:id>/', chapter, name='chapter'),  

    path('news', news, name='news'),
    path('news/<int:id>', news_details, name='news_details'),

    path('signup', signup, name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # path('exam/<int:id>', exam, name='exam'),

    path('add-chapter', add_chapter, name='add_chapter'),
    path('add-exam', add_exam, name='add_exam'),
    path('add-question', add_question, name='add_question'),

    path('view-chapters', view_chapters, name='view_chapters'),
    path('view-exams', view_exams, name='view_exams'),
    path('view-questions', view_questions, name='view_questions'),

    path('edit-exam/<int:pk>', edit_exam, name='edit_exam'),
    path('edit-question/<int:pk>', edit_question, name='edit_question'),
    path('edit-chapter/<int:pk>', edit_chapter, name='edit_chapter'),

    path('students-results', students_results, name='students_results'),
    path('your-result/<int:id>', after_exam, name='after_exam'),

    path('take_test/<int:chapter_id>', take_test, name='take_test'),


]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
