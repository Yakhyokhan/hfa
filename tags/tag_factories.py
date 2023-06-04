from .abstract_tags import TagFactoriesType, AnyTagFactory, Types,\
    ParentTagFactory, ChildTagFactory, ParentAndChildTagFactory
from .tags import radio_default_value, Body, Div, FieldSet, ListTag, Input, InputWithList, StringInput, IntegerInput, FloatInput, Checkbox, Radio
class BodyFactory(ParentTagFactory):
    res_class = Body

class DivFactory(ParentAndChildTagFactory):
    res_class = Div

class FieldSetFactory(ParentAndChildTagFactory):
    res_class = FieldSet

class ListTagFactory(ParentAndChildTagFactory):
    res_class = ListTag

class InputFactory(ChildTagFactory):
    res_class = Input
    
class InputWithListFactory(InputFactory):
    res_class = InputWithList

class StringInputFactory(InputWithListFactory):
    res_class = StringInput

class IntegerInputFactory(InputWithListFactory):
    res_class = IntegerInput

class FloatInputFactory(InputWithListFactory):
    res_class = FloatInput

class CheckboxFactory(InputFactory):
    res_class = Checkbox

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
            value = radio_default_value[value_type]

        kwarg['value_type'] = value_type
        kwarg['value'] = value
        return super().create(**kwarg)
    

TagFactoriesType.add_clses([
    BodyFactory,
    DivFactory,
    FieldSetFactory,
    ListTagFactory,
    InputFactory,
    StringInputFactory,
    IntegerInputFactory,
    FloatInputFactory,
    CheckboxFactory,
    RadioFactory
    ])
