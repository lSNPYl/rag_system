import io

import re

from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager

pdf = "C:/Users/Данил/rag-progect/Трудовой кодекс Российской Федерации от 30.12.2001 N 197-ФЗ.pdf"

def pdf_text_converter(pdf_path, pages):
    with open(pdf_path, "rb") as file:
        resource_manager = PDFResourceManager()
        io_string = io.StringIO()
        converter = TextConverter(resource_manager, io_string)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        for index, page in enumerate(PDFPage.get_pages(file)):
            if index < pages:
                page_interpreter.process_page(page)
                text = io_string.getvalue()
                io_string.seek(0)
                io_string.truncate(0)
                yield text


        converter.close()
        io_string.close()




def remove_header(page_text):
    re_colontitul = r'.*? КонсультантПлюс.*?www\.consultant\.ru.*?Страница \d*? из \d* \d+'
    text_wc = re.sub(re_colontitul, "", page_text)
    if page_text != text_wc:
        return text_wc
    else:
        raise ValueError("Колонтитул не найден на странице: ")

def remove_header_first_page(page_text):
    re_colontitul_first_page = r'Документ.*?КонсультантПлюс.*?www\.consultant\.ru.*?Дата сохранения:.+'
    text_wc = re.sub(re_colontitul_first_page, "", page_text)
    if page_text != text_wc:
        return text_wc
    else:
        raise ValueError("Колонтитул не найден на странице: ")

def extract_text(pdf_path, pages):
    for index, page in enumerate(pdf_text_converter(pdf_path, pages)):
        if index == 0:
            try:
                text = remove_header_first_page(page)
                print(text)
            except ValueError as e:
                print(e, index + 1)
        else:
            try:
                text = remove_header(page)
                print(text)
            except ValueError as e:
                print(e, index + 1)


extract_text(pdf, 30)