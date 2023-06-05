from .abstract_tags import  Types, Tag, AnyTagFactory
from .tags import *
from .tag_factories import RadioValueTypes

class TagSerializer:
    tag = Tag
    def __init__(self, obj:tag):
        assert issubclass(obj.__class__, self.tag), f'{obj} is not {self.tag} class'
        self.obj = obj
        self.data = self.get_info()

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.data})'

    def get_info(self):
        return {'type': self.obj.type}
    
    
    @classmethod
    def create(self, kwarg: dict):
        tag = AnyTagFactory.create(**kwarg)
        return self(tag)
    
class SerializerTypes(Types):
    types: dict[str, TagSerializer] = {}
    @classmethod
    def add_type(self, type: str, serializer: TagSerializer):
        self.types[type] = serializer

    @classmethod
    def add_cls(self, serializer: TagSerializer):
        self.add_type(serializer.tag.type, serializer)

    @classmethod
    def get_all_types(self):
        return self.types
    
    @classmethod
    def get_type(self, type):
        return self.types[type]
    
    @classmethod
    def get_type_with_cls(self, cls: Tag):
        return self.get_type(cls.type)

    @classmethod
    def add_clses(self, clses):
        for cls in clses: self.add_cls(cls)

    @classmethod
    def add_clses_with_cls(self, clses: list[list[Tag, TagSerializer]]):
        for cls in clses: self.add_type(cls[0].type, cls[1])
    
class AnyTagSerializer:

    @classmethod
    def create(self, kwarg: dict):
        type = kwarg['type']
        serializer = SerializerTypes.get_type(type)
        return serializer.create(kwarg)
    
    @classmethod
    def create_with_obj(self, obj: Tag) -> TagSerializer:
        serializer = SerializerTypes.get_type(obj.type)
        return serializer(obj)
    
class ManyTagSerializer:

    def __init__(self) -> None:
        self.obj_list = []
        self.data = []

    def add(self, obj:Tag):
        assert issubclass(obj.__class__, Tag), f'{obj} is not Tag class'
        self.obj_list.append(obj)
        serializer = AnyTagSerializer.create_with_obj(obj)
        self.data.append(serializer.data)

    def add_many(self, list: list[Tag]):
        for tag in list: self.add(tag)

    @classmethod
    def create(self, list: list[dict]):
        ins = ManyTagSerializer()
        for dict in list:
            obj = AnyTagFactory.create(dict)
            ins.add(obj)

class ParentTagSerializer(TagSerializer):
    tag = ParentTag

    def get_info(self):
        info = super().get_info()
        serializer = ManyTagSerializer()
        serializer.add_many(self.obj.childs)
        childs_info = serializer.data
        info['childs'] = childs_info
        return info

class ChildTagSerializer(TagSerializer):
    tag = ChildTag

class ParentAndChildTagSerializer(ParentTagSerializer):
    tag = ParentAndChildTag

class FieldsetSerializer(ParentAndChildTagSerializer):
    tag = FieldSet

    def get_info(self):
        info = super().get_info()
        info['legend'] = self.obj.legend
        return info

class ListTagSerializer(ParentAndChildTagSerializer):
    tag = ListTag

    def get_info(self):
        info = super().get_info()
        info['name'] = self.obj.name
        return info
    
class InputSerializer(ChildTagSerializer):
    tag = Input

    def get_info(self):
        info = super().get_info()
        info['name'] = self.obj.name
        info['value'] = self.obj.value
        info['label'] = self.obj.label
        return info
    
class InputWithListSerializer(InputSerializer):
    tag = InputWithList

    def get_info(self):
        info = super().get_info()
        info['list_name'] = None
        list = self.obj.list
        if list:
            info['list_name'] = list.name
        return info

class CheckboxSerializer(InputSerializer):
    tag = Checkbox

    def get_info(self):
        info =  super().get_info()
        info['is_checked'] = self.obj.is_checked
        return info

class RadioSerializer(InputSerializer):
    tag = Radio

    def get_info(self):
        info = super().get_info()
        info['radio_list'] = self.obj.radio_list
        info['value_type'] = RadioValueTypes.get_type(self.obj.value_type)
        return info

SerializerTypes.add_clses([
    FieldsetSerializer,
    ListTagSerializer,
    RadioSerializer,
    CheckboxSerializer
])
SerializerTypes.add_clses_with_cls([
    [Body, ParentTagSerializer],
    [Div, ParentAndChildTagSerializer],
    [StringInput, InputWithListSerializer],
    [FloatInput, InputWithListSerializer],
    [IntegerInput, InputWithListSerializer],
])
    