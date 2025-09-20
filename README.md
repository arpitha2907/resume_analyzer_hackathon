# resume_analyzer_hackathon
Problem Statement: Automated Resume relevance Check System
The system will:
Accept resumes (PDF/DOCX) uploaded by students.
Accept job descriptions uploaded by the placement team.
Use text extraction + embeddings to compare resume content with job descriptions.
Run hybrid scoring:
Hard match (keywords, skills, education)
Soft match (semantic fit via embeddings + LLM reasoning)
Output a Relevance Score, Missing Elements, and Verdict.
Store results for the placement team in a searchable web application dashboard.
