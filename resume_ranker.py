
import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#function to extract text from PDF
def extract_text_from_pdf(file):
    pdf=PdfReader(file)
    text=""
    for page in pdf.pages:
        extracted_text=page.extract_text()
        if extracted_text:
            text+=extracted_text + "\n"
    # Debug: Check if text was extracted
    if not text.strip():
        st.warning(f"⚠️ Could not extract text from {file.name}. It may be an image-based PDF.")
    return text

#function to rank resumes
def rank_resumes(job_description,resumes):
    #combine job description with resumes
    documents=[job_description]+resumes
    vectorizer=TfidfVectorizer().fit_transform(documents)
    vectors=vectorizer.toarray()

    #calculate cosine similarity
    job_description_vector=vectors[0]
    resume_vectors=vectors[1:]
    cosine_similarities=cosine_similarity([job_description_vector],resume_vectors).flatten()

    return cosine_similarities

#streamlit app
st.title("AI Resume Screening and Ranking System")

#Job description input
st.header("Job Description")
job_description=st.text_area("Enter the job description")

#File uploader
st.header("Upload Resumes")
uploaded_files=st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files and job_description:
    st.header("Ranking Resumes")

    resumes=[]
    for file in uploaded_files:
        text=extract_text_from_pdf(file)
        resumes.append(text)

    #Rank resumes
    scores=rank_resumes(job_description,resumes)

    #Display scores
    results=pd.DataFrame({"Resume": [file.name for file in uploaded_files], "Score" : scores})
    results = results.sort_values(by="Score", ascending=False)  # Sort from highest to lowest
    st.subheader("🏆 Ranked Resumes")
    st.write(results)