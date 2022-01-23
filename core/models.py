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
    name = models.CharField(max_length=60)


class Issue(models.Model):
    
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="creator")
    assignee = models.ManyToManyField(User, related_name="assignee")

    bug = models.CharField(max_length=500)
    pub_date = models.DateTimeField(default=timezone.now())
    due_date = models.DateTimeField('date due')
    resolved = models.BooleanField(default=False)        
    
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE)
    
    def resolve(self):
        self.resolved = True
    
    def __str__(self):
        return self.bug  

class Person(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)