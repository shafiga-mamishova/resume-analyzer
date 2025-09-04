# TODO: User uploads PDF. Parse PDF as plain text

import pypdf

def parse(file):
    reader=pypdf.PdfReader(file)
    text=""
    for page in reader.pages:
        text += page.extract_text()
    print(text)
    return text