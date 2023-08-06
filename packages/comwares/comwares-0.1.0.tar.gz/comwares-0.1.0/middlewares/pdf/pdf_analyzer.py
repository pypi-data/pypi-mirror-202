import datetime
import pdfplumber
import requests
import pandas as pd
from io import BytesIO


def process_pdf(file, keyword='本次发行配售结果如下'):
    with pdfplumber.open(file) as pdf:
        text = ''
        tables = []
        for idx, page in enumerate(pdf.pages):
            text += page.extract_text() + '\n'
            table = page.extract_table()
            if table:
                clean_headers = []
                for field_name in table[0]:
                    if isinstance(field_name, str):
                        clean_headers.append(field_name.replace('\n', ''))
                    else:
                        clean_headers.append(field_name)
                table[0] = clean_headers    # clean header
                if tables:
                    last_table = tables[-1]
                    last_table_columns = len(last_table[0])
                    cur_table_columns = len(table[0])
                    if cur_table_columns == last_table_columns:
                        tables[-1] += table
                    else:
                        tables.append(table)
                else:
                    tables.append(table)
    res = {
        'text': text,
        'tables': tables
    }
    return res


def get_pdf_from_url(url):
    print(f"[{datetime.datetime.now()}] Downloading from: {url}")
    r = requests.get(url=url)
    print(f"[{datetime.datetime.now()}] Analyzing info in pdf...")
    res = process_pdf(BytesIO(r.content))
    return res


if __name__ == '__main__':

    URL = 'https://pdf.dfcfw.com/pdf/H2_AN202012221442705664_1.pdf'
    result = get_pdf_from_url(URL)
    print(result)

