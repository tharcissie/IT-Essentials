from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from django.contrib import admin
from it_essentials.views import *




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('results', view_result, name='view_result'),
    path('chapter/<int:id>/', chapter, name='chapter'),  
    path('it-essentials/<int:id>/take-test', take_test, name='take_exam'),
    path('it-essentials/<int:id>/start-test', start_test, name='start-exam'),
    path('it/calculate-marks', calculate_marks,name='calculate-marks'),
    path('my-result/<int:id>', after_exam, name='after_exam'),
    path('test-results/<int:id>', results,name='test_results'),
    path('done-test', done_test,name='done_test'),
    path('profile', profile,name='profile'),
    path('user-change-password',auth_views.PasswordChangeView.as_view(template_name='core/change_password.html',success_url = '/'), name='user_change_password'),

    path('news', news, name='news'),
    path('news/<int:id>', news_details, name='news_details'),

    path('add-chapter', add_chapter, name='add_chapter'),
    path('add-test', add_exam, name='add_exam'),
    path('add-question', add_question, name='add_question'),
    path('view-chapters', view_chapters, name='view_chapters'),
    path('view-tests', view_exams, name='view_exams'),
    path('view-questions', view_questions, name='view_questions'),
    path('modify-test/<int:pk>', edit_exam, name='edit_exam'),
    path('modify-question/<int:pk>', edit_question, name='edit_question'),
    path('modify-chapter/<int:pk>', edit_chapter, name='edit_chapter'),
    path('students-results', students_results, name='students_results'),
    path('registered-students', registered_students, name='registered_students'),
    path('account', account, name='account'),
    path('change-password',auth_views.PasswordChangeView.as_view(template_name='admin/change_password.html',success_url = 'account'), name='change_password'),

]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
