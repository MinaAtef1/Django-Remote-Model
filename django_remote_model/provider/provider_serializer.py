from rest_framework import serializers



class dynamic_model_dict_serializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=255)
    null = serializers.BooleanField()
    blank = serializers.BooleanField()
    default = serializers.CharField(max_length=255)
    editable = serializers.BooleanField()
    choices = serializers.ListField(max_length=255)
    help_text = serializers.CharField(max_length=255)
    verbose_name = serializers.CharField(max_length=255)
    primary_key = serializers.BooleanField()
    max_length = serializers.IntegerField()

    def to_representation(self, obj):
        ret = super(dynamic_model_dict_serializer, self).to_representation(obj)

        # remove 'url' field if mobile request
        if ret['type'] == 'FileField':
            ret.pop('primary_key')

        return ret 


def provider_model_generator(model_class):
    class serializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = '__all__'

    return serializer