
#!/usr/bin/python3
 
import textract # https://textract.readthedocs.io/en/latest/installation.html

import fitz
from PIL import Image

import pytesseract
import sys, os, io, tempfile, re
from io import BytesIO
from pdf2image import convert_from_path

def analyze_pdf2(streamfile: BytesIO, settings) -> str:
    '''
    Функция извлекает текст как из PDF-файла, так и из сканов,
    содержащихся в файле, и определяет класс документа

    arguments:

        streamfile: BytesIO

        settings: пример [{"name": "Name", "code":"code", "criterias": [{"type":"r", "text": "^regexp$"}, {"type":"s", "text": "text"}]}]

    ВНИМАНИЕ: функция кидает исключения, на основе которых нужно выдавать ответы серверу
    
    textract: https://textract.readthedocs.io/en/latest/installation.html

    fitz: https://www.geeksforgeeks.org/how-to-extract-images-from-pdf-in-python/
    
    pytesseract: https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/

    '''
    result_text = ""

    # сохранение содержимого файла из BytesIO во временный файл, т.к. обработчики pdf работают только с файлами
    temp_file = tempfile.NamedTemporaryFile(delete=True,suffix=".pdf")
    streamfile.seek(0)
    temp_file.write(streamfile.read())

    if __name__ == "__main__":  # диагностическая печать названия временного файла для отладки
        print("temp_file.name = ", temp_file.name)
    
    # извлечение текста, хранящегося в pdf
    text_from_pdf = textract.process(temp_file.name)
    result_text += text_from_pdf.decode("utf-8").lower()

    # попытка классифицировать документ по накопленному тексту
    code = regexp_classifier(result_text, settings)
    if code is not None:
        return code

    # открытие pdf для извлечения изображений и их распознавания
    pdf_file = fitz.open(temp_file.name)

    file_counter = 0 # счётчик извлечённых изображений

    # цикл по страницам pdf
    for page_index in range(min(len(pdf_file), 4)):
        
        page = pdf_file[page_index]
        if __name__ == "__main__": # диагностический вывод сводки по страницам для отладки
            image_list = page.getImageList()
            if image_list:
                print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
            else:
                print("[!] No images found on page", page_index)

        for image_index, img in enumerate(page.getImageList(), start=1):

            # get the XREF of the image
            xref = img[0]
            
            # extract the image bytes
            base_image = pdf_file.extractImage(xref)
            image_bytes = base_image["image"]

            buffer = BytesIO()
            buffer.write(base_image["image"])
            buffer.seek(0)
            pil_image = Image.open(buffer)

            if __name__ == "__main__": # диагностическая запись извлечённых изображений для отладки
                fl = open("img_" + str(file_counter) + "." + base_image["ext"], "wb+")
                fl.write(base_image["image"])
                fl.close()
                file_counter += 1
            
            try:
                pytesseract_str = pytesseract.image_to_string(pil_image, lang="rus")
                result_text += pytesseract_str.lower()
                if __name__ == "__main__": # диагностическая печать для отладки
                    print("pytesseract returns: ", pytesseract_str)
                code = regexp_classifier(result_text, settings)
                if code is not None:
                    return code
            except Exception as e:
                mes = "Не удалось обработать изображение" + \
                    ", страница " + str(image_index) +\
                    ", расширение " + str(base_image["ext"]) + \
                    ", размер ", str(base_image["width"]) + "x" + str(base_image["height"])
                if __name__ == "__main__":
                    print(mes)
                else:
                    return None, mes

    result_text = result_text.lower()
    code, status = regexp_classifier(result_text, settings)

    # matching_table = [
    #     ["555ced1c-c169-4d61-9a82-348801494581", ["положен", "совет", "директоров"], ""], # Учредительные и иные внутренние документы
    #     ["33a37ce4-c6a9-4dad-8424-707abd47c125", ["устав", "обществ"], ""], # Учредительные и иные внутренние документы
    #     ["4f501f4a-c665-4cc8-9715-6ed26e7819f2", ["0710001","актив","оборотн", "бухгалтерск","баланс"]],# Бухгалтерская отчетность_форма 1
    #     ["cabd193c-f9a9-4a9c-a4ae-80f0347adf40", ["0710002","выручк", "прибыл", "доход", "расход"]],# Бухгалтерская отчетность_форма 2
    #     ["2e321818-4571-43ae-9e08-2ade54b83e14", []],# Бухгалтерская отчетность_форма 1 _промежуточная
    #     ["3b4f4647-f755-4100-bd63-059627107919", []],# Бухгалтерская отчетность_форма 2 _промежуточная
    #     ["16f35ccc-b90f-4731-8178-11f3e0e3ca20", ["аудиторск", "заключени", "бухгалтерск", "отчетност"]],# Аудиторское заключение
    #     ["a397c2cf-c5ad-4560-bc65-db4f79840f82", []],# Описание_деятельности_ГК
    #     ["3af37c7f-d8b1-46de-98cc-683b0ffb3513", []],# Решение_назначение ЕИО
    # ]
    # classification_scores = [0 for _ in matching_table]
    # for i in range(len(matching_table)):
    #     for phrase in matching_table[i][1]:
    #         if phrase in result_text:
    #             classification_scores[i] += 1.0 / len(matching_table[i][1])
    # maxval = max(classification_scores)
    # index_max = classification_scores.index(maxval)
    # code = matching_table[index_max][0]

    temp_file.close()
    return code, status

