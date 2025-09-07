# AI - Powered Resume Ranker

This is a Flask web application that ranks PDF resumes against a job description using NLP techniques (SpaCy, TF-IDF)

## Features

- Upload multiple resume PDFs
- Enter a job description text
- Ranks candidates based on resume-job description similarity
- Download ranking report as CSV

## Setup Instructions

### Prerequisities

- Python 3.8 or newer installed
- Git installed (optional)

### Clone Repository

```
git clone https://github.com/myrayaya/resume-ranker.git
cd resume-ranker
```

### Setup Virtual Environment (using Terminal)

- On Windows:

```
python -m venv venv
.\venv\Scripts\activate
```

- On Linux:

```
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Run the Application

- On Windows: 
```
python app.py
```

- On Linux/macOS: (Run this command first: chmod +x run.sh)

```
python3 app.py
```

- Open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Troubleshooting

- For PDF text extraction issues, ensure resumes are actual text PDFs (not scanned images).
- If app reloads with no results, check console for errors and try sample resumes.
