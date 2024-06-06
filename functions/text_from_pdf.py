"""
This module reads the PDF and returns the text
"""
from pypdf import PdfReader


def pdf_to_text(pdf, page_list):
    """
    This function takes a PDF file and returns a text of the pdf as string
    """
    corpus = ''  # Store the text of the pdf

    reader = PdfReader(pdf)

    # If the user returns inputs 0 the program will extract text from all pages
    if len(page_list) == 0:
        page_list = [int(page_num) for page_num in range(reader.get_num_pages())]
    else:
        page_list = [int(page_num) for page_num in page_list.split(',')]

    for num in page_list:
        page = reader.pages[num]
        corpus += page.extract_text()

    return corpus
