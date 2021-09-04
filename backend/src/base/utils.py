from src.base.models import Setting
from typing import Tuple

import requests
import json
from src.settings import CREDS, API_URL

from src.base.xls_processing import analyze_xls


def send_to_API(file, name, code, inn, mime_type):
    headers = {
        'Authorization': f"Basic {CREDS}",
    }
    data = {
        'createRequest': json.dumps(
            {
                'documentNomenclatureId': code,
                'unrecognised': False,
                'inn': inn,
            }
        )
    }
    files = {
        'attachments': (name, file, mime_type),
    }
    r = requests.post(API_URL, headers=headers, data=data, files=files)
    print(r.content)


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
    setting = Setting.objects.get(code=code)
    recommended_name = setting.name + '.' + setting.type
    return recommended_name, code, ''
