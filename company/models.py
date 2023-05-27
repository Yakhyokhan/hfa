from django.db import models
from adress.models import Adress
# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=25)
    inn = models.IntegerField()
    adress = models.ForeignKey(Adress, on_delete=models.PROTECT)
    


