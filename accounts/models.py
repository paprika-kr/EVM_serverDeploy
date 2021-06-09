from django.db import models

# Create your models here.
#model for login
class monitor(models.Model):
    email = models.CharField(primary_key=True, max_length=30)
    fullname = models.CharField(max_length=30)
    password = models.CharField(max_length=30)