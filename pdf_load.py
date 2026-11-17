import io

import re

from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.high_level import extract_pages

PDF = "C:/Users/Данил/rag-progect/Трудовой кодекс Российской Федерации от 30.12.2001 N 197-ФЗ.pdf"

with open(PDF, "rb") as file:
    PAGES = sum(1 for _ in PDFPage.get_pages(file))

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
    pages_text = []
    for index, page in enumerate(pdf_text_converter(pdf_path, pages)):
        try:
            if index == 0:
                text = remove_header_first_page(page)
            else:
                text = remove_header(page)
            pages_text.append(text.rstrip())
        except ValueError as e:
            print(e, index + 1)
    return "".join(pages_text)

print(f"Количество страниц в документе: {PAGES}")
print(extract_text(PDF, PAGES))