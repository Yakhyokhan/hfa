'''
this party is to detect HTML tags
'''

class Tag:
    '''
    base HTML tag class
    '''
    type: str = 'tag'
    @classmethod
    def cls_name(self):
        return self.__name__


    def get_info(self):
        return {'type': self.type}
    
    def __str__(self):
        return f'{self.cls_name()}(type:{self.type})'
    
    def __repr__(self) -> str:
        return self.__str__()
    
tag_type = Tag.type

#to look for tag class with its type  
tags = [
    tag_type
]
    

class TagFactory:
    '''
    parent class to create HTML tag classes
    '''
    res_class = Tag
    @classmethod
    def create(self, **kwarg):
        return self.res_class()


# to look for tag factories with type of tag
tag_factories: dict[str: TagFactory] = {
    tag_type: TagFactory
}

#to create any HTML tag from all Tags
class AnyTagFactory:
    @classmethod
    def create(self, type:str, **kwarg):
        tag_factory_type =  tag_factories[type]
        tag = tag_factory_type.create(**kwarg)
        return tag

class Ability:
    '''
    abstract class for abilities
    '''
    pass

class Child(Ability):
    pass

class Parent(Ability):
    def __init__(self) -> None:
        self.not_child_err = 'have a variable which not be from child class '
        self.childs: list[Tag] = []
    def __str__(self) -> str:
        return f'Parent({self.childs})'

    def __repr__(self) -> str:
        return self.__str__()
    
    def is_child(self, child):
        if not issubclass(child.__class__, Child):
            return False
        return True
    
    def get_childs_info(self):
        return {'childs': [i.get_info() for i in self.childs]}
    
    def add_child(self, child:Child):
        assert self.is_child(child), str(child) + 'is not Child class'
        self.childs.append(child)
        
    def delete_child(self, child: Child = 0):
        self.childs.remove(child)
    

class ParentTag(Tag, Parent):
    type = 'parent_tag'
    def __init__(self):
        super().__init__()

    def get_info(self):
        info = super().get_info()
        childs_info = self.get_childs_info()
        info.update(childs_info)
        return info
        
    def __str__(self) -> str:
        return f'{self.cls_name()}(type:{self.type}, childs:{self.childs})'

    def __repr__(self) -> str:
        return self.__str__()
    
parent_tag_type = ParentTag.type

tags.append(parent_tag_type)

class ParentFactoryWith:
    type : str
    @classmethod
    def create(self,parent:ParentTag, childs = []):
        pass

parent_tag_factory_type = {}

class ParentFactoryWithChildClass(ParentFactoryWith):
    type = 'with_child'
    @classmethod
    def create(self,parent:ParentTag, childs = []):
        b = parent
        self.set_childs_with_child_class(b, childs)
        return  b
    
    @staticmethod
    def set_childs_with_child_class(parent:Parent, childs: list[Child] = [] ):
        for child in childs:
            parent.add_child(child)
    
parent_tag_factory_type[ParentFactoryWithChildClass.type] = ParentFactoryWithChildClass
    
class ParentFactoryWithDict(ParentFactoryWith):
    type = 'with_dict'
    @classmethod
    def create(self,parent:ParentTag, childs: list[dict] = []):
        b = parent
        self.set_childs_with_dict(b, childs)
        return b
    
    @staticmethod
    def set_childs_with_dict(parent:Parent , childs:list[dict]):
        for child in childs:
            type = child.pop('type')
            parent.add_child(AnyTagFactory.create(type = type, **child))
    
parent_tag_factory_type[ParentFactoryWithDict.type] = ParentFactoryWithDict

class ParentTagFactory(TagFactory):
    res_class = ParentTag
    @classmethod
    def create(self, creation_type = 'with_dict', childs:list[dict] = [], **kwarg):
        res_obj = super().create(**kwarg)
        creation_type = parent_tag_factory_type[creation_type]
        return creation_type.create(res_obj, childs)


    
tag_factories[parent_tag_type] = ParentTagFactory

class ChildTag(Tag, Child):
    type = 'child_tag'

child_tag_type = ChildTag.type

tags.append(child_tag_type)

class ChildTagFactory(TagFactory):
    res_class = ChildTag
    
tag_factories[child_tag_type] = ChildTagFactory

class ParentAndChildTag(ParentTag, Child):
    type = 'parent_and_child_tag'

parent_and_child_tag_type = ParentAndChildTag.type

tags.append(parent_and_child_tag_type)

class ParentAndChildTagFactory(ParentTagFactory):
    res_class = ParentAndChildTag

tag_factories[parent_and_child_tag_type] = ParentAndChildTagFactory

class Body(ParentTag):
    type = 'body'

body_type = Body.type
tags.append(body_type)

class BodyFactory(ParentTagFactory):
    res_class = Body

tag_factories[body_type] = BodyFactory

        

# parent = AnyTagFactory.create(**{'type':'body', 'childs': [{'type': 'parent_and_child_tag', 'childs': [{'type': 'child_tag'},{'type': 'child_tag'}]}]})
# parent
# # body = AnyTagFactory.create(type= 'body', creation_type = 'with_child', childs = [Body(), Input()])
# # print('........')
# # print(body)
# # print(body2)
# print('....................')
# print(parent)
# print('..........') 
