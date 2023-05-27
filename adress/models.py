from django.db import models

# Create your models here.

class Adress(models.Model):
    country = models.CharField(max_length=25)
    region = models.CharField(max_length=25)
    town = models.CharField(max_length=25)
    line = models.TextField()