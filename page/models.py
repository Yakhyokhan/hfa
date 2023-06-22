from django.db import models
from responsible_group.models import ResponsibleGroup
from company.models import Company
from interface.models import Html
# Create your models here.

class Page(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    html = models.ForeignKey(Html, on_delete=models.PROTECT, null=True, blank=True)
    responsible_group = models.ForeignKey(ResponsibleGroup, on_delete=models.PROTECT)

