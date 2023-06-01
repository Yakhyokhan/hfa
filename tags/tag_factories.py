from .abstract_tags import TagFactoriesType, AnyTagFactory, \
    ParentTagFactory, ChildTagFactory, ParentAndChildTagFactory
from .tags import Body, Div, FieldSet, ListTag, Input
class BodyFactory(ParentTagFactory):
    res_class = Body

TagFactoriesType.add_cls(BodyFactory)

class DivFactory(ParentAndChildTagFactory):
    res_class = Div

TagFactoriesType.add_cls(DivFactory)

class FieldSetFactory(ParentAndChildTagFactory):
    res_class = FieldSet

    @classmethod
    def get_info(self, tag:res_class):
        info = super().get_info(tag)
        info['legend'] = tag.legend
        return info
    
TagFactoriesType.add_cls(FieldSetFactory)

class ListTagFactory(ParentAndChildTagFactory):
    res_class = ListTag

    @classmethod
    def get_info(self, tag: res_class):
        info = super().get_info(tag)
        info['name'] = tag.name
        return info

TagFactoriesType.add_cls(ListTagFactory)

class InputFactory(ChildTagFactory):
    res_class = Input

    @classmethod
    def get_info(self, tag: res_class):
        info = super().get_info(tag)
        info['name'] = tag.name
        info['value'] = tag.value
        return info

TagFactoriesType.add_cls(InputFactory)