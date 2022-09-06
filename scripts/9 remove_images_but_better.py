from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import *
from PyPDF2.constants import PagesAttributes as PA


class NewPdfWriter(PdfWriter):
    def __init__(self, fileobj=""):
        super().__init__(fileobj)
        self._header = b"%PDF-1.7"

    def remove_image_objects(self):
        """
        Remove text from this output.
        """
        pg_dict = cast(DictionaryObject, self.get_object(self._pages))
        pages = cast(List[IndirectObject], pg_dict[PA.KIDS])
        for page in pages:
            page_ref = cast(Dict[str, Any], self.get_object(page))
            
            resources = page_ref['/Resources']
            print(resources)
            new_resources = DictionaryObject()
            for key, val in resources.items():
                if key == '/XObject':
                    val = DictionaryObject()
                new_resources.__setitem__(NameObject(key), val)
            page_ref.__setitem__(NameObject("/Resources"), new_resources)


def remove_images(filename, outputfile):
    reader = PdfReader(filename)
    writer = NewPdfWriter()

    for page in reader.pages:
        writer.add_page(page)
    
    # Remove the text
    writer.remove_image_objects()

    # Save the new PDF to a file
    with open(outputfile, "wb") as fp:
        writer.write(fp)


if __name__ == "__main__":
    import subprocess

    remove_images("sample_pdfs/Pirate Ipsum with Picture.pdf", "processed_pdfs/Just Pirate Ipsum.pdf")
    subprocess.call(['open', 'processed_pdfs/Just Pirate Ipsum.pdf'])