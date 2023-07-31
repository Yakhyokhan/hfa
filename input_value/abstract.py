from rest_framework import validators
from tags.tags import default_values
class Value:
    type = "value"
    def __init__(self, value = ...) -> None:
        self.value = value

class ValueWithType:
    type = "value_with_type"
    value_type = ...
    def __init__(self, name, value= default_values[value_type]):
        val_type = self.value_type
        if not type(value) == val_type: raise  validators.ValidationError(f'{value} is not {val_type}')
        super().__init__(name,value)

class ValueTypes:
    def __init__(self) -> None:
        self.value_types = {}

    def add(self, type, value):
        self.value_types[type] = value

    def add_cls(self, cls: Value):
        self.add(cls.type, cls)
    
    def add_many(self, type_list: list[str, Value]):
        for type in type_list:
            self.add(*type)
    
    def add_many_cls(self, cls_list: list[Value]):
        for cls in cls_list:
            self.add_cls(cls)

# class InputValue:
#     input_type = FieldHabitude
#     value_type = Value
#     def __init__(self, input: input_type, value: value_type):
#         input_type = self.input_type
#         value_type = self.value_type
#         if not issubclass(input.__class__, input_type):
#             raise validators.ValidationError(f'{input}is not subclass {input_type}')
#         if not issubclass(value.__class__, value_type):
#             raise validators.ValidationError(f'{value} is not subclass {value_type}')
#         self.input = input
#         self.value = value

class NumberValue(ValueWithType):
    type = 'number'
    value_type = int

class StringValue(ValueWithType):
    type = 'string'
    value_type = str

class FloatValue(ValueWithType):
    type = 'float'
    value_type = float

class BooleanValue(ValueWithType):
    type = "boolean"
    value_type = bool

class ListItem:
    value_type = Value
    def __init__(self, item: list[value_type]) -> None:
        self.values = []

    def add(self, value):
        if not issubclass(value.__class__, self.value_type): 
            raise validators.ValidationError(f"part is not {self.value_type}")
        self.values.append(value)

    def add_many(self, values):
        for value in values:
            self.add(value)

    def is_similar(self, obj):
        for i, value in enumerate(self.values):
            if value.__class__ != obj[i].__class__: return False
        return True

class ListValue(Value):
    type = 'list_value'
    list_item = ListItem
    def __init__(self, name, item_model:ListItem) -> None:
        super().__init__(name, [])
        if not issubclass(item_model.__class__, self.list_item):
            raise validators.ValidationError(f"{item_model} is not {self.list_item}")
        self.item_model = item_model

    def add(self, item: list_item):
        if not self.item_model.is_similar(item):
            raise validators.ValidationError(f'{item} is not similar with {self.item_model}')
        self.value.append(item)

    def add_many(self, items):
        for item in items:
            self.add(item)


