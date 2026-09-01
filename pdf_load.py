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


#

def remove_header(page_text):
    re_colontitul = r'\S\w+(?: \w+){3}\S \w{2} \d{2}\.\d{2}\.\d{4} \w \d{3}-\w{2} \(\w{3}\. \w{2} \d{2}\.\d{2}\.\d{4}, \w \w{3}\. \w{2} \d{2}\.\d{2}\.\d{4}\)(?: \w+){5}: \d{2}\.\d{2}\.\d{4}\s+(\w+ ){4}www\.\w+\.ru \w+ \d+ \w{2} \d{3} \d'
    text_wc = re.sub(re_colontitul, "", page_text)
    return text_wc

def remove_header_first_page(page_text):
    re_colontitul_first_page = r'(?: \w+){3}\s+www\.\w+\.ru\s+w+ \w+: d{2}\.\d{2}\.\d{4}'
    text_wc = re.sub(re_colontitul_first_page, "", page_text)
    return text_wc

def extract_text(pdf_path, pages):
    for index, page in enumerate(pdf_text_converter(pdf_path, pages)):
        print(index)
        if index == 0:
            text = remove_header_first_page(page)
            print(text)
        else:
            text = remove_header(page)
            print(text)


extract_text(pdf, 5)