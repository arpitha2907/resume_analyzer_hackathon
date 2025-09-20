# parser.py
import docx2txt
import fitz  # PyMuPDF

def extract_text(file_path: str, file_type: str) -> str:
    if file_type == "application/pdf":
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(file_path)
    else:
        return "Unsupported file format."
