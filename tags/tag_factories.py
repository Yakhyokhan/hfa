from .abstract_tags import TagFactoriesType, AnyTagFactory, Types,\
    ParentTagFactory, ChildTagFactory, ParentAndChildTagFactory
from .tags import Body, Div, FieldSet, ListTag, Input, StringInput, IntegerInput, FloatInput, Checkbox, radio_default_value, Radio
class BodyFactory(ParentTagFactory):
    res_class = Body

class DivFactory(ParentAndChildTagFactory):
    res_class = Div

class FieldSetFactory(ParentAndChildTagFactory):
    res_class = FieldSet

    @classmethod
    def get_info(self, tag:res_class):
        info = super().get_info(tag)
        info['legend'] = tag.legend
        return info

class ListTagFactory(ParentAndChildTagFactory):
    res_class = ListTag

    @classmethod
    def get_info(self, tag: res_class):
        info = super().get_info(tag)
        info['name'] = tag.name
        return info

class InputFactory(ChildTagFactory):
    res_class = Input

    @classmethod
    def get_info(self, tag: res_class):
        info = super().get_info(tag)
        info['name'] = tag.name
        info['value'] = tag.value
        return info

class StringInputFactory(InputFactory):
    res_class = StringInput

class IntegerInputFactory(InputFactory):
    res_class = IntegerInput

class FloatInputFactory(InputFactory):
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

    @classmethod
    def get_info(self, tag: res_class):
        info = super().get_info(tag)
        info['radio_list'] = tag.radio_list
        info['value_type'] = RadioValueTypes.get_type(tag.value_type)
        return info
    

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
