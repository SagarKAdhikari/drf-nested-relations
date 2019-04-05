
from rest_framework import serializers
from .serializers import request_cfg
from functools import wraps


def helper_data_add(func):

    @wraps(func)
    def wrapper(self, validated_data):
        maps = self.pop_helper_data(validated_data)
        obj = func(self, validated_data)
        self.save_helper_data(maps, obj)
        obj.save()
        return obj
    return wrapper


def helper_data_update_with_delete(func):

    @wraps(func)
    def wrapper(self, instance, validated_data):

        if hasattr(request_cfg, 'delete'):
            for each in request_cfg.delete:
                each.delete()

        request_cfg.delete = []

        for key, value in self.Meta.nestedSerializer.items():

            if issubclass(
                value['serializer_class'],
                serializers.ModelSerializer
            ):

                if eval("'"+key+"'") in validated_data:

                    data = validated_data.pop(eval("'"+key+"'"))

                    if 'kwargs' in value:
                        kwargs = {value['kwargs']: instance}
                    else:
                        kwargs = {'content_object': instance}

                    for serializer in data:
                        serializer.save(**kwargs)

        obj = func(self, instance, validated_data)
        return obj

    return wrapper


def helper_data_update(func):

    @wraps(func)
    def wrapper(self, instance, validated_data):

        for key, value in self.Meta.nestedSerializer.items():

            if issubclass(
                value['serializer_class'],
                serializers.ModelSerializer
            ):
                if eval("'"+key+"'") in validated_data:

                    data = validated_data.pop(eval("'"+key+"'"))

                    if 'kwargs' in value:
                        kwargs = {value['kwargs']: instance}
                    else:
                        kwargs = {'content_object': instance}

                    for serializer in data:
                        serializer.save(**kwargs)

        obj = func(self, instance, validated_data)
        return obj

    return wrapper