from django.db import models
from responsible_group.models import ResponsibleGroup
from company.models import Company
from tags.serializer import AnyTagSerializer, ManyTagSerializer
from tags.field_finders import AnyFieldFinder
from typing import Any
# Create your models here.

class TagField(models.JSONField):
    db_writer = AnyTagSerializer
    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        json = super().from_db_value(value, expression, connection)
        if json == None: return None
        return self.db_writer.create(**json).obj
    def to_python(self, value: Any) -> Any:
        json = super().to_python(value)
        if json == None: return None
        return self.db_writer.create(**json).obj
    
    def get_prep_value(self, value: Any) -> Any:
        json = self.db_writer.create_with_obj(value).get_info()
        return super().get_prep_value(json)
    
    
    
class ManyTagField(models.JSONField):
    db_writer = ManyTagSerializer
    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        json = super().from_db_value(value, expression, connection)
        if json == None: return None
        return self.db_writer.create(json).obj_list
    def to_python(self, value: Any) -> Any:
        json = super().to_python(value)
        if json == None: return None
        return self.db_writer.create(json).obj_list
    
    def get_prep_value(self, value: Any) -> Any:
        db_obj = self.db_writer()
        db_obj.add_many(value)
        json = db_obj.get_info()
        return super().get_prep_value(json)

class Html(models.Model):
    name = models.CharField(max_length=50)
    tags = TagField()
    inputs = ManyTagField(null=True, blank=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.inputs == None:
            self.inputs = AnyFieldFinder.find(self.tags)

    def save(self, force_insert = False, force_update = False, using = None, update_fields = None):
        self.inputs = AnyFieldFinder.find(self.tags)
        if update_fields is not None and "inputs" in update_fields:
            update_fields = {"inputs"}.union(update_fields)
        super().save(force_insert, force_update, using, update_fields)
    


class Page(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    html = models.ForeignKey(Html, on_delete=models.PROTECT, null=True, blank=True)
    responsible_group = models.ForeignKey(ResponsibleGroup, on_delete=models.PROTECT)

