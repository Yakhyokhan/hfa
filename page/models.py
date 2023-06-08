from typing import Any, Iterable, Optional
from django.db import models
from responsible_group.models import ResponsibleGroup
from company.models import Company
from tags.serializer import AnyTagSerializer, ManyTagSerializer
from tags.field_finders import AnyFieldFinder
from value_list.models import List
# Create your models here.

class Page(models.Model):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.html:
            html = AnyTagSerializer.create(**self.html)
            self.html = html.obj
        inputs = self.inputs
        if inputs != None: 
            self.inputs = ManyTagSerializer.create(inputs).obj_list
            return
        self.inputs = AnyFieldFinder.find(self.html)

    def save(self, *args, **kwargs) -> None:
        html = self.html
        self.html = AnyTagSerializer.create_with_obj(html).get_info()
        inputs = AnyFieldFinder.find(html)
        input_info = ManyTagSerializer()
        input_info.add_many(inputs)
        self.inputs = input_info.get_info()
        super().save(*args, **kwargs)
        self.html = html
        self.inputs = inputs

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    html = models.JSONField()
    responsible_group = models.ForeignKey(ResponsibleGroup, on_delete=models.PROTECT)
    inputs = models.JSONField(null=True, blank=True)
    list = models.ManyToManyField(List, blank=True)







