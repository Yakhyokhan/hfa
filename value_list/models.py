from django.db import models
from company.models import Company
# Create your models here.

class List(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def get_items(self):
        items = ListItem.objects.filter(list = self)
        return items

class ListItem(models.Model):
    name = models.CharField(max_length=50)
    list = models.ForeignKey(List, on_delete=models.CASCADE)