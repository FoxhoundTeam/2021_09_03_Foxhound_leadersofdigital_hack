import requests
import json
from src.settings import CREDS, API_URL


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
