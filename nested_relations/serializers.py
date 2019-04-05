
import threading
from rest_framework import serializers

request_cfg = threading.local()


def validate_json(self, data, serializer_class, many=False):

    serializer = None

    method = self.context['request'].method

    if method == 'PATCH':
        partial = True
    else:
        partial = False
    if issubclass(serializer_class, serializers.ModelSerializer):
        if data is None:
            data = []
        all_serializers = []
        if many and not isinstance(data, list):
            raise serializers.ValidationError(
                {'non_field_errors': 'Not a list'}
            )
        for each in data:
            if 'id' in each:
                id = each.pop('id')
                model = serializer_class.Meta.model

                try:
                    obj = model.objects.get(id=id)
                except model.DoesNotExist:
                    raise serializers.ValidationError('Object does not exist')

                if each == {}:
                    if not hasattr(request_cfg, 'delete'):
                        request_cfg.delete = []
                    request_cfg.delete.append(obj)
                    serializer = None

                else:
                    serializer = serializer_class(
                        obj,
                        data=each,
                        context={'request': self.context['request']},
                        partial=partial
                    )
     
            else:
                serializer = serializer_class(
                    data=each,
                    context={'request': self.context['request']}
                )

            if serializer:
                serializer.is_valid(raise_exception=True)  
                all_serializers.append(serializer)

        return all_serializers

    if data not in [None]:
        serializer = serializer_class(data=data, many=many)
        serializer.is_valid(raise_exception=True)

        print(serializer.validated_data)

    return serializer.validated_data if serializer else data


class NestedDataSerializer(serializers.Serializer):
   
    def __init__(self, *args, **kwargs):
       
        self.createValidationFunctions(self.Meta.nestedSerializer)

        super().__init__(*args, **kwargs)

    def createValidationFunctions(self, dic):
        for key, value in dic.items():
            # print(key)
            # print("THERE")
            many = value['many'] if 'many' in value else False

            the_name = 'validate_' + key

            setattr(self, the_name,
                    (
                        lambda many, serializer_class: lambda x: validate_json
                        (self,
                         x,
                         serializer_class=serializer_class,
                         many=many,
                         ))
                    (many, value['serializer_class'])
                    )

    def to_representation(self, instance):        
        representation = super().to_representation(instance)
        try:
            instance.refresh_from_db()
        except AttributeError:
            pass
        for k, v in self.Meta.nestedSerializer.items():
            print(k, v)
            try:             
                obj = getattr(instance, k)
            except AttributeError:
                try:
                    obj = instance[k]
                except BaseException:

                    obj = None

            many = v['many'] if 'many' in v else False
            try:
                obj = obj.all()
            except AttributeError:
                pass
            print(obj)
            if obj is not None:
                try:
                    representation[k] = v['serializer_class'](obj, many=many).data
                except BaseException:
                    pass
        return representation

    def pop_helper_data(self, validated_data):
        maps = {}
        print(self.Meta.nestedSerializer.items())
        for key, value in self.Meta.nestedSerializer.items():
            if issubclass(value['serializer_class'], serializers.ModelSerializer):
                if eval("'"+key+"'") in validated_data:
                    maps[key] = {
                        'model': value['serializer_class'].Meta.model,
                        'data': validated_data.pop(eval("'"+key+"'")),
                        'type': value['type'] if 'type' in value else None,
                        'kwargs': value['kwargs'] if 'kwargs' in value else None
                    }
        return maps

    def save_helper_data(self, maps, obj):
        for key, value in maps.items():
            data = value['data']
            if data:
                if value['type']:
                    kwargs = {value['kwargs']: obj}
                else:
                    kwargs = {'content_object': obj}
               
                for serializer in data:
                    serializer.save(**kwargs)

    class Meta:
        abstract = True
