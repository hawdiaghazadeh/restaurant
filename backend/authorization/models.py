from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import random
# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True, db_index=True)
    password = models.CharField(max_length=128)
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.username
    
    def set_password(self, password):
        self.password = make_password(password)
        self.save()

    def check_password(self, password):
        return check_password(password, self.password)
