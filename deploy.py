# deploy.py
import streamlit as st
import fitz  # PyMuPDF
import docx2txt
from PIL import Image
import pytesseract
import re
import time

# --- Page Configuration ---
st.set_page_config(page_title="AI Resume Analyzer", page_icon="🤖", layout="wide")

# --- Custom CSS (from your previous version) ---
css_string = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
body { font-family: 'Poppins', sans-serif; }
.card {
    background-color: #172A45;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #4F8BF9;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    margin-bottom: 20px;
    animation: fadeIn 0.5s ease-in-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
[data-testid="stMetricLabel"] { font-size: 18px; font-weight: 500; }
"""
st.markdown(f"<style>{css_string}</style>", unsafe_allow_html=True)

# --- All Helper Functions are now in this file ---

def extract_text(file_obj, file_type: str) -> str:
    """Reads text from an uploaded file object (PDF, DOCX, Image)."""
    text = ""
    try:
        if file_type == "application/pdf":
            doc = fitz.open(stream=file_obj.read(), filetype="pdf")
            for page in doc:
                text += page.get_text()
            if not text.strip(): # Fallback for image-based PDFs
                file_obj.seek(0) # Reset file pointer
                doc = fitz.open(stream=file_obj.read(), filetype="pdf")
                for i, page in enumerate(doc):
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text += pytesseract.image_to_string(img)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = docx2txt.process(file_obj)
        elif file_type in ["image/png", "image/jpeg", "image/jpg"]:
            text = pytesseract.image_to_string(Image.open(file_obj))
    except Exception as e:
        st.error(f"Error processing file: {e}")
    return text

def hard_match_scorer(resume_text: str, jd_text: str) -> dict:
    """Scores the resume based on keyword matching."""
    resume_keywords = {word for word in re.findall(r'\b[a-z0-9+#-]+\b', resume_text.lower()) if len(word) > 1}
    jd_keywords = {skill.strip() for skill in jd_text.lower().split(',') if skill.strip()}
    found_skills = list(jd_keywords.intersection(resume_keywords))
    score = (len(found_skills) / len(jd_keywords)) * 100 if jd_keywords else 0
    return {
        "score": round(score, 2),
        "matched_keywords": found_skills,
        "total_keywords_checked": list(jd_keywords)
    }

def display_results(result: dict):
    """Renders the analysis report UI."""
    st.header("Analysis Report")
    score = result.get('score', 0)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎯 Overall Match Score")
        # ... (rest of your display_results function from frontend.py)
        if score >= 75:
            st.metric(label="Verdict", value=f"{score}%", delta="Excellent Candidate")
        elif score >= 50:
            st.metric(label="Verdict", value=f"{score}%", delta="Potential Candidate")
        else:
            st.metric(label="Verdict", value=f"{score}%", delta="Needs Improvement", delta_color="inverse")
        st.progress(int(score))
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔑 Keyword Analysis")
        # ... (rest of your display_results function from frontend.py)
        col1, col2 = st.columns(2)
        with col1:
            st.success("✅ Matched Keywords")
            matched = result.get('matched_keywords', [])
            st.markdown(" ".join([f"`{kw}`" for kw in matched]) if matched else "No keywords matched.")
        with col2:
            st.info("📄 Job Description Keywords")
            jd_keywords = result.get('total_keywords_checked', [])
            st.markdown(" ".join([f"`{kw}`" for kw in jd_keywords]) if jd_keywords else "No keywords found in JD.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- Main App Interface ---

with st.sidebar:
    st.title("👨‍💻 AI Resume Analyzer")
    st.image("https://www.innomatics.in/wp-content/uploads/2022/09/Innomatics-Logo1.png", width=250)
    st.header("Upload Your Details")
    job_description = st.text_area("Paste JD Keywords (comma-separated):", height=150, placeholder="e.g., Python, Django, NLP")
    uploaded_file = st.file_uploader("Upload Your Resume (PDF, DOCX, PNG, JPG)", type=["pdf", "docx", "png", "jpg", "jpeg"])
    evaluate_button = st.button("Analyze Resume ✨", type="primary", use_container_width=True)

st.title("Welcome to the AI-Powered Resume Analyzer")
st.markdown("### Get instant feedback on how well your resume matches a job description.")

if evaluate_button:
    if uploaded_file is not None and job_description:
        # This is the NEW button logic
        with st.spinner('Analyzing your documents... This can take a moment.'):
            resume_text = extract_text(uploaded_file, uploaded_file.type)
            if resume_text:
                result = hard_match_scorer(resume_text, job_description)
                display_results(result)
            else:
                st.error("Could not read text from the uploaded file. It might be empty, corrupted, or an unsupported format.")
    else:
        st.warning("Please provide a job description and upload a resume in the sidebar.")
else:
    st.info("Fill in your details on the left and click 'Analyze Resume' to start.")