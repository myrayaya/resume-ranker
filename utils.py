# import essential libraries

import fitz # PyMuPDF
import spacy
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# loading spacy model
nlp = spacy.load('en_core_web_sm')

# function to extract text from pdf file
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream = pdf_file.read(), filetype = 'pdf') as doc:
        for page in doc:
            text += page.get_text()
    return text

# function to preprocess text
def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return ' '.join(tokens)

# function to compute similarity between job description and resumes
def compute_similarity_scores(job_desc, resumes_texts):
    vectorizer = TfidfVectorizer()
    all_docs = [job_desc] + resumes_texts
    tfidf_matrix = vectorizer.fit_transform(all_docs)
    job_vec = tfidf_matrix[0]
    resume_vecs = tfidf_matrix[1:]
    
    scores = cosine_similarity(resume_vecs, job_vec)
    return scores.flatten() # numpy array of scores

# function to generate report
def generate_report (names, scores):
    df = pd.DataFrame({'Candidate Name' : names, 'Score' : scores})
    df = df.sort_values(by = 'Score', ascending = False)
    csv = df.to_csv(index = False)
    return csv
