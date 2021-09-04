import os
from typing import Tuple

from src.base.utils import send_to_API
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from src.base.models import Setting
from src.base.serializers import RecognizeSerializer, SettingSerializer

from backend.src.base.xls_processing import analyze_xls

MIME_TYPES = {
    'pdf': 'application/pdf',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'xls': 'application/vnd.ms-excel',
}


def process_doc(file, ext, setting) -> Tuple[str, str, str]:
    try:
        if ext in ("xlsx", 'xls'):
            code = analyze_xls(file, setting)  # Кирилл
        elif ext == "pdf":
            code = '1'
            # code = analyze_pdf(filename) # Антон Н.
        else:
            return "None", "None", "Загрузите документ с расширением xls/xlsx или pdf"
    except Exception as ex:
        return "None", "None", f"Ошибка в процессе обработки {ex}"
    # recommended_name = get_recommended_name(filename, type)
    recommended_name = ''
    return recommended_name, code, ''


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
        ext = old_name.split('.')[-1]
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
