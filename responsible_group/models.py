from typing import Any, Iterable, Optional
from rest_framework.validators import ValidationError
from django.db import models
from staff.models import ResponsiblePerson as rp
from page.models import Page
# Create your models here.

# I used in this section from linked list. ResponsiblePerson is linkedlist node, ResponsibleGroup is linkedlist manager

RESPONSIBLE_TYPE = [
    ("fi", "filler"),
    ("co", "confirmative")
]

class ResponsiblePerson(models.Model):
    group = models.ForeignKey("ResponsibleGroup", on_delete=models.CASCADE, related_name="for_option")
    responsible = models.ForeignKey(rp, on_delete=models.PROTECT)
    type = models.CharField(max_length=25, choices=RESPONSIBLE_TYPE, default="co")
    next = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

class Filler(ResponsiblePerson):
    fields = models.JSONField(null=True, blank=True)
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.type = "fi"

    def save(self, force_insert: bool = ..., 
             force_update: bool = ..., using: str | None = ..., 
             update_fields: Iterable[str] | None = ...) -> None:
        fields = self.fields
        if type(fields) != list: return ValidationError("fields must be a list")
        available_fields = self.group.page.inputs.inputs
        for field in fields:
            if not field in available_fields: 
                ValidationError(f"{field} is not available {self.group.page.name} page")
        return super().save(force_insert, force_update, using, update_fields)

    

# this group resbonsible for some defined documents

class ResponsibleGroup(models.Model):
    page = models.OneToOneField(Page, on_delete=models.PROTECT)
    first = models.ForeignKey(ResponsiblePerson, on_delete=models.PROTECT, related_name='first_responsible_person', null=True, blank=True)
    last = models.ForeignKey(ResponsiblePerson, on_delete=models.PROTECT, related_name='last_responsible_person', null=True, blank=True)


