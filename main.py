# main.py
from fastapi import FastAPI, UploadFile, File, Form
import shutil
from parser import extract_text
from scorer import hard_match_scorer  # <-- Import your new scorer function

app = FastAPI()

@app.post("/evaluate/")
async def evaluate_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    # Save the uploaded file temporarily
    temp_file_path = f"temp_{resume_file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(resume_file.file, buffer)

    # Use your parser to read the text
    resume_text = extract_text(
        file_path=temp_file_path,
        file_type=resume_file.content_type
    )

    # Use your new scorer to get the result
    result = hard_match_scorer(resume_text, job_description) # <-- Call the scorer

    return result # <-- Return the entire result from the scorer