from tags.abstract_tags import TagType
from .abstract_tags import TagFactoriesType, ParentTagFactory, ChildTagFactory, ParentAndChildTagFactory
from .tags import *

class InputFactory(ChildTagFactory):
    res_class = Input

    @classmethod
    def create(self, type, value = None, **kwargs):
        tag = TagType.get_type(type)
        value_type = tag.value_type
        default_value = default_values[value_type]
        if not value:
            value = default_value
        return tag(value= value, **kwargs)
        

class InputWithListFactory(InputFactory):
    res_class = InputWithList

    @classmethod
    def create(self,type=..., list = None, **kwargs):
        return super().create(type, list, **kwargs)

class RadioValueTypes:

    type_cls = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool
    }

    cls_type = {
        str: "str",
        int: "int",
        float: "float",
        bool: "bool" 
    }

    @classmethod
    def add(self, type, cls):
        self.type_cls[type] = cls
        self.cls_type[cls] = type

    @classmethod
    def get_cls(self, type):
        return self.type_cls[type]
    
    @classmethod
    def get_type(self, cls):
        return self.cls_type[cls]

class RadioFactory(InputFactory):
    res_class = Radio

    @classmethod
    def create(self, with_cls = False ,value_type = 'str', value = None ,**kwarg):
        if not with_cls:
            value_type = RadioValueTypes.get_cls(value_type)
        if not value:
            value = default_values[value_type]

        kwarg['value_type'] = value_type
        kwarg['value'] = value
        return super().create(**kwarg)
    
TagFactoriesType.add_cls(RadioFactory)
TagFactoriesType.add_clses_with_cls([
    [Body, ParentTagFactory],
    [Div, ParentAndChildTagFactory],
    [FieldSet, ParentAndChildTagFactory],
    [ListTag, ParentAndChildTagFactory],
    [StringInput, InputFactory],
    [IntegerInput, InputFactory],
    [FloatInput, InputFactory],
    [Checkbox, InputFactory],

])
