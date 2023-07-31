from django.db import models
from tags.serializer import AnyTagSerializer, ManyTagSerializer
from tags.field_finders import AnyFieldFinder
from tags.abstract_tags import Parent
from typing import Any
from django.dispatch import Signal
from django.db.models.signals import post_save

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


class HtmlInputs(models.Model):
    html = models.OneToOneField(Html, on_delete=models.CASCADE)
    inputs = models.JSONField(null=True, blank=True)
    required_fields = models.JSONField(null=True, blank=True)


def signal_html_input(sender, instance: Html, created, **kwarg):
    inputs = AnyFieldFinder.find(instance.tags)
    info = [x.get_input_info() for x in inputs if inputs]
    def info_to_json(info: list[dict]):
        res = {}
        required = []
        for item in info:
            name = item.pop("name")
            if "childs" in item:
                childs = item.pop("childs")
                childs, child_rq = info_to_json(childs)
                required += child_rq
                res.update(childs)
            else:
                if item["required"] == True:
                    required.append(name)
            res[name] = item
        print(res)
        return res, required
    inputs, required = info_to_json(info)

    if created:
        HtmlInputs.objects.create(html = instance, inputs = inputs, required_fields = required)
        return
    input_ins = HtmlInputs.objects.get(html = instance)
    input_ins.inputs = inputs
    input_ins.required_fields = required
    input_ins.save()
    
Signal.connect(post_save, signal_html_input, Html)