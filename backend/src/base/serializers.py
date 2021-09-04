from io import BytesIO
import json
import requests
from rest_framework import serializers
from src.base.models import Setting

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not isinstance(data['criterias'], list):
            data['criterias'] = json.loads(data['criterias'])
        return data

    def to_internal_value(self, data):
        data['criterias'] = json.dumps(data['criterias'])
        return super().to_internal_value(data)

class RecognizeSerializer(serializers.Serializer):
    filename = serializers.CharField()
    url = serializers.URLField(required=False)
    file = serializers.FileField(required=False)
    inn = serializers.CharField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not attrs.get('file'):
            attrs['file'] = BytesIO(requests.get(attrs['url']).content)
        return attrs
