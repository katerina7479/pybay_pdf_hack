from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import *
from PyPDF2.constants import PagesAttributes as PA


    # def remove_text(self, ignore_byte_string_object: bool = False) -> None:
    #     """
    #     Remove text from this output.

    #     :param bool ignore_byte_string_object: optional parameter
    #         to ignore ByteString Objects.
    #     """
    #     pg_dict = cast(DictionaryObject, self.get_object(self._pages))
    #     pages = cast(List[IndirectObject], pg_dict[PA.KIDS])
    #     for page in pages:
    #         page_ref = cast(Dict[str, Any], self.get_object(page))
    #         content = page_ref["/Contents"].get_object()
    #         if not isinstance(content, ContentStream):
    #             content = ContentStream(content, page_ref)
    #         for operands, operator in content.operations:
    #             if operator in [b"Tj", b"'"]:
    #                 text = operands[0]
    #                 if not ignore_byte_string_object:
    #                     if isinstance(text, TextStringObject):
    #                         operands[0] = TextStringObject()
    #                 else:
    #                     if isinstance(text, (TextStringObject, ByteStringObject)):
    #                         operands[0] = TextStringObject()
    #             elif operator == b'"':
    #                 text = operands[2]
    #                 if not ignore_byte_string_object:
    #                     if isinstance(text, TextStringObject):
    #                         operands[2] = TextStringObject()
    #                 else:
    #                     if isinstance(text, (TextStringObject, ByteStringObject)):
    #                         operands[2] = TextStringObject()
    #             elif operator == b"TJ":
    #                 for i in range(len(operands[0])):
    #                     if not ignore_byte_string_object:
    #                         if isinstance(operands[0][i], TextStringObject):
    #                             operands[0][i] = TextStringObject()
    #                     else:
    #                         if isinstance(
    #                             operands[0][i], (TextStringObject, ByteStringObject)
    #                         ):
    #                             operands[0][i] = TextStringObject()
    #         page_ref.__setitem__(NameObject("/Contents"), content)




class NewPdfWriter(PdfWriter):
    def __init__(self, fileobj=""):
        super().__init__(fileobj)
        self._header = b"%PDF-1.7"

    def remove_text(self):
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
            for operands, operator in content.operations:
                if operator in [b"Tj", b"'", b'"', b"TJ", b"Td", b"Tf", b"TD"]:
                    pass
                else:
                    new_operations.append((operands, operator))

            content.operations = new_operations
            page_ref.__setitem__(NameObject("/Contents"), content)


def remove_all_text(filename, outputfile):
    reader = PdfReader(filename)
    writer = NewPdfWriter()

    for page in reader.pages:
        writer.add_page(page)
    
    # Remove the text
    writer.remove_text()

    # Save the new PDF to a file
    with open(outputfile, "wb") as fp:
        writer.write(fp)


if __name__ == "__main__":
    remove_all_text("sample_pdfs/Scratch my tummy.pdf", "processed_pdfs/Just Cat in a Box.pdf")