from django.urls import path 

from . import views 

urlpatterns = [
    path('register/', views.register, name='register'), 
    path('createissue/', views.createIssue, name='createIssue'),
    path('', views.base, name='base'),
    path('createproject/', views.createProject, name='createProject'),
    path('<int:project_id>/', views.project, name='project'),
    path('<int:issue_id>/details/', views.issue, name='issue'),
    path('projects/', views.projects, name='projects'),
    path('<int:project_id>/manage_users/', views.manage_users, name='manage_users'),
    path('myissues/', views.myissues, name='myissues'),
    path('/accounts/logout/', views.logout_view, name='logout')
]