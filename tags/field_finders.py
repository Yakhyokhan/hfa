from .abstract_tags import Tag, Types, AnyTagFactory
from .tags import *

class TagFieldFinder:
    tag = Tag

    @classmethod
    def find(self, obj:tag):
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
        find_class = TagFildFinderTypes.get_type(obj.type)
        return find_class.find(obj)
    
class ManyFieldsFinder:

    @classmethod
    def find(self, objs = list[Tag]):
        list = []
        for obj in objs:
            field = AnyFieldFinder.find(obj)
            if field != None:
                list.append(field)
        return list
    
class ParentFinder(TagFieldFinder):
    tag = ParentTag

    @classmethod
    def find(self, obj: tag):
        childs = ManyFieldsFinder.find(obj.childs)
        if issubclass(obj.__class__, FieldHabitude): 
            new_obj = AnyTagFactory.create(type = obj.type)
            new_obj.add_childs(childs)
            return new_obj
        return childs
    
class ChildFinder(TagFieldFinder):
    tag = ChildTag

class ParentAndCHildTagFinder(ParentFinder):
    tag = ParentAndChildTag

TagFildFinderTypes.add_clses_with_tag([
    [Body, ParentFinder],
    [Div, ParentAndChildTag],
    [FieldSet, ParentAndChildTag],
    [ListTag, ParentAndChildTag],
    [StringInput, ChildFinder],
    [IntegerInput, ChildFinder],
    [FloatInput, ChildFinder],
    [Checkbox, ChildFinder],
    [Radio, ChildFinder],
])

