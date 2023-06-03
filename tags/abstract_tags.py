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
    def add_types(self, types: list[str]):
            for type in types: self.add_type(type)

    @classmethod
    def add_clses(self, clses):
        for cls in clses: self.add_cls(cls)

# tag types
class TagType(Types):
    types: list = []
    @classmethod
    def add_type(self, type: str):
        self.types.append(type)    

    @classmethod
    def add_cls(self, cls: Tag):
        self.add_type(cls.type)

    @classmethod
    def get_type(self,i):
        return self.types[i]
    
            
    
TagType.add_cls(Tag)
class TagFactory:
    '''
    parent class to create HTML tag classes
    '''
    res_class = Tag
    @classmethod
    def create(self, **kwarg):
        return self.res_class(**kwarg)
    
    @classmethod
    def get_info(self, tag: res_class):
        return {'type': tag.type}


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
    
        


TagFactoriesType.add_cls(TagFactory)

#to create any HTML tag from all Tags
class AnyTagFactory(TagFactory):
    @classmethod
    def create(self, type:str, **kwarg):
        tag_factory_type =  TagFactoriesType.get_type(type)
        tag = tag_factory_type.create(**kwarg)
        return tag
    
    @classmethod
    def get_info(self, tag: Tag):
        factory = TagFactoriesType.get_factory_with_cls(tag)
        return factory.get_info(tag)



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
        
    def delete_child(self, child: Child = 0):
        self.childs.remove(child)
    

class ParentTag(Tag, Parent):
    type = 'parent_tag'
    def __init__(self):
        super().__init__()

        
    def for_str(self) -> str:
        info = super().for_str()
        return info +  f', childs:{self.childs}'

    
TagType.add_cls(ParentTag)

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
    
    @classmethod
    def get_info(self, tag: res_class):
        info = super().get_info(tag)
        childs_info = self.get_childs_info(tag.childs)
        info.update(childs_info)
        return info
    
    @classmethod
    def get_childs_info(self, childs: list[Tag]):
        childs_info = []
        for child in childs:
            factory = TagFactoriesType.get_factory_with_cls(child)
            info = factory.get_info(child)
            childs_info.append(info)
        return {'childs': childs_info}


    
TagFactoriesType.add_cls(ParentTagFactory)

class ChildTag(Tag, Child):
    type = 'child_tag'

TagType.add_cls(ChildTag)

class ChildTagFactory(TagFactory):
    res_class = ChildTag
    
TagFactoriesType.add_cls(ChildTagFactory)

class ParentAndChildTag(ParentTag, Child):
    type = 'parent_and_child_tag'

TagType.add_cls(ParentAndChildTag)

class ParentAndChildTagFactory(ParentTagFactory):
    res_class = ParentAndChildTag

TagFactoriesType.add_cls(ParentAndChildTagFactory)



        

# parent = AnyTagFactory.create(**{'type':'parent_tag', 'childs': [{'type': 'parent_and_child_tag', 'childs': [{'type': 'child_tag'},{'type': 'child_tag'}]}]})
# print(parent)
