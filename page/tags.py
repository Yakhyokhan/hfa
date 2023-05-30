'''
this party is to detect HTML tags
'''

class Tag:
    '''
    base HTML tag class
    '''
    type: str = 'tag'


    def get_info(self):
        return {'type': self.type}
    
    def __str__(self):
        return f'Tag(type:{self.type})'
    
    def __repr__(self) -> str:
        return self.__str__()
    
tag_type = Tag.type

#to look for tag class with its type  
tags:dict[str:Tag] = {
    tag_type: Tag
}
    

class TagFactory:
    '''
    abstract class to create HTML tag classes
    '''
    @classmethod
    def create(self):
        return Tag()


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
    def __init__(self, childs = []) -> None:
        not_child_err = f'{childs} have a variable which not be from child class '
        assert self.__is_child(childs), not_child_err
        self.childs: list[Tag, Child] = childs
    
    def __str__(self) -> str:
        return f'Parent({self.childs})'

    def __repr__(self) -> str:
        return self.__str__()
    
    def __is_child(self, childs):
        for i in childs:
            if not issubclass(i.__class__, Child):
                return False
        return True
    
    def get_childs_info(self):
        return [i.get_info() for i in self.childs]
    
    def add_child(self, child:Child):
        # assert issubclass(child.__class__, Child), f'{child} is not CHild class'
        self.childs.append(child)
        
    def delete_child(self, child: Child = 0):
        self.childs.remove(child)
    
    def set_childs(self, childs:list[dict]):
        for child in childs:
            type = child.pop('type')
            self.add_child(AnyTagFactory.create(type = type, **child))

# class Identificator:
#     id = 0
#     @classmethod
#     def get_id(self):
#         res = self.id
#         self.id += 1
#         return res

class Body(Tag, Parent, Child):
    type = 'body'
    def __init__(self, childs: list[Tag, Child] = []):
        super().__init__(childs)
        
    def __str__(self) -> str:
        return f'Body(type:{self.type}, childs:{self.childs})'

    def __repr__(self) -> str:
        return self.__str__()
    
body_type = Body.type

class BodyFactoryWith:
    type : str
    @classmethod
    def create(self, childs = []):
        pass

body_factory_type = {}

class BodyFactoryWithChildClass:
    type = 'with_child'
    @classmethod
    def create(self, childs = []):
        return Body(childs)
    
body_factory_type[BodyFactoryWithChildClass.type] = BodyFactoryWithChildClass
    
class BodyFactoryWithDict:
    type = 'with_dict'
    @classmethod
    def create(self, childs: list[dict] = []):
        b = Body()
        b.set_childs(childs)
        return b
    
body_factory_type[BodyFactoryWithDict.type] = BodyFactoryWithDict

class BodyFactory:
    @classmethod
    def create(self, creation_type = 'with_dict', childs:list[dict] = []):
        creation_type = body_factory_type[creation_type]
        return creation_type.create(childs)


    
tag_factories[body_type] = BodyFactory

class Input(Tag, Child):
    type = 'input'
    def __init__(self, value = ''):
        self.value = value

    def __str__(self):
        return f'Input(type:\'{self.type}\',value:\'{self.value}\')'
input_type = Input.type

tags[input_type] = Input

class InputFactory():
    @classmethod
    def create(self,value = ''):
        return Input(value)
    
tag_factories[input_type] = InputFactory

        

# parent = AnyTagFactory.create(type='body', creation_type = 'with_dict', childs = [{'type': 'body', 'childs': [{'type': 'input', 'value': '434343'},{'type': 'input'}]}])
# parent
# # body = Body([Body()])
# # body2 = Body()
# print('........')
# # print(body)
# # print(body2)
# print('....................')
# print(parent)
# print('..........') 
