from django.urls import path 

from . import views 

urlpatterns = [
    path('register/', views.register, name='register'), 
    path('createissue/', views.createIssue, name='createIssue'),
    path('', views.base, name='base'),
    path('createproject/', views.createProject, name='createProject'),
    path('<int:project_id>/', views.project, name='project'),
    path('<int:issue_id>/details/', views.issue, name='issue')
]