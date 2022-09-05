from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO



def decode(filename, outputfile):
    reader = PdfReader(filename)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Save the new PDF to a file
    with open(outputfile, "wb") as fp:
        writer.write(fp)


if __name__ == "__main__":
    decode("example_pdfs/Pirate with his Pet.pdf", "example_pdfs/Pirate with his Pet 2.pdf")
