from src.base.pdf_classificator import analyze_pdf2
from rest_framework.serializers import ValidationError
from src.base.models import Setting
from typing import Tuple

import requests
import json
from src.settings import CREDS, API_URL

from src.base.xls_processing import analyze_xls


def send_to_API(file, name, code, inn, mime_type):
    unrecognised = False
    if not code:
        unrecognised = True
    data = {
        'createRequest': {
            'unrecognised': unrecognised,
            'inn': inn,
        }
    }
    if code:
        data['createRequest']['documentNomenclatureId'] = code
    data['createRequest'] = json.dumps(data['createRequest'])
    headers = {
        'Authorization': f"Basic {CREDS}",
    }
    files = {
        'attachments': (name, file, mime_type),
    }
    r = requests.post(API_URL, headers=headers, data=data, files=files)
    print(r.content)


def process_doc(file, ext, setting) -> Tuple[str, str, str]:
    try:
        if ext in ("xlsx", 'xls'):
            code, status = analyze_xls(file, setting)  # Кирилл
        elif ext == "pdf":
            code, status = analyze_pdf2(file, setting) # Антон Н.
        else:
            raise ValidationError("Загрузите документ с расширением xls/xlsx или pdf")
    except Exception as ex:
        raise ValidationError(f"Ошибка в процессе обработки {ex}")
    if not code:
        return None, None, status
    setting = Setting.objects.get(code=code)
    recommended_name = setting.name + '.' + setting.type
    return recommended_name, code, status
