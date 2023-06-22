from rest_framework import serializers
from .models import Html
from tags.serializer import (ManyTagSerializerForShowing, AnyTagSerializerForShowing, 
    AnyTagSerializer, ManyTagSerializer)


class AnyTagField(serializers.JSONField):
    def to_internal_value(self, data):
        return AnyTagSerializer.create(**data).obj
    
    def to_representation(self, value):
        return AnyTagSerializerForShowing.create_with_obj(value).get_info()

class ManyTagField(serializers.JSONField):
    def to_internal_value(self, data):
        return ManyTagSerializer.create(data).obj_list
    
    def to_representation(self, value):
        serializer = ManyTagSerializerForShowing()
        serializer.add_many(value)
        return serializer.get_info()

class HtmlSerializer(serializers.ModelSerializer):
    tags = AnyTagField()
    inputs = ManyTagField(read_only = True)
    class Meta:
        model = Html
        fields = '__all__'