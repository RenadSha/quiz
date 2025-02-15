from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name = "home"),
    path('register/', views.register, name = "register"),
    path('login/', views.userLogin, name = "login"),
    path('logout/', views.userLogout, name = "logout"),

    path('invite/accept/<int:invite_id>/', views.accept_invite, name='accept_invite'),
    path('quiz/<int:quiz_id>/', views.quiz_page, name='quiz_page'),


    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('quiz/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
    path('quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),


]
