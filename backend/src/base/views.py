from src.base.utils import send_to_API
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from src.base.models import Setting
from src.base.serializers import RecognizeSerializer, SettingSerializer

MIME_TYPES = {
    'pdf': 'application/pdf',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'xls': 'application/vnd.ms-excel',
}

class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer

    @action(detail=False, methods=['post'])
    def recognize(self, request):
        data = RecognizeSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data = data.validated_data
        settings = SettingSerializer(Setting.objects.all(), many=True).data
        old_name = data['filename']
        file_name = 'New name.xlsx'
        code = '33a37ce4-c6a9-4dad-8424-707abd47c125'
        mime_type = MIME_TYPES[old_name.split('.')[-1]]

        # DO SOME ACTIONS

        send_to_API(data['file'], file_name, code, data['inn'], mime_type)

        return Response(
            {
                'new_name': file_name,
                'code': mime_type,
            }
        )
