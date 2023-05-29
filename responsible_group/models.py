from django.db import models
from staff.models import ResponsiblePerson as rp
# Create your models here.

# I used in this section from linked list. ResponsiblePerson is linkedlist node, ResponsibleGroup is linkedlist manager

class ResponsiblePerson(models.Model):
    responsible = models.ForeignKey(rp, on_delete=models.PROTECT)
    type = models.CharField(max_length=25)
    next = models.ForeignKey('self', on_delete=models.PROTECT)

# class Filler(ResponsiblePerson):
    type = 'filler'
    

# this group resbonsible for some defined documents

class ResponsibleGroup(models.Model):
    first = models.ForeignKey(ResponsiblePerson, on_delete=models.PROTECT, related_name='first_responsible_person')
    last = models.ForeignKey(ResponsiblePerson, on_delete=models.PROTECT, related_name='last_responsible_person')