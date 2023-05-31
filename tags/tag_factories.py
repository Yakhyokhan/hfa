from .abstract_tags import TagFactoriesType, AnyTagFactory, \
    ParentTagFactory, ChildTagFactory, ParentAndChildTagFactory
from .tags import Body
class BodyFactory(ParentTagFactory):
    res_class = Body

TagFactoriesType.add_cls(Body, BodyFactory)