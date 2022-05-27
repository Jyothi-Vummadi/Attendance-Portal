from django.urls import path
from . import views
from me22 import views
from django.conf import settings
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.homepage, name= 'homepage'),
    path('faculty/', views.faculty, name='faculty'),
    path('student/', views.student, name="student"),
    path('register_faculty/', views.register_fac, name='register_fac'),
    path('login/', views.login, name='login'),
    path('recog/', views.recognition, name="recog"),
    path('date_selection/', views.display_date.as_view(), name='date'),
    path('name_selection/', views.display_name.as_view(), name='name'),
    path('choose/', views.choice, name='choice'),
    path('register_student/', views.register_stu, name='register_stu'),
    path('student_attendance/', views.sav, name='sav'),
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout')
]