from django.db import models
from django.contrib.auth import get_user_model 

# Create your models here.
User =  get_user_model()
users = User.objects.values()
usernames = [(user['username'], user['first_name'] + " " + user['last_name']) for user in users]

class Issue(models.Model):
    creator = models.CharField(max_length=60)
    assignee = models.CharField(max_length=150, choices=usernames)
    bug = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published')
    due_date = models.DateTimeField('date due')
    resolved = models.BooleanField()
    
    def resolve(self):
        self.resolved = True
    
    def __str__(self):
        return self.bug 

