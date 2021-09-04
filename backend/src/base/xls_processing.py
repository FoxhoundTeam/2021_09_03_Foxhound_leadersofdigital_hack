import math
from typing import Dict

import pandas as pd
import re


def analyze_xls(file, settings) -> str:
    try:
        df = pd.read_excel(file)
        criterias_data = [{"name": "Камаз", "code": "12345",
                           "criterias": [{"type": "r", "text": ""}, {"type": "s", "text": ''}]}]
        phrases = set()
        for column in df:
            for cell in df[column]:
                if cell != math.nan:
                    phrases.add(str(cell))

        for criterias_type in criterias_data:
            global_allow = True
            for critetias in criterias_type['criterias']:
                allow = False
                if critetias['type'] == 'r':
                    for phrase in phrases:
                        try:
                            if not re.fullmatch(critetias['text'], phrase):
                                allow = True
                                break
                        except:
                            raise ValueError(f"Не верный паттерн в условии {criterias_type['name']}")
                else:
                    for phrase in phrases:
                        if phrase == critetias['text']:
                            allow = True
                            break
                if not allow:
                    global_allow = False
                    break

            if global_allow:
                return criterias_type['code']
    except:
        raise RuntimeError(f"Ошибка обработки")
    raise ValueError('Не подходит под текущие критерии')
