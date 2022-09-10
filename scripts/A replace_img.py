from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import *
from PyPDF2.constants import PagesAttributes as PA


class NewPdfWriter(PdfWriter):
    def __init__(self, fileobj=""):
        super().__init__(fileobj)
        self._header = b"%PDF-1.7"

    def get_image_objects(self):
        """
        Remove text from this output.
        """
        pg_dict =self.get_object(self._pages)
        pages = pg_dict[PA.KIDS]
        images = []
        for page in pages:
            page_ref = self.get_object(page)
            
            resources = page_ref['/Resources']
            new_resources = DictionaryObject()
            for key, val in resources.items():
                if key == '/XObject':
                    image_value = list(val.values())[0]
                    image_object =image_value.get_object() 
                    images.append(image_object)
                    val = DictionaryObject()
        return images

    def replace_image(self, image_object):
        """
        Replace image 1 with image 2
        """
        pg_dict =self.get_object(self._pages)
        pages = pg_dict[PA.KIDS]
        for page in pages:
            page_ref =  self.get_object(page)
            
            resources = page_ref['/Resources']
            new_resources = DictionaryObject()
            for key, val in resources.items():
                if key == '/XObject':
                    val_key = list(val.keys())[0]
                    val = DictionaryObject()
                    val.__setitem__(NameObject(val_key), image_object)
                new_resources.__setitem__(NameObject(key), val)
            page_ref.__setitem__(NameObject("/Resources"), new_resources)


def replace_image(filename, filename_two, outputfile):
    reader = PdfReader(filename)
    writer = NewPdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    reader_2 = PdfReader(filename_two)
    writer_2 = NewPdfWriter()
    for page in reader_2.pages:
        writer_2.add_page(page)

    # pull the image from the second pdf
    replacement_images = writer_2.get_image_objects()
    
    writer.replace_image(replacement_images[0])

    # Save the new PDF to a file
    with open(outputfile, "wb") as fp:
        writer.write(fp)


if __name__ == "__main__":
    import subprocess
    subprocess.call(['open', 'sample_pdfs/Pirate with his Pet.pdf'])

    input("Press any key to continue")
    replace_image("sample_pdfs/Pirate with his Pet.pdf", "sample_pdfs/Pirate Pet Pic 2.pdf", "processed_pdfs/Pirate with his Real Pet.pdf")
    
    subprocess.call(['open', 'processed_pdfs/Pirate with his Real Pet.pdf'])

