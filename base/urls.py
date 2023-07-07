from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('room/<str:pk>/',views.room, name='room'),
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('register/',views.registerPage, name='register'),
    path('create-room/',views.createRoom, name='create-room'),
    path('edit-room/<str:pk>/',views.editRoom, name='edit-room'),
    path('delete-room/<str:pk>/',views.deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>/',views.deleteMessage, name='delete-message'),
    path('profile/<str:pk>/',views.userProfile, name='profile'),
    path('edit-profile/<str:pk>/',views.editProfile, name='edit-profile'),
    path('activities/',views.activitiesPage, name='activities'),
    path('topics/',views.topicsPage, name='topics'),
]