def regexp_classifier(doc_text : str, settings) -> str:
    '''
    Функция классифицирует извлечённый текст с помощью сопоставления
    по регулярным выражениям

    Возвращает код документа или None

    '''
    for criterias_type in settings:
        for criterias in criterias_type['criterias']:
            if criterias['type'] == 'r':
                match = re.search(criterias['text'], doc_text)
                if __name__ == "__main__":
                    print("match = ", match)
                if match:
                    return criterias_type['code'], 'OK'
            elif criterias['type'] == 's':
                if criterias['text'] in doc_text:
                    return criterias_type['code'], 'OK'
            else:
                return None, 'Не подходит под текущие критерии'
    return None, 'Не подходит под текущие критерии'

if __name__ == "__main__":
    print("*** analyze_pdf2(text):")
    filename = 'Устав НКХП.pdf'
    tmp_file = open(filename, 'rb')
    streamfile = BytesIO(tmp_file.read())
    tmp_file.close()

    test_settings = [{
        "name": "xxx",
        "code":"555ced1c-c169-4d61-9a82-348801494581",
        "criterias": [
            {"type":"r",
            "text": r"положен\w*\s*совет\w*\s*директоров"},
            # {"type":"s",
            # "text": "text"}
            ]
        },     
        {
        "name": "xxx",
        "code":"33a37ce4-c6a9-4dad-8424-707abd47c125",
        "criterias": [
            {"type":"r",
            "text": r"устав\s*\w*\s*\w*\s*обществ"},
            # {"type":"s",
            # "text": "text"}
            ]
        },
                {
        "name": "xxx",
        "code":"4f501f4a-c665-4cc8-9715-6ed26e7819f2",
        "criterias": [
            {"type":"r",
            "text": r"0710001"},
            # {"type":"s",
            # "text": "text"}
            ]
        },
        {
        "name": "xxx",
        "code":"cabd193c-f9a9-4a9c-a4ae-80f0347adf40",
        "criterias": [
            {"type":"r",
            "text": r"0710002"},
            # {"type":"s",
            # "text": "text"}
            ]
        },
        {
        "name": "xxx",
        "code":"16f35ccc-b90f-4731-8178-11f3e0e3ca20",
        "criterias": [
            {"type":"r",
            "text": r"аудиторск\w*\s*заключени\w*"},
            # {"type":"s",
            # "text": "text"}
            ]
        },        
        ]

    ret_val = analyze_pdf2(streamfile, test_settings)
    print(ret_val)

    # print("*** analyze_pdf1(text):")
    # analyze_pdf1('example_text.pdf')
    # print("*** analyze_pdf1(scan):")
    # analyze_pdf1('example_scan.pdf')
