from django.db import models
from db_connections import db
# Create your models here.

users_collection = db['users']
test_collection = db['tests']

class users(models.Model):
    name = models.CharField(max_length=200)  
    isStudent = models.BooleanField(default=True)
    email = models.EmailField()  
    userId = models.CharField(max_length=20) 
    password = models.CharField(max_length=10) 

    def __str__(self):  
        return self.name