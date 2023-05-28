from django.db import models
from company.models import Company
from user.models import User
# Create your models here.


class Works(models.Model):
    name = models.CharField(max_length=25)

class Workers(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    work = models.ManyToManyField(Works, through= 'ResponsiblePerson')

class ResponsiblePerson(models.Model):
    work = models.ForeignKey(Works, on_delete=models.PROTECT)
    worker = models.ForeignKey(Workers, on_delete=models.PROTECT)
    salary = models.BigIntegerField()