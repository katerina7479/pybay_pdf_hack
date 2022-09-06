from PyPDF2 import PdfReader, PdfWriter


def remove_all_text(filename, outputfile):
    reader = PdfReader(filename)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)
    
    # Remove the text
    writer.remove_text()

    # Save the new PDF to a file
    with open(outputfile, "wb") as fp:
        writer.write(fp)


if __name__ == "__main__":
    import subprocess
    subprocess.call(['open', 'sample_pdfs/Pirate Ipsum with Picture.pdf'])
    input("Press any key to continue")
    
    remove_all_text("sample_pdfs/Pirate Ipsum with Picture.pdf", "processed_pdfs/No Text.pdf")
    subprocess.call(['open', 'processed_pdfs/No Text.pdf'])
