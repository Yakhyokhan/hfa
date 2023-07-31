from django.db import models
from company.models import Company
from interface.models import Html, HtmlInputs
from django.dispatch import Signal
from django.db.models.signals import post_save
# Create your models here.

class Page(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    html = models.ForeignKey(Html, on_delete=models.PROTECT, null=True, blank=True)
    inputs = models.ForeignKey(HtmlInputs, on_delete=models.PROTECT, null=True, blank=True)
    

    def save(self, force_insert = ..., force_update = ..., using = ..., update_fields = ...):
        self.inputs = HtmlInputs.objects.get(html = self.html)
        if update_fields is not None and "inputs" in update_fields:
            update_fields = {"inputs"}.union(update_fields)
        super().save(force_insert, force_update, using, update_fields)