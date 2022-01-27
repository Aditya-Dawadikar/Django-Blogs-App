from django.db import models
from itertools import chain

# Create your models here.
class User(models.Model):
    
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20,unique=True)
    isAdmin = models.BooleanField(null=False)
    
class Blog(models.Model):
    
    blogid = models.AutoField(primary_key=True)
    blog_title = models.CharField(max_length = 50)
    blog_content = models.TextField()
    blog_date = models.DateField()
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
