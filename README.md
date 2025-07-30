# CV & Job Description Analyzer 🧠📄

This tool helps recruiters match CVs with job descriptions using NLP-based parsing and semantic similarity (BERT). It extracts key info from resumes and ranks candidates based on how well they match the JD.

---

## 🔧 Features

- Parse resumes (PDF, DOCX, TXT)
- Extract name, contact, skills, experience, education
- Extract job requirements from JD
- Compute match score (rule-based + BERT similarity)
- Rank resumes with explanations

---

## 🛠 Tech Stack

- Python 3.9+
- spaCy, NLTK, regex
- transformers (BERT), PyTorch
- FastAPI (optional)

---
---

## 🚀 Setup Instructions

```bash
git clone https://github.com/missLaiba22/CV_Analysis_Project.git
cd cv_analysis
python -m venv venv
venv\Scripts\activate  # on Windows
pip install -r requirements.txt

---

## 🧪 Run Tests

**Test Info Extraction:**

```bash
python test_parsing_extraction.py
```

**Test Matching Logic:**

```bash
python test_semantic_matcher.py
```



