from .serializer import AnyTagSerializer, ManyTagSerializer, TagSerializer
from .field_finders import AnyFieldFinder

class DbWriter:
    def __init__(self, serializer: TagSerializer, ):
        assert issubclass(serializer.__class__, TagSerializer), f'{serializer} is not Serializer'
        self.serializer = serializer
        self.fields_serializer = self.set_fields_serializer()
    
    def get_data(self):
        return self.serializer.data

    def get_fields(self):
        return AnyFieldFinder.find(self.serializer.obj)
    
    def set_fields_serializer(self):
        fields = self.get_fields()
        serializer =  ManyTagSerializer()
        serializer.add_many(fields)
        return serializer

    def get_fields_data(self):
        return self.fields_serializer.data
        
    
    @classmethod
    def create(self, dict):
        serializer =  AnyTagSerializer.create(dict)
        ins = DbWriter
        return ins(serializer)


    
