from PyPDF2 import PageObject, PdfReader


def read_text(filename):
    reader = PdfReader(filename)

    word_set = set()
    for page in reader.pages:
        text = page.extract_text()
        print(text)
        text = text.replace(".", " ").replace('\n', " ")
        words = text.split(' ')
        for word in words:
        	word_set.add(word.lower())

    print(sorted(list(word_set)))


if __name__ == "__main__":
    import subprocess
    subprocess.call(['open', 'sample_pdfs/Pirate Ipsum.pdf'])
    
    read_text("sample_pdfs/Pirate Ipsum.pdf")
