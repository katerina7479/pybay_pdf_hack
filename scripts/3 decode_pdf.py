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
    import subprocess
    subprocess.call(['open', 'sample_pdfs/Skull Stamp.pdf'])

    decode("sample_pdfs/Skull Stamp.pdf", "processed_pdfs/Decoded Skull.pdf")
    subprocess.call(['open', 'processed_pdfs/Decoded Skull.pdf'])
