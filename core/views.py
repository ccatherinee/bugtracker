from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, IssueForm, ProjectForm, UpdateIssueForm, CommentForm, UpdateWorkersForm
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.http import HttpResponse

from .models import Project, Issue, Comment, IssueHistory
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

def logout_view(request):
    logout(request)
    return redirect('/accounts/login')

def createIssue(request):
    if request.user.is_authenticated:
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
    else: 
        return redirect('/accounts/login')
def base(request):
    if request.user.is_authenticated:
        return render(request, 'core/base.html')
    else:
        return redirect('/accounts/login')

def projects(request):
    if request.user.is_authenticated:
        return render(request, 'core/projects.html', {'projects': Project.objects.values()})

def manage_users(request, project_id):
    if request.user.is_authenticated:
        return render(request, 'core/manage_users.html', {'project': Project.objects.get(pk=project_id)})

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
    else:
        return redirect('/accounts/login')
    return render(request, 'core/createproject.html', {'form': f})

def project(request, project_id):
    request.session['project'] = project_id
    bugs = Issue.objects.filter(project_id=project_id)

    if request.GET.get('created by me') == 'created by me':
        bugs = Issue.objects.filter(project_id=project_id).filter(creator_id=request.user.id)

    if request.GET.get('unresolved') == 'unresolved':
        bugs = Issue.objects.filter(project_id=project_id).filter(resolved=False)
    
    if request.GET.get('resolved') == 'resolved':
        bugs = Issue.objects.filter(project_id=project_id).filter(resolved=True)

    if request.method == 'POST':
        f = UpdateWorkersForm(project_id, request.POST)
        if f.is_valid():
            f.save()
            return redirect('/%s/' % project_id)
    else:
        f = UpdateWorkersForm(project_id) 

    information = []
    for bug in bugs:
        user = User.objects.get(pk=bug.creator_id)
        creator = user.first_name + " " + user.last_name
        assignees = ""
        for assignee in bug.assignee.all():
            user = User.objects.get(pk=assignee.id)
            assignees = user.first_name + " " + user.last_name + ", " + assignees
        resolved = bug.resolved
        created = bug.pub_date
        due = bug.due_date
        information.append((bug, assignees[:-2], creator, resolved, created, due))

    project = Project.objects.get(pk=project_id)

    workers = []
    for worker in project.workers.all():
        user = User.objects.get(pk=worker.id)
        workers.append(user.first_name + " " + user.last_name)


    return render(request, 'core/project.html', {'bugs': bugs, 'information': information, 'workers': workers, 'project': project, 'form': f})

def issue(request, issue_id):
    project_id = request.session['project']
    current_user = request.user.id
    bug = Issue.objects.get(id=issue_id)

    history_information = []
    histories = IssueHistory.objects.filter(issue_id=issue_id)
    for history in histories:
        issue = history.bug
        resolved = history.resolved
        assignees = ""
        for assignee in history.assignee.all():
            user = User.objects.get(pk=assignee.id)
            assignees = user.first_name + " " + user.last_name + ", " + assignees
        date = history.date
        history_information.append((issue, resolved, assignees[:-2], date))

    comments = Comment.objects.filter(issue_id=issue_id)

    posters = []
    for comment in comments:
        user = User.objects.get(pk=comment.poster_id)
        poster = user.first_name + " " + user.last_name
        posters.append((comment, poster))

    if request.method == 'POST':
        if "Update" in request.POST:
            f = UpdateIssueForm(issue_id, request.POST)
            if f.is_valid():
                f.save()
                messages.success(request, 'Issue updated successfully')
                return redirect('/%s/details' % issue_id)
        else:
            f = UpdateIssueForm(issue_id)
        if "Comment" in request.POST:
            g = CommentForm(current_user, issue_id, request.POST)
            if g.is_valid():
                g.save()
                return redirect('/%s/details/' % issue_id)
        else:
            g = CommentForm(current_user, issue_id)
    else: 
        f = UpdateIssueForm(issue_id)
        g = CommentForm(current_user, issue_id)

    information = []
    user = User.objects.get(pk=bug.creator_id)
    creator = user.first_name + " " + user.last_name
    assignees = ""
    for assignee in bug.assignee.all():
        user = User.objects.get(pk=assignee.id)
        assignees = user.first_name + " " + user.last_name + ", " + assignees
    resolved = bug.resolved
    created = bug.pub_date
    due = bug.due_date
    information.append((bug, assignees[:-2], creator, resolved, created, due))

    return render(request, 'core/issue.html', {'form': f, 'form2': g, 'comments': comments, 'posters': posters, 'information': information, 'history_information': history_information})


def myissues(request):
    curr_user = request.user.id

    bugs = Issue.objects.filter(creator_id=curr_user)

    if request.GET.get('created by me') == 'created by me':
        bugs = Issue.objects.filter(creator_id=curr_user)

    if request.GET.get('unresolved') == 'unresolved':
        bugs = Issue.objects.filter(creator_id=curr_user).filter(resolved=False)
    
    if request.GET.get('resolved') == 'resolved':
        bugs = Issue.objects.filter(creator_id=curr_user).filter(resolved=True)

    information = []
    for bug in bugs:
        user = User.objects.get(pk=bug.creator_id)
        creator = user.first_name + " " + user.last_name
        assignees = ""
        for assignee in bug.assignee.all():
            user = User.objects.get(pk=assignee.id)
            assignees = user.first_name + " " + user.last_name + ", " + assignees
        resolved = bug.resolved
        created = bug.pub_date
        due = bug.due_date
        project = Project.objects.get(pk=bug.project_id)
        information.append((bug, project, assignees[:-2], creator, resolved, created, due))

    return render(request, 'core/myissues.html', {'information': information})

