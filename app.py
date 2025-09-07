from flask import Flask, request, render_template, send_file, jsonify
from utils import extract_text_from_pdf, preprocess_text, compute_similarity_scores, generate_report
import io
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok = True)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        job_desc = request.form['job_desc']
        files = request.files.getlist('resumes')
        
        
        resume_texts = []
        names = []
        for file in files:
            name = file.filename
            text = extract_text_from_pdf(file)
            processed = preprocess_text(text)
            if processed.strip():            # Only keep non-empty resumes
                names.append(name)
                resume_texts.append(processed)

        print("Names:", names)
        print("Resume_texts: ", resume_texts)
                
        job_desc_processed = preprocess_text(job_desc)
        print("Job Description Processed: ", job_desc_processed)
        
        if not resume_texts:
            # No valid resumes extracted, handle this gracefully in your app
            return render_template('index.html', show_results=False, error="No valid resume text found in uploaded files.")
        
        scores = compute_similarity_scores(job_desc_processed, resume_texts)
        print("Scores: ", scores)
        
        if len(names) != len(scores):
            # Defensive: This should never happen, but if it does, handle the error
            return render_template('index.html', show_results=False, error=f"Resume/app error: {len(names)} names, {len(scores)} scores.")
        
        report = generate_report(names, scores)
        
        # saving the report to a file
        report_file = os.path.join(UPLOAD_FOLDER, 'HR_report.csv')
        with open(report_file, 'w') as f:
            f.write(report)
        
        ranked = sorted(zip(names, scores), key = lambda x: -x[1])
        return render_template('index.html',ranked = ranked, show_results = True, error = None)
        print("Ranked: ", ranked)
        print("Type of ranked items: ", [type(item) for item in ranked])    
    return render_template('index.html', show_results = False)

@app.route('/download')
def download():
    report_file = os.path.join(UPLOAD_FOLDER, 'HR_report.csv')
    return send_file(report_file, as_attachment = True)

if __name__ == '__main__':
    app.run(debug = True)