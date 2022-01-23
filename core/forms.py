from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model 

from .models import Issue, Project

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    first_name = forms.CharField(label='Enter First Name', min_length=1, max_length=150)
    last_name = forms.CharField(label='Enter Last Name', min_length=1, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email 
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'], 
            first_name=self.cleaned_data['first_name'], 
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'], 
            password=self.cleaned_data['password1']
        )
        return user

class IssueForm(forms.Form):

    User =  get_user_model()
    users = User.objects.values()
    # ids = User.objects.values_list('id', flat=True)
    usernames = [(user['id'], user['first_name'] + " " + user['last_name']) for user in users]

    
    assignee = forms.ChoiceField(choices=usernames)
    
    bug = forms.CharField(max_length=500)
    due_date = forms.DateTimeField(label='date due')

    def __init__(self, curr_user, project_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        User =  get_user_model()
        users = User.objects.values()
        usernames = [(user['id'], user['first_name'] + " " + user['last_name']) for user in users]

        self.fields['assignee'] = forms.ChoiceField(choices=usernames)
        # self.fields['creator'].queryset = curr_user
        self.curr_user = curr_user
        self.project_id = project_id

    def save(self, commit=True):
        issue = Issue.objects.create(
            creator_id=self.curr_user,
            project_id=self.project_id,
            bug=self.cleaned_data['bug'], 
            due_date=self.cleaned_data['due_date'], 
        )
        issue.assignee.add(self.cleaned_data['assignee']) 
        return issue

class ProjectForm(forms.Form):

    name = forms.CharField(max_length=60)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        User = get_user_model()
        users = User.objects.values()
        usernames = [(user['id'], user['first_name'] + " " + user['last_name']) for user in users]

        self.fields['workers'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=usernames)

    def save(self, commit=True):
        project = Project.objects.create(
            name=self.cleaned_data['name']
        )
        [project.workers.add(worker) for worker in self.cleaned_data['workers']]
        return project

