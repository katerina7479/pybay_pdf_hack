from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import *
from PyPDF2.constants import PagesAttributes as PA


class NewPdfWriter(PdfWriter):
    def __init__(self, fileobj=""):
        super().__init__(fileobj)
        self._header = b"%PDF-1.7"

    def remove_red_text(self):
        """
        Remove text from this output.
        """
        pg_dict = cast(DictionaryObject, self.get_object(self._pages))
        pages = cast(List[IndirectObject], pg_dict[PA.KIDS])
        for page in pages:
            page_ref = cast(Dict[str, Any], self.get_object(page))
            content = page_ref["/Contents"].get_object()
            if not isinstance(content, ContentStream):
                content = ContentStream(content, page_ref)

            new_operations = []
            is_red = False
            for operands, operator in content.operations:
                if operator in [b'rg', b"RG"]:
                    r, g, b = operands
                    if r > g and r > b:
                        is_red = True
                    else:
                        is_red = False

                if operator in [b"Tj", b"'", b'"', b"TJ", b"Td", b"Tf", b"TD"] and is_red:
                    pass
                else:
                    new_operations.append((operands, operator))

            content.operations = new_operations
            page_ref.__setitem__(NameObject("/Contents"), content)


    def change_red_to_blue_text(self):
        """
        Change Red to blue Text
        """
        pg_dict = cast(DictionaryObject, self.get_object(self._pages))
        pages = cast(List[IndirectObject], pg_dict[PA.KIDS])
        for page in pages:
            page_ref = cast(Dict[str, Any], self.get_object(page))
            content = page_ref["/Contents"].get_object()
            if not isinstance(content, ContentStream):
                content = ContentStream(content, page_ref)

            new_operations = []
            is_red = False
            for operands, operator in content.operations:
                if operator in [b'rg', b"RG"]:
                    r, g, b = operands
                    if r > g and r > b:
                        operands = [FloatObject(0), FloatObject(0), FloatObject(0.8)]

                new_operations.append((operands, operator))

            content.operations = new_operations
            page_ref.__setitem__(NameObject("/Contents"), content)


def remove_red_text_only(filename, outputfile):
    reader = PdfReader(filename)
    writer = NewPdfWriter()

    for page in reader.pages:
        writer.add_page(page)
    
    # Remove the text
    writer.remove_red_text()

    # Save the new PDF to a file
    with open(outputfile, "wb") as fp:
        writer.write(fp)


def change_color(filename, outputfile):
    reader = PdfReader(filename)
    writer = NewPdfWriter()

    for page in reader.pages:
        writer.add_page(page)
    
    # Remove the text
    writer.change_red_to_blue_text()

    # Save the new PDF to a file
    with open(outputfile, "wb") as fp:
        writer.write(fp)    


if __name__ == "__main__":
    remove_red_text_only("sample_pdfs/Win-win organic growth.pdf", "processed_pdfs/No Red Text Wins.pdf")
    change_color("sample_pdfs/Win-win organic growth.pdf", "processed_pdfs/Red is Blue Wins.pdf")
