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
    
    def __str__(self):
        return f'{self.cls_name()}({self.for_str()})'
    
    def for_str(self):
        return f'type:{self.type}'
    
    def __repr__(self) -> str:
        return self.__str__()
    
class Types:
    types: object
    @classmethod
    def add_type(self):
        pass  

    @classmethod
    def add_cls(self):
        pass

    @classmethod
    def get_all_types(self):
        return self.types
    
    @classmethod
    def get_type(self):
        pass


    @classmethod
    def add_clses(self, clses):
        for cls in clses: self.add_cls(cls)
    
    @classmethod
    def add_clses_with_cls(self, clses: list[list[Tag, Tag]]):
        for cls in clses: self.add_type(cls[0].type, cls[1])

# tag types
class TagType(Types):
    types: list = {}
    @classmethod
    def add_type(self, type: str, tag):
        self.types[type] = tag

    @classmethod
    def add_cls(self, cls: Tag):
        self.add_type(cls.type, cls)

    

    @classmethod
    def get_type(self,i):
        return self.types[i]

class TagFactory:
    '''
    parent class to create HTML tag classes
    '''
    res_class = Tag
    @classmethod
    def create(self, type, **kwarg):
        cls = TagType.get_type(type)
        return cls(**kwarg)
    
# to look for tag factories with type of tag
class TagFactoriesType(Types):
    types = {}
    @classmethod
    def add_type(self, type: str, factory:TagFactory):
        self.types[type] = factory   

    @classmethod
    def add_cls(self, cls: TagFactory):
        self.add_type(cls.res_class.type, cls)

    @classmethod
    def get_type(self, type: str) -> TagFactory:
        return self.types[type]
    
    @classmethod
    def get_factory_with_cls(self, cls: Tag) -> TagFactory:
        return self.types[cls.type]

#to create any HTML tag from all Tags
class AnyTagFactory(TagFactory):
    @classmethod
    def create(self, **kwarg):
        type = kwarg['type']
        tag_factory_type =  TagFactoriesType.get_type(type)
        tag = tag_factory_type.create(**kwarg)
        return tag
    
    @classmethod
    def get_info(self, tag: Tag):
        factory = TagFactoriesType.get_factory_with_cls(tag)
        return factory.get_info(tag)

class ManyTagFactory:

    @classmethod
    def create(self, list:list[dict]):
        tags = []
        for child in list:
            type = child.pop('type')
            tags.append(AnyTagFactory.create(type = type, **child))
        return tags

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
    
    def add_child(self, child:Child):
        assert self.is_child(child), str(child) + 'is not Child class'
        self.childs.append(child)

    def add_childs(self, childs):
        for child in childs:
            self.add_child(child)
        
    def delete_child(self, child: Child = 0):
        self.childs.remove(child)
    
    def empty_childs(self):
        self.childs = []

class ParentTag(Tag, Parent):
    type = 'parent_tag'
    def __init__(self):
        super().__init__()

        
    def for_str(self) -> str:
        info = super().for_str()
        return info +  f', childs:{self.childs}'

class ParentFactoryWith:
    type : str
    @classmethod
    def add_childs(self,parent:ParentTag, childs = []):
        pass

parent_tag_factory_type: dict[str, ParentFactoryWith] = {}

class ParentFactoryWithChildClass(ParentFactoryWith):
    type = 'with_child'
    @classmethod
    def add_childs(self, parent:ParentTag, childs = []):
        parent.add_childs(childs)
        
    
parent_tag_factory_type[ParentFactoryWithChildClass.type] = ParentFactoryWithChildClass
    
class ParentFactoryWithDict(ParentFactoryWith):
    type = 'with_dict'
    @classmethod
    def add_childs(self, parent:ParentTag, childs: list[dict] = []):
        b = parent
        childs = ManyTagFactory.create(childs)
        ParentFactoryWithChildClass.add_childs(b, childs)
    
    
parent_tag_factory_type[ParentFactoryWithDict.type] = ParentFactoryWithDict

class ParentTagFactory(TagFactory):
    res_class = ParentTag
    @classmethod
    def create(self, *, creation_type = 'with_dict', childs:list[dict] = [], **kwarg):
        res_obj = super().create(**kwarg)
        creation_type = parent_tag_factory_type[creation_type]
        creation_type.add_childs(res_obj, childs)
        return res_obj

class ChildTag(Tag, Child):
    type = 'child_tag'

class ChildTagFactory(TagFactory):
    res_class = ChildTag

class ParentAndChildTag(ParentTag, Child):
    type = 'parent_and_child_tag'

class ParentAndChildTagFactory(ParentTagFactory):
    res_class = ParentAndChildTag

class Habitude:
    pass

class FieldHabitude(Habitude):
    def __init__(self) -> None:
        self.name: str
        self.label: str

class LoopHabitude(Habitude):
    pass



        

# parent = AnyTagFactory.create(**{'type':'parent_tag', 'childs': [{'type': 'parent_and_child_tag', 'childs': [{'type': 'child_tag'},{'type': 'child_tag'}]}]})
# print(parent)
