from django.urls import path
from . import views

urlpatterns = [


    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),  # Ensure the pattern matches this
    path('submit_review/<int:movie_id>/', views.submit_review, name='submit_review'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('edit_profile/', views.edit_user_profile, name='edit_user_profile'),
    path('user_profile/', views.user_profile, name='user_profile'),
]