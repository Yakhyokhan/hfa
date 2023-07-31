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
    def __init__(self, parent = None) -> None:
        self.check_parent(parent)

    def check_parent(self, parent):
        if parent:
            parent.add_child(self)
            return
        self.parent = None

class Parent(Ability):
    def __init__(self, root = False) -> None:
        self.not_child_err = 'have a variable which not be from child class '
        self.childs: list[Tag] = []
        self.root = root
        if root:
            self.names = []
    def __str__(self) -> str:
        return f'Parent({self.childs})'

    def __repr__(self) -> str:
        return self.__str__()
    
    def is_child(self, child):
        if not issubclass(child.__class__, Child):
            return False
        return True

    def is_name_not_exist(self, name):
        return True
    
    def add_child(self, child:Child):
        assert self.is_child(child), str(child) + 'is not Child class'
        if issubclass(child.__class__, Parent):
            if child.root:
                for name in child.names:
                    self.is_name_not_exist(name)
        elif issubclass(child.__class__, FieldHabitude):
            name = child.name
            self.is_name_not_exist(name)
        self.childs.append(child)
        child.parent = self

    def add_childs(self, childs):
        for child in childs:
            self.add_child(child)
        
    def delete_child(self, child: Child = 0):
        self.childs.remove(child)
    
    def empty_childs(self):
        self.childs = []

def check_name(name, names: list, obj):
    assert not name in names, name + ' is exist in root ' + obj.__str__()
    names.append(name)
    return True

class ParentTag(Tag, Parent):
    type = 'parent_tag'
    def __init__(self) -> None:
        super().__init__(root= True)

    def is_name_not_exist(self, name):
        return check_name(name, self.names, self)
        
    def for_str(self) -> str:
        info = super().for_str()
        return info +  f', childs:{self.childs}'

class ParentFactoryWith:
    type : str
    @classmethod
    def add_childs(self,parent:ParentTag, childs = []):
        pass

class ParentFactoryWithChildClass(ParentFactoryWith):
    type = 'with_child'
    @classmethod
    def add_childs(self, parent:ParentTag, childs = []):
        parent.add_childs(childs)

class ParentTagFactory(TagFactory):
    res_class = ParentTag
    @classmethod
    def create(self, childs:list[Tag] = [], **kwarg):
        res_obj = super().create(**kwarg)
        creation_type = ParentFactoryWithChildClass
        creation_type.add_childs(res_obj, childs)
        return res_obj

class ChildTag(Tag, Child):
    type = 'child_tag'

    def for_str(self):
        info =  super().for_str()
        return info + f', parent: {self.parent}'

class ChildTagFactory(TagFactory):
    res_class = ChildTag

class ParentAndChildTag(Tag, Parent, Child):
    type = 'parent_and_child_tag'

    def __init__(self, parent: Parent = None) -> None:
        root = not parent
        super().__init__(root)
        self.check_parent(parent)

    def is_name_not_exist(self, name):
        if self.root:
            return check_name(name, self.names, self)
        return self.parent.is_name_not_exist(name)
            

    def for_str(self) -> str:
        info = super().for_str()
        return info +  f', parent: {self.parent}, childs:{self.childs}'

class ParentAndChildTagFactory(ParentTagFactory):
    res_class = ParentAndChildTag

class Habitude:
    pass

class FieldHabitude(Habitude):
    def __init__(self) -> None:
        self.name: str
        self.label: str

    def get_input_info(self):
        return {"type": self.name}

class LoopHabitude(Habitude):
    pass



        

# parent = AnyTagFactory.create(**{'type':'parent_tag', 'childs': [{'type': 'parent_and_child_tag', 'childs': [{'type': 'child_tag'},{'type': 'child_tag'}]}]})
# print(parent)
# {"type":"body", "childs": [{"type": "list", "name":"Anvar", "childs": [{"type": "input_string", "name":"Eshmat"},{"type": "input_string", "name":"Toshmat"}]}]}