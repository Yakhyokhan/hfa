from .abstract_tags import TagType, ParentTag, ChildTag,ParentAndChildTag, FieldHabitude, LoopHabitude
from page.models import List



class Body(ParentTag):
    type = 'body'

class Div(ParentAndChildTag):
    type = 'div'

class FieldSet(ParentAndChildTag):
    type = 'fieldset'
    def __init__(self, legend = ''):
        super().__init__()
        self.legend = legend

    def for_str(self) -> str:
        return f'type:{self.type}, legend:\'{self.legend}\', childs:{self.childs}'

class ListTag(ParentAndChildTag, FieldHabitude, LoopHabitude):
    type = 'list'
    def __init__(self, name:str):
        super().__init__()
        self.name = name

    def for_str(self) -> str:
        return f'type: {self.type}, name:{self.name}, childs: {self.childs}'
    
    def add_child(self, child):
        assert not type(child) == ListTag, 'List objects don\'t acsess itself'
        return super().add_child(child)

class Input(ChildTag, FieldHabitude):
    type = 'input'
    value_type: object
    def __init__(self, name, value) -> None:
        assert  type(value) == self.value_type, f'{value} is not {self.value_type.__name__}'
        super().__init__()
        self.name = name
        self.value = value

    def for_str(self):
        info = super().for_str()
        return info +  f', name:\'{self.name}\', value:\'{self.value}\''
    
class InputWithList(Input):
    type = 'input_with_list'
    def __init__(self, name, value='', list: List = None) -> None:
        super().__init__(name, value)
        self.list = list

    def for_str(self):
        info =  super().for_str()
        return info + ', list'

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
    value_type = bool
    def __init__(self, name, value= True) -> None:
        super().__init__(name, value)

radio_default_value = {
    str: '',
    int: 0,
    float: 0.00,
    bool: False
    }

class Radio(Input):
    type = 'radio'
    def __init__(self, name, value, value_type = str, radio_list = []) -> None:
        self.value_type = value_type
        self.check_radio_list(radio_list)
        self.radio_list = radio_list
        self.check_value(value)
        super().__init__(name, value)

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
