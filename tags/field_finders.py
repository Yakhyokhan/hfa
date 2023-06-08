from .abstract_tags import Tag, Types, AnyTagFactory, Parent, Child
from .tags import *
from copy import copy

class TagNotFieldFinder:
    tag = Tag

    @classmethod
    def find(self, obj:tag):
        return None
    
class TagFieldFinder(TagNotFieldFinder):
    tag = Tag

    @classmethod
    def find(self, obj: tag):
        return self.is_field(obj)
        
    @classmethod
    def is_field(self, obj):
        if issubclass(obj.__class__, FieldHabitude):
            return obj

class TagFildFinderTypes(Types):
    types = {}

    @classmethod
    def add_type(self, type, find_field):
        self.types[type] = find_field

    @classmethod
    def add_cls(self, find_field: TagFieldFinder):
        self.add_type(find_field.tag.type, find_field)

    @classmethod
    def add_clses_with_tag(self, types: list[list[Tag, TagFieldFinder]]):
        for type in types: self.add_type(type[0].type, type[1])

    @classmethod
    def add_clses(self, clses):
        for cls in clses: self.add_cls(cls)

    @classmethod
    def get_type(self, type):
        return self.types[type]
    
    @classmethod
    def get_all_types(self):
        return self.types

class AnyFieldFinder:

    @classmethod
    def find(self, obj):
        if not obj:
            return
        find_class = TagFildFinderTypes.get_type(obj.type)
        return find_class.find(obj)
    
class ManyFieldsFinder:

    @classmethod
    def find(self, objs = list[Tag]):
        if not objs:
            return
        field_list = []
        for obj in objs:
            fields = AnyFieldFinder.find(obj)
            if type(fields) == list:
                for field in fields: field_list.append(field)
                continue
            if fields != None:
                field_list.append(fields)
        return field_list
    
class ParentNotFieldFinder(TagFieldFinder):
    tag = ParentTag

    @classmethod
    def find(self, obj: tag):
        return ManyFieldsFinder.find(obj.childs)
    
class ParentFieldFinder(ParentNotFieldFinder, TagFieldFinder):
    tag = Parent

    @classmethod
    def find(self, obj: tag):
        childs =  super().find(obj)

        childs = [copy(child) for child in childs]
        if self.is_field(obj): 
            new_obj = copy(obj)
            if issubclass(new_obj.__class__, Child):
                new_obj.parent = None
                new_obj.root = True
                new_obj.names = []
            new_obj.childs = []
            new_obj.add_childs(childs)
            return new_obj
        return childs

TagFildFinderTypes.add_clses_with_tag([
    [Body, ParentNotFieldFinder],
    [Div, ParentNotFieldFinder],
    [FieldSet, ParentNotFieldFinder],
    [ListTag, ParentFieldFinder],
    [StringInput, TagFieldFinder],
    [IntegerInput, TagFieldFinder],
    [FloatInput, TagFieldFinder],
    [Checkbox, TagFieldFinder],
    [Radio, TagFieldFinder],
])

