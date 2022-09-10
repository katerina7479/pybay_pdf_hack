from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import *
from PyPDF2.constants import PagesAttributes as PA


class NewPdfWriter(PdfWriter):
    def __init__(self, fileobj=""):
        super().__init__(fileobj)
        self._header = b"%PDF-1.7"


    def remove_text(self):
        """
        Remove text from this output.
        """
        pg_dict =  self.get_object(self._pages)
        pages = pg_dict[PA.KIDS]
        for page in pages:
            page_ref =  self.get_object(page)

            content = page_ref["/Contents"].get_object()
            if not isinstance(content, ContentStream):
                content = ContentStream(content, page_ref)
            
            new_operations = []
            for operands, operator in content.operations:
                if operator in [b"Tj", b"'", b'"', b"TJ", b"Td", b"Tf", b"TD"]:
                    pass
                else:
                    new_operations.append((operands, operator))

            content.operations = new_operations
            page_ref.__setitem__(NameObject("/Contents"), content)


    def remove_image_objects(self):
        """
        Remove text from this output.
        """
        pg_dict = self.get_object(self._pages)
        pages = pg_dict[PA.KIDS]
        for page in pages:
            page_ref =  self.get_object(page)
            
            resources = page_ref['/Resources']
            new_resources = DictionaryObject()
            for key, val in resources.items():
                if key == '/XObject':
                    val = DictionaryObject()
                new_resources.__setitem__(NameObject(key), val)
            page_ref.__setitem__(NameObject("/Resources"), new_resources)


    def remove_stamp(self):
        pg_dict = self.get_object(self._pages)
        pages =  pg_dict[PA.KIDS]
        for page in pages:
            page_ref = self.get_object(page)
            page_ref.__setitem__(NameObject("/Annots"), NullObject())



def remove_text_and_images(filename, outputfile):
    reader = PdfReader(filename)
    writer = NewPdfWriter()

    for page in reader.pages:
        writer.add_page(page)
    
    # Remove the images
    writer.remove_text()
    writer.remove_image_objects()

    # Save the new PDF to a file
    with open(outputfile, "wb") as fp:
        writer.write(fp)


def remove_stamp(filename, outputfile):
    reader = PdfReader(filename)
    writer = NewPdfWriter()

    for page in reader.pages:
        writer.add_page(page)
    
    # Remove the stamp
    writer.remove_stamp()

    # Save the new PDF to a file
    with open(outputfile, "wb") as fp:
        writer.write(fp)


if __name__ == "__main__":
    import subprocess
    subprocess.call(['open', 'sample_pdfs/Stamped Pirate.pdf'])
    input("Press any key to continue")

    remove_images("sample_pdfs/Stamped Pirate.pdf", "processed_pdfs/Clean-ish Pirate.pdf")
    subprocess.call(['open', 'processed_pdfs/Clean-ish Pirate.pdf'])
    
    input("Press any key to continue")
    remove_stamp("sample_pdfs/Stamped Pirate.pdf", "processed_pdfs/Actually Clean Pirate.pdf")
    subprocess.call(['open', 'processed_pdfs/Actually Clean Pirate.pdf'])

