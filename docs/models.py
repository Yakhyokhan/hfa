from django.db import models
from page.models import Page
from responsible_group.models import ResponsiblePerson

# Create your models here.

class Docs(models.Model):
    page = models.ForeignKey(Page, on_delete=models.PROTECT)
    curr_responsible = models.ForeignKey(ResponsiblePerson, on_delete=models.PROTECT)
    values = models.JSONField()
