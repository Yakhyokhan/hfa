from django.db import models
from responsible_group.models import ResponsibleGroup
from company.models import Company
# Create your models here.

class Page(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    html = models.JSONField()
    responsible_group = models.ForeignKey(ResponsibleGroup, on_delete=models.PROTECT)
    inputs = models.JSONField()
    list = models.ManyToManyField('List')


class List(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class ListItem(models.Model):
    name = models.CharField(max_length=50)
    list = models.ForeignKey(List, on_delete=models.CASCADE)




