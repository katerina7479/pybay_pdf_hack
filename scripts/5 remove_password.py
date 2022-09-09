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
    import subprocess
    subprocess.call(['open', 'sample_pdfs/password_protected.pdf'])

    input("Press any key to continue password: ahoy")

    remove_password('sample_pdfs/password_protected.pdf', 'processed_pdfs/removed_password.pdf', 'ahoy')
    subprocess.call(['open', 'processed_pdfs/removed_password.pdf'])
