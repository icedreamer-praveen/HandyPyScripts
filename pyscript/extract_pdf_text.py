# This code is importing the `PdfReader` class from the `pypdf` module and using it to read a PDF file
# named "pressnote1.pdf". It then determines the number of pages in the PDF and extracts the text from
# the first page using the `extract_text()` method. Finally, it prints the extracted text to the
# console.

 # Importing the PdfReader class from PyPDF2 library
from pypdf import PdfReader

# Creating a PdfReader object by passing the PDF file path
reader = PdfReader("pressnote1.pdf", "rb")
 # Getting the total number of pages in the PDF
number_of_pages = len(reader.pages)
# Accessing the first page of the PDF (index starts from 0)
page = reader.pages[0]
# Extracting the text content from the page
text = page.extract_text()
# Printing the extracted text
print(text)