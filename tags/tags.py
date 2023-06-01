from tags.abstract_tags import Child
from .abstract_tags import TagType, ParentTag, ChildTag,ParentAndChildTag
from page.models import List

class Habitude:
    pass

class FieldHabitude(Habitude):
    def __init__(self) -> None:
        self.name: str

class LoopHabitude(Habitude):
    pass

class Body(ParentTag):
    type = 'body'

TagType.add_cls(Body)

class Div(ParentAndChildTag):
    type = 'div'

TagType.add_cls(Div)

class FieldSet(ParentAndChildTag):
    type = 'fieldset'
    def __init__(self, legend = ''):
        super().__init__()
        self.legend = legend

    def __str__(self) -> str:
        return f'{self.cls_name()}(type:{self.type}, legend:\'{self.legend}\', childs:{self.childs}'

TagType.add_cls(FieldSet)


class ListTag(ParentAndChildTag, FieldHabitude, LoopHabitude):
    type = 'list'
    def __init__(self, name:str):
        super().__init__()
        self.name = name

    def __str__(self) -> str:
        return f'{self.cls_name()}(type: {self.type}, name:{self.name}, childs: {self.childs})'
    
    def add_child(self, child: Child):
        assert not type(child) == ListTag, 'List objects don\'t acsess itself'
        return super().add_child(child)
    
TagType.add_cls(ListTag)

class Input(ChildTag):
    type = 'input'
    def __init__(self, name, value = '') -> None:
        super().__init__()
        self.name = name
        self.value = value

    def __str__(self):
        return f'{self.cls_name()}(type:{self.type}, name:{self.name}, value:\'{self.value}\')'

TagType.add_cls(Input)
