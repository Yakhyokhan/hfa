from .abstract_tags import  Types, Tag, AnyTagFactory
from .tags import *
from .tag_factories import RadioValueTypes

class TagSerializer:
    tag = Tag
    def __init__(self, obj:tag):
        assert issubclass(obj.__class__, self.tag), f'{obj} is not {self.tag} class'
        self.obj = obj

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.get_info()})'
    
    def __repr__(self) -> str:
        return self.__str__()

    def get_info(self) -> dict:
        return {'type': self.obj.type}
    
    
    @classmethod
    def create(self, **kwarg: dict):
        tag = AnyTagFactory.create(**kwarg)
        return self(tag)
    
class SerializerTypes:
    def __init__(self) -> None:
        self.types: dict[str, TagSerializer] = {}

    def add_type(self, type: str, serializer: TagSerializer):
        self.types[type] = serializer

    def add_cls(self, serializer: TagSerializer):
        self.add_type(serializer.tag.type, serializer)

    def get_all_types(self):
        return self.types
    
    def get_type(self, type):
        return self.types[type]
    
    def get_type_with_cls(self, cls: Tag):
        return self.get_type(cls.type)

    def add_clses(self, clses):
        for cls in clses: self.add_cls(cls)

    def add_clses_with_cls(self, clses: list[list[Tag, TagSerializer]]):
        for cls in clses: self.add_type(cls[0].type, cls[1])

    def update_type(self, type, cls):
        self.types[type] = cls

    def update_cls(self, cls):
        self.types[cls.tag.type] = cls

serializer_types = SerializerTypes()
serializer_types_for_showing = SerializerTypes()
    
class AnyTagSerializer:
    serializer_types = serializer_types
    @classmethod
    def create(self, **kwarg: dict):
        if not kwarg:
            return
        type = kwarg['type']
        serializer = self.serializer_types.get_type(type)
        return serializer.create(**kwarg)
    
    @classmethod
    def create_with_obj(self, obj: Tag) -> TagSerializer:
        serializer = self.serializer_types.get_type(obj.type)
        return serializer(obj)
    
class AnyTagSerializerForShowing(AnyTagSerializer):
    serializer_types = serializer_types_for_showing
    
class ManyTagSerializer:
    any_tag_serializer = AnyTagSerializer

    def __init__(self) -> None:
        self.obj_list = []
        self.serializers = []

    def add(self, obj:Tag):
        assert issubclass(obj.__class__, Tag), f'{obj} is not Tag class'
        self.obj_list.append(obj)
        serializer = self.any_tag_serializer.create_with_obj(obj)
        self.serializers.append(serializer)

    def add_many(self, list: list[Tag]):
        for tag in list: self.add(tag)

    def get_info(self):
        if not self.serializers:
            return
        return [serializer.get_info() for serializer in self.serializers]

    @classmethod
    def create(self, list: list[dict]):
        ins = self()
        for dict in list:
            obj = self.any_tag_serializer.create(**dict)
            ins.add(obj.obj)
        return ins

class ManyTagSerializerForShowing(ManyTagSerializer):
    any_tag_serializer = AnyTagSerializerForShowing

class ParentTagSerializer(TagSerializer):
    tag = ParentTag
    creation_serializer = AnyTagSerializer
    informing_many_serializer = ManyTagSerializer

    @classmethod
    def create(self, childs = [], **kwarg: dict):
        parent =  super().create(**kwarg)
        for child in childs:
            child['parent'] = parent.obj
            self.creation_serializer.create(**child)
        return parent

    def get_info(self) -> dict:
        info = super().get_info()
        serializer = self.informing_many_serializer()
        serializer.add_many(self.obj.childs)
        childs_info = serializer.get_info()
        info['childs'] = childs_info
        return info
    
class ParentTagSerializerForShowing(ParentTagSerializer):
    creation_serializer = AnyTagSerializerForShowing
    informing_many_serializer = ManyTagSerializerForShowing

class ChildTagSerializer(TagSerializer):
    tag = ChildTag

class ParentAndChildTagSerializer(ParentTagSerializer):
    tag = ParentAndChildTag

class ParentAndChildTagSerializerForShowing(ParentTagSerializerForShowing):
    tag = ParentAndChildTag

class FieldsetSerializer(ParentAndChildTagSerializer):
    tag = FieldSet

    def get_info(self):
        info = super().get_info()
        info['legend'] = self.obj.legend
        return info
    

class FieldsetSerializerForShowing(FieldsetSerializer):
    creation_serializer = AnyTagSerializerForShowing
    informing_many_serializer = ManyTagSerializerForShowing

class ListTagSerializer(ParentAndChildTagSerializer):
    tag = ListTag

    def get_info(self):
        info = super().get_info()
        info['name'] = self.obj.name
        return info
    
class ListTagSerializerForShowing(ListTagSerializer):
    creation_serializer = AnyTagSerializerForShowing
    informing_many_serializer = ManyTagSerializerForShowing
    
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

    @classmethod
    def create(self, list = None, **kwarg: dict):
        if list:
            list = List.objects.get(name = list['name'], company__name = list['company_name'], company__user__username = list['username'])
        kwarg['list'] = list
        return super().create(**kwarg)

    def get_info(self):
        info = super().get_info()
        list = self.obj.list
        if list:
            info['list'] = {
            'name': list.name,
            'company_name': list.company.name,
            'username': list.company.user.username,

            }
            return info
        info['list'] = None
        return info
    
class InputWithListSerializerForShowing(InputWithListSerializer):
    tag = InputWithList
    def get_info(self):
        info = super().get_info()
        list = info['list']
        if list:
            items = self.obj.list.get_items()
            items = [item.name for item in items]
            info['list']['items'] = items
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

serializer_types.add_clses([
    FieldsetSerializer,
    ListTagSerializer,
    RadioSerializer,
    CheckboxSerializer
])
serializer_types.add_clses_with_cls([
    [Body, ParentTagSerializer],
    [Div, ParentAndChildTagSerializer],
    [StringInput, InputWithListSerializer],
    [FloatInput, InputWithListSerializer],
    [IntegerInput, InputWithListSerializer],
])

serializer_types_for_showing.add_clses([
    FieldsetSerializerForShowing,
    ListTagSerializerForShowing,
    RadioSerializer,
    CheckboxSerializer
])
serializer_types_for_showing.add_clses_with_cls([
    [Body, ParentTagSerializerForShowing],
    [Div, ParentAndChildTagSerializerForShowing],
    [StringInput, InputWithListSerializerForShowing],
    [FloatInput, InputWithListSerializerForShowing],
    [IntegerInput, InputWithListSerializerForShowing],
])  