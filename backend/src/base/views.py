from src.base.utils import send_to_API
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from src.base.models import Setting
from src.base.serializers import RecognizeSerializer, SettingSerializer

from backend.src.base.utils import process_doc

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
        old_name = data['filename']
        ext = old_name.split('.')[-1]
        settings = SettingSerializer(Setting.objects.filter(type=ext), many=True).data
        file_name, code, error_str = process_doc(
            file=data['file'],
            ext=ext,
            setting=settings,
        )
        mime_type = MIME_TYPES[ext]

        send_to_API(data['file'], file_name, code, data['inn'], mime_type)

        return Response(
            {
                'new_name': file_name,
                'code': mime_type,
                'error_str': error_str,
            }
        )
