# frontend.py
import streamlit as st
import requests
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)

# --- Custom CSS for Styling ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# You can create a style.css file or just inject the string
# For simplicity, we'll inject the string
css_string = """
/* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* General Styles */
body {
    font-family: 'Poppins', sans-serif;
}

/* Card Style for Results */
.card {
    background-color: #172A45;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #4F8BF9;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    transition: 0.3s;
    margin-bottom: 20px;
    animation: fadeIn 0.5s ease-in-out;
}

/* Animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Metric Label Style */
[data-testid="stMetricLabel"] {
    font-size: 18px;
    font-weight: 500;
}
"""
st.markdown(f"<style>{css_string}</style>", unsafe_allow_html=True)


# --- Helper Function to Display Results ---
def display_results(result: dict):
    st.header("Analysis Report")
    
    score = result.get('score', 0)
    
    # --- Score Metric in a Card ---
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎯 Overall Match Score")
        if score >= 75:
            st.metric(label="Verdict", value=f"{score}%", delta="Excellent Candidate")
        elif score >= 50:
            st.metric(label="Verdict", value=f"{score}%", delta="Potential Candidate")
        else:
            st.metric(label="Verdict", value=f"{score}%", delta="Needs Improvement", delta_color="inverse")
        st.progress(int(score))
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Keyword Analysis in Columns within a Card ---
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔑 Keyword Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.success("✅ Matched Keywords")
            matched = result.get('matched_keywords', [])
            if matched:
                st.markdown(" ".join([f"`{kw}`" for kw in matched]))
            else:
                st.markdown("No keywords matched.")
        
        with col2:
            st.info("📄 Job Description Keywords")
            jd_keywords = result.get('total_keywords_checked', [])
            if jd_keywords:
                st.markdown(" ".join([f"`{kw}`" for kw in jd_keywords]))
        st.markdown('</div>', unsafe_allow_html=True)

# --- Main App Interface ---
with st.sidebar:
    st.title("👨‍💻 AI Resume Analyzer")
    st.image("https://www.innomatics.in/wp-content/uploads/2022/09/Innomatics-Logo1.png", width=250)
    st.header("Upload Your Details")
    
    job_description = st.text_area("Paste the Job Description Here:", height=200, placeholder="e.g., Python, Django, NLP")
    uploaded_file = st.file_uploader("Upload Your Resume (PDF or DOCX)", type=["pdf", "docx"])
    
    evaluate_button = st.button("Analyze Resume ✨", type="primary", use_container_width=True)

st.title("Welcome to the AI-Powered Resume Analyzer")
st.markdown("### Get instant feedback on how well your resume matches a job description.")

if evaluate_button:
    if uploaded_file is not None and job_description:
        # Show a more engaging spinner
        with st.spinner('Reading documents...'):
            time.sleep(1)
        with st.spinner('Comparing keywords...'):
            time.sleep(1)
        with st.spinner('Finalizing report...'):
            # The actual API call
            files = {'resume_file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            payload = {'job_description': job_description}
            response = requests.post("http://127.0.0.1:8000/evaluate/", files=files, data=payload)
            if response.status_code == 200:
                result = response.json()
                st.success("Analysis Complete! Here is your report.")
                display_results(result)
            else:
                st.error("There was an error with the server.")
    else:
        st.warning("Please upload a resume and provide a job description in the sidebar.")
else:
    st.info("Fill in your details on the left and click 'Analyze Resume' to start.")