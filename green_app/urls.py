from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Core views
    path('', views.IndexView.as_view(), name='index'),
    path('idea/<int:pk>/', views.IdeaDetailView.as_view(), name='idea_detail'),
    path('submit/', views.SubmitIdeaView.as_view(), name='submit_idea'),
    path('search/', views.search_view, name='search'),
    path('about/', views.about_us_view, name='about_us'),
    
    # Authentication views
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('unregister/', views.unregister_view, name='unregister'),
    path('history/', views.user_history_view, name='user_history'),
    
    # User Profile views
    path('profile/', views.user_profile_view, name='user_profile'),
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
    
    # Comment and Rating views
    path('idea/<int:idea_id>/comment/', views.add_comment_view, name='add_comment'),
    path('idea/<int:idea_id>/rate/', views.add_rating_view, name='add_rating'),
    
    # Project views
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    
    # Event views
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    
    # Resource views
    path('resources/', views.ResourceListView.as_view(), name='resource_list'),
    path('resources/<int:pk>/', views.ResourceDetailView.as_view(), name='resource_detail'),
    path('resources/create/', views.ResourceCreateView.as_view(), name='resource_create'),
    
    # Collaboration views
    path('projects/<int:project_id>/collaborate/', views.collaboration_request_view, name='collaboration_request'),
    path('collaboration/<int:collaboration_id>/<str:response>/', views.collaboration_response_view, name='collaboration_response'),
    
    # Newsletter views
    path('newsletters/', views.NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletters/<int:pk>/', views.NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('newsletters/create/', views.NewsletterCreateView.as_view(), name='newsletter_create'),
    
    # Idea management
    path('idea/<int:pk>/delete/', views.delete_idea_view, name='delete_idea'),
    
    # Password reset views
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='green_app/password_reset.html'
         ), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='green_app/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='green_app/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='green_app/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]