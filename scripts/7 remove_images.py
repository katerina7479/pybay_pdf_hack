from PyPDF2 import PdfReader, PdfWriter


def remove_images(filename, outputfile):
    reader = PdfReader(filename)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)
    
    # Remove the text
    writer.remove_images()

    # Save the new PDF to a file
    with open(outputfile, "wb") as fp:
        writer.write(fp)


if __name__ == "__main__":
    import subprocess

    remove_images("sample_pdfs/Pirate Ipsum with Picture.pdf", "processed_pdfs/No Images.pdf")
    subprocess.call(['open', 'processed_pdfs/No Images.pdf'])
