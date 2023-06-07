from .abstract_tags import TagType, ParentTag, ChildTag,ParentAndChildTag, FieldHabitude, LoopHabitude
from page.models import List



class Body(ParentTag):
    type = 'body'

class Div(ParentAndChildTag):
    type = 'div'

class FieldSet(ParentAndChildTag):
    type = 'fieldset'
    def __init__(self, parent = None, legend = ''):
        super().__init__(parent)
        self.legend = legend

    def for_str(self) -> str:
        return f'type:{self.type}, legend:\'{self.legend}\', childs:{self.childs}'

class ListTag(ParentAndChildTag, FieldHabitude, LoopHabitude):
    type = 'list'
    def __init__(self, name:str, parent = None, label = None):
        self.name = name
        super().__init__(parent)
        if not parent:
            self.names = [self.name]
        if not label:
            label = name
        self.label = label

    def for_str(self) -> str:
        return f'type: {self.type}, parent: {self.parent}, name:{self.name}, childs: {self.childs}'
    
    def add_child(self, child):
        assert not type(child) == ListTag, 'List objects don\'t acsess itself'
        return super().add_child(child)

class Input(ChildTag, FieldHabitude):
    type = 'input'
    value_type: object
    def __init__(self, name, value, parent = None, label = None) -> None:
        assert  type(value) == self.value_type, f'{value} is not {self.value_type.__name__}'
        self.name = name
        super().__init__(parent)
        self.value = value
        if not label:
            label = name
        self.label = label

    def for_str(self):
        info = super().for_str()
        return info +  f', name:\'{self.name}\', value:\'{self.value}\''
    
class InputWithList(Input):
    type = 'input_with_list'
    def __init__(self, name, parent = None, label = None, value='', list: List = None) -> None:
        assert list == None or isinstance(list, List), f'{list} is not List model'
        super().__init__(name, value, parent, label)
        self.list = list

    def for_str(self):
        info =  super().for_str()
        return info + f', list: {self.list}'

class StringInput(InputWithList):
    type = 'input_string'
    value_type = str

class IntegerInput(InputWithList):
    type = 'input_number'
    value_type = int

class FloatInput(InputWithList):
    type = 'input_float'
    value_type = float

class Checkbox(Input):
    type = 'checkbox'
    value_type = str
    def __init__(self, name, parent = None, value= True, is_checked = False, label = None) -> None:
        super().__init__(name, value, parent, label)
        self.is_checked = is_checked

radio_default_value = {
    str: '',
    int: 0,
    float: 0.00,
    bool: False
    }

class Radio(Input):
    type = 'radio'
    def __init__(self, name, value, parent = None, value_type = str, radio_list = [], label = None) -> None:
        self.value_type = value_type
        self.check_radio_list(radio_list)
        self.radio_list = radio_list
        self.check_value(value)
        super().__init__(name, value, parent, label)

    def check_any_value(self, value):
        assert type(value) == self.value_type, f'{value} is not {self.value_type}'

    def check_radio_list(self, radio_list):
        for item in radio_list:
            self.check_any_value(item)

    def check_value(self, value):
        assert value in self.radio_list or value == radio_default_value[self.value_type], \
            f'{value} is not available in radio_list:{self.radio_list}'

    def for_str(self):
        info = super().for_str()
        return info + f', radio_list:{self.radio_list}'

TagType.add_clses([
    Body,
    Div,
    FieldSet,
    ListTag,
    Input,
    StringInput,
    IntegerInput,
    FloatInput,
    Checkbox,
    Radio
])
