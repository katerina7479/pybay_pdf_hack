from PyPDF2 import PageObject, PdfReader


def read_text(filename):
    reader = PdfReader(filename)
    for page in reader.pages:
    	text = page.extract_text()
    	print(text)


if __name__ == "__main__":
	read_text("sample_pdfs/Cupcake Ipsum.pdf")
