from django.db import models
from django.contrib.auth import get_user_model 
from django.utils import timezone

from django.contrib.auth.models import User 


# Create your models here.

# many to many relationship between issues and assignees (DONE)
# many to many relationship between projects and users 
# one to many relationship between issues and projects 

class Project(models.Model):
    workers = models.ManyToManyField(User)
    description = models.CharField(max_length=500)
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Issue(models.Model):
    
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="creator")
    assignee = models.ManyToManyField(User, related_name="assignee")

    bug = models.CharField(max_length=500)
    pub_date = models.DateTimeField(default=timezone.now())
    due_date = models.DateTimeField('date due')
    resolved = models.BooleanField(default=False)        
    
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.bug  

class Comment(models.Model):

    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poster')
    body = models.CharField(max_length=1000)
    posted = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.body


class Person(models.Model): 
    description = models.CharField(max_length=500)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class IssueHistory(models.Model):
    assignee = models.ManyToManyField(User, related_name="updatedassignee", blank=True, null=True)
    bug = models.CharField(max_length=500, blank=True, null=True)
    resolved = models.BooleanField(default=False)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='issue')
    date = models.DateTimeField(default=timezone.now())

