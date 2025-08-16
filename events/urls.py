from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view, name='home' ),
    path('events/',views.event_list, name ='event_list'),
    path('dashboard/', views.organizer_dashboard, name='organizer_dashboard'),
    path('categories/',views.category_list, name ='category_list'),


    path('signin/',views.signin_view, name='signin' ),

    path('signup/',views.signup_view, name='signup'),

    path('categories/<int:pk>/delete/',views.category_delete, name='category_delete'),
    path('events/create/', views.event_create, name='event_create'),

    path('events/<int:pk>/leave/',views.leave_event, name='leave_event'),
    path('events/<int:pk>/edit/',views.event_edit, name='event_edit'),
    path('events/<int:pk>/' ,views.event_details, name ='event_details'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('categories/<int:pk>/edit/',views.category_edit, name='category_edit'),
    path('events/<int:pk>/join/' ,views.join_event, name ='join_event'),
    path('events/<int:event_id>/remove/<int:participant_id>/',views.remove_participant, name='remove_participant'),


    path('profile/',views.profile_view, name='profile' ),
    path('signout/',views.signout_view, name='signout' ),
]
