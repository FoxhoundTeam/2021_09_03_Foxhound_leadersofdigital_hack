
#!/usr/bin/python3
 
import textract # https://textract.readthedocs.io/en/latest/installation.html

import fitz
from PIL import Image

import pytesseract
import sys, os, io
from io import BytesIO
from pdf2image import convert_from_path

def analyze_pdf1(filename):
    '''
    Извлечение текста и классификация PDF на основе пакета textract
    https://textract.readthedocs.io/en/latest/installation.html
    '''
    
    text_from_pdf = textract.process(filename)
    text_from_pdf = text_from_pdf.decode("utf-8")
    #print(text_from_pdf)

    code = "xxx-xxx-xxx-xxx"

    #TODO матчинг
    
    return code

def analyze_pdf2(filename):
    '''
    Извлечение текста и классификация PDF на основе OCR

    ВНИМАНИЕ: функция кидает исключения, на основе которых нужно выдавать ответы серверу

    https://www.geeksforgeeks.org/how-to-extract-images-from-pdf-in-python/
    https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/

    '''
    result_text = ""
            
    text_from_pdf = textract.process(filename)
    result_text += text_from_pdf.decode("utf-8")

    pdf_file = fitz.open(filename)

    file_counter = 0

    # iterate over PDF pages
    for page_index in range(min(len(pdf_file), 4)):
        
        # get the page itself
        page = pdf_file[page_index]
        image_list = page.getImageList()
        
        # printing number of images found in this page
        # if image_list:
        #     print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        # else:
        #     print("[!] No images found on page", page_index)

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

            if __name__ == "__main__":
                fl = open("img_" + str(file_counter) + "." + base_image["ext"], "wb+")
                fl.write(base_image["image"])
                fl.close()
                file_counter += 1
            
            try:
                pytesseract_str = pytesseract.image_to_string(pil_image, lang="rus")
                result_text += pytesseract_str
                if __name__ == "__main__":
                    print("pytesseract returns: ", pytesseract_str)
            except Exception as e:
                if __name__ == "__main__":
                    print("Не удалось обработать изображение, файл ", filename,
                    ", страница ", image_index,
                    ", расширение ", base_image["ext"],
                    ", размер ", str(base_image["width"]) + "x" + str(base_image["height"]))

    #TODO матчинг code =
    matching_table = [
        ["555ced1c-c169-4d61-9a82-348801494581", ["положен", "совет", "директоров"], ""], # Учредительные и иные внутренние документы
        ["33a37ce4-c6a9-4dad-8424-707abd47c125", ["устав", "обществ"], ""], # Учредительные и иные внутренние документы
        ["4f501f4a-c665-4cc8-9715-6ed26e7819f2", ["0710001","актив","оборотн", "бухгалтерск","баланс"]],# Бухгалтерская отчетность_форма 1
        ["cabd193c-f9a9-4a9c-a4ae-80f0347adf40", ["0710002","выручк", "прибыл", "доход", "расход"]],# Бухгалтерская отчетность_форма 2
        ["2e321818-4571-43ae-9e08-2ade54b83e14", []],# Бухгалтерская отчетность_форма 1 _промежуточная
        ["3b4f4647-f755-4100-bd63-059627107919", []],# Бухгалтерская отчетность_форма 2 _промежуточная
        ["16f35ccc-b90f-4731-8178-11f3e0e3ca20", ["аудиторск", "заключени", "бухгалтерск", "отчетност"]],# Аудиторское заключение
        ["a397c2cf-c5ad-4560-bc65-db4f79840f82", []],# Описание_деятельности_ГК
        ["3af37c7f-d8b1-46de-98cc-683b0ffb3513", []],# Решение_назначение ЕИО
    ]

    result_text = result_text.lower()
    classification_scores = [0 for _ in matching_table]
    for i in range(len(matching_table)):
        for phrase in matching_table[i][1]:
            if phrase in result_text:
                classification_scores[i] += 1.0 / len(matching_table[i][1])
    maxval = max(classification_scores)
    index_max = classification_scores.index(maxval)

    
    code = matching_table[index_max][0]
    return code

if __name__ == "__main__":
    print("*** analyze_pdf2(text):")
    ret_val = analyze_pdf2('example3.pdf')
    print(ret_val)

    # print("*** analyze_pdf1(text):")
    # analyze_pdf1('example_text.pdf')
    # print("*** analyze_pdf1(scan):")
    # analyze_pdf1('example_scan.pdf')
