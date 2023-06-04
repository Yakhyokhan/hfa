from .abstract_tags import  Types,TagFactory, ParentTagFactory, Tag, ChildTagFactory, ParentAndChildTagFactory
from .tag_factories import *
from .tags import FieldHabitude

class TagSerializer:
    factory = TagFactory
    tag = factory.res_class
    def __init__(self, obj:tag):
        assert type(obj) == self.tag, f'{obj} is not {self.tag} class'
        self.obj = obj
        self.data = self.__get_info()

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.data})'

    def __get_info(self):
        return {'type': self.obj.type}
    
    
    @classmethod
    def create(self, kwarg: dict):
        tag = self.factory.create(**kwarg)
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
    def add_types(self, types: list[str]):
            for type in types: self.add_type(type)

    @classmethod
    def add_clses(self, clses):
        for cls in clses: self.add_cls(cls)
    
class AnyTagSerializer:

    @classmethod
    def create(self, kwarg: dict):
        type = kwarg['type']
        serializer = SerializerTypes.get_type(type)
        return serializer.create(kwarg)
    
    def create_with_obj(self, obj: Tag) -> TagSerializer:
        serializer = SerializerTypes.get_type(obj)
        return serializer(obj)
    
class ManyTagSerializer:

    def __init__(self) -> None:
        self.obj_list = []
        self.data = self.__get_info()

    def __get_info(self):
        list = []
        for obj in self.obj_list:
            serializer = AnyTagSerializer.create_with_obj(obj)
            list.append(serializer.data)
        return list

    def add(self, obj:Tag):
        assert isinstance(obj.__class__, Tag), f'{obj} is not Tag class'
        self.obj_list.append(obj)

    def add_many(self, list: list[Tag]):
        for tag in list: self.obj_list.append(tag)

    @classmethod
    def create(self, list: list[dict]):
        ins = ManyTagSerializer()
        for dict in list:
            obj = AnyTagFactory.create(dict)
            ins.add(obj)

class ParentTagSerializer(TagSerializer):
    factory = ParentTagFactory

    def __get_info(self):
        info = super().__get_info()
        serializer = ManyTagSerializer()
        serializer.add_many(self.obj.childs)
        childs_info = serializer.data
        info['childs'] = childs_info
        return info

    
class ChildTagSerializer(TagSerializer):
    factory = ChildTagFactory

class ParentAndChildTagSerializer(ParentTagSerializer):
    factory = ParentAndChildTagFactory

class BodySerializer(ParentTagSerializer):
    factory = BodyFactory

class DivSerializer(ParentAndChildTagSerializer):
    factory = DivFactory

class FieldsetSerializer(ParentAndChildTagSerializer):
    factory = FieldSetFactory

    def __get_info(self):
        info = super().__get_info()
        info['legend'] = self.obj.legend
        return info

class ListTagSerializer(ParentAndChildTagSerializer):
    factory = ListTagFactory

    def __get_info(self):
        info = super().__get_info()
        info['name'] = self.obj.name
        return info
    
class InputSerializer(ChildTagSerializer):
    factory = InputFactory

    def __get_info(self):
        info = super().__get_info()
        info['name'] = self.obj.name
        info['value'] = self.obj.value
        return info
    
class InputWithListSerializer(InputSerializer):
    factory = InputWithListFactory

    def __get_info(self):
        info = super().__get_info()
        info['list_name'] = self.obj.list.name
        return info

class StringInputSerializer(InputWithListSerializer):
    factory = StringInputFactory

class IntegerInputSerializer(InputWithListSerializer):
    factory = IntegerInputFactory

class FloatInputSerializer(InputWithListSerializer):
    factory = FloatInputFactory

class CheckboxSerializer(InputSerializer):
    factory = CheckboxFactory

class RadioSerializer(InputSerializer):
    factory = RadioFactory

    def get_info(self):
        info = super().get_info()
        info['radio_list'] = self.obj.radio_list
        info['value_type'] = RadioValueTypes.get_type(self.obj.value_type)
        return info

SerializerTypes.add_clses([
    BodySerializer,
    DivSerializer,
    FieldsetSerializer,
    ListTagSerializer,
    StringInputSerializer,
    IntegerInputSerializer,
    FloatInputSerializer,
    CheckboxSerializer,
    RadioSerializer
])
    