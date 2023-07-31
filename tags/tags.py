from .abstract_tags import TagType, ParentTag, ChildTag,ParentAndChildTag, FieldHabitude, LoopHabitude, Parent
from value_list.models import List



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
        self.primary_child = None

    def for_str(self) -> str:
        return f'type: {self.type}, parent: {self.parent}, name:{self.name}, primary_child: {self.primary_child}, childs: {self.childs}'
    
    def add_child(self, child):
        assert not type(child) == ListTag, 'List objects don\'t acsess itself'
        super().add_child(child)

    
    def find_primary(self, childs, p_child_name):
        for child in childs:
            if issubclass(child.__class__, Parent): 
                p_child = self.check_primary(child.childs, p_child_name)
                if p_child: 
                    return p_child
            if issubclass(child.__class__, Input):
                if child.name == p_child_name: 
                    return child
        return None

    def update_primary_child(self, p_child_name):
        p_child = self.find_primary(self.childs, p_child_name)
        assert p_child, f"{p_child_name} is not exist in childs {self.childs}"
        self.primary_child = p_child.name
        p_child.required = True

    def get_input_info(self):
        parent = self.parent.name if self.parent else None
        primary_child = self.primary_child
        info =  {"type":self.type, "name":self.name, "parent":parent, "primary_child": primary_child,
                 "childs":[x.get_input_info() for x in self.childs if issubclass(x.__class__, FieldHabitude)]
                 }
        return info

class Input(ChildTag, FieldHabitude):
    type = 'input'
    value_type: object
    def __init__(self, name, value, parent = None, label = None, required = False) -> None:
        assert  type(value) == self.value_type, f'{value} is not {self.value_type.__name__}'
        self.name = name
        self.required = required
        super().__init__(parent)
        self.value = value
        if not label:
            label = name
        self.label = label

    def for_str(self):
        info = super().for_str()
        return info +  f', name:\'{self.name}\', value:\'{self.value}\', required: {self.required}'
    
    def get_input_info(self):
        parent = self.parent
        if parent:
            parent = parent.name
        info = {"type":self.type, "parent": parent, "name": self.name, "required":self.required}
        return info
    
class InputWithList(Input):
    type = 'input_with_list'
    def __init__(self, name, parent = None, label = None, value='', list: List = None, required = False) -> None:
        assert list == None or isinstance(list, List), f'{list} is not List model'
        super().__init__(name, value, parent, label, required)
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
    value_type = bool

default_values = {
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
        assert value in self.radio_list or value == default_values[self.value_type], \
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
