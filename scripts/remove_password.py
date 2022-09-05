from PyPDF2 import PdfReader, PdfWriter



def remove_password(filename, outputfile, password):
    reader = PdfReader(filename)
    writer = PdfWriter()

    if reader.is_encrypted:
        reader.decrypt(password)

    # Add all pages to the writer
    for page in reader.pages:
        writer.add_page(page)

    # Save the new PDF to a file
    with open(outputfile, "wb") as f:
        writer.write(f)


if __name__ == '__main__':
    remove_password('sample_pdfs/password_protected.pdf', 'processed_pdfs/removed_password.pdf', 'my-secret-password')
