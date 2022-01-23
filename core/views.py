from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, IssueForm, ProjectForm
from django.contrib import messages
from django.contrib.auth import get_user_model 
from django.http import HttpResponse

from .models import Project, Issue
from django.contrib.auth.models import User 

# Create your views here.

def register(request):
    # check to see if POST or GET
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
        
            return redirect('register')
    
    else:
        f = CustomUserCreationForm()
    
    return render(request, 'core/register.html', {'form': f})

def createIssue(request):
    current_user = request.user.id
    project_id = request.session['project']
    if request.method == 'POST':
        f = IssueForm(current_user, project_id, request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Issue created successfully')
            return redirect('/%s/' % project_id)
    else: 
        f = IssueForm(current_user, project_id)
    
    return render(request, 'core/createissue.html', {'form': f})

def base(request):
    if request.user.is_authenticated:
        return render(request, 'core/base.html', {'projects': Project.objects.values()})
    else:
        return redirect('accounts/login')

def createProject(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            f = ProjectForm(request.POST)
            if f.is_valid():
                f.save()
                messages.success(request, 'Project created successfully')
                return redirect('base')
        else:
            f = ProjectForm() 
    return render(request, 'core/createproject.html', {'form': f})

def project(request, project_id):
    bugs = Issue.objects.filter(project_id=project_id)
    creators = []
    for bug in bugs:
        user = User.objects.get(pk=bug.creator_id)
        creator = user.first_name + " " + user.last_name
        creators.append((bug, creator))
    request.session['project'] = project_id
    return render(request, 'core/project.html', {'bugs': bugs, 'creators': creators})

def issue(request, issue_id):
    bug = Issue.objects.get(id=issue_id)
    return render(request, 'core/issue.html', {'bug': bug})