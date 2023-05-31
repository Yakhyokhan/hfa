from .abstract_tags import ParentTag, ChildTag, TagType
class Body(ParentTag):
    type = 'body'

TagType.add_cls(Body)

