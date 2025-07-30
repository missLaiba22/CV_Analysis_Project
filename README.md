Sure! Here's the updated `README.md` with an additional section that includes instructions for running `test_parsing_extraction.py`, which tests the CV and JD parsing + information extraction functionality.

---

```markdown
# CV and Job Description Analyzer 🧠📄

This project is an intelligent CV filtering and ranking system designed to help recruiters or hiring platforms identify the best-matched candidates based on job descriptions. It combines rule-based parsing with semantic similarity to evaluate resumes and generate structured insights.

---

## 🔍 Features

- ✅ Parse CVs (PDF, DOCX, TXT) and extract:
  - Name, Contact Info
  - Skills, Education
  - Work Experience, Projects
  - Certifications

- ✅ Extract Job Description (JD) requirements:
  - Skills, Education, Experience, Location

- ✅ Match Resumes to JD using:
  - Semantic similarity (BERT-based)
  - Rule-based skill/education/experience comparison

- ✅ Rank candidates and provide explainable match scores

---

## 🛠 Tech Stack

- **Python 3.9+**
- **spaCy** for NLP parsing
- **transformers (BERT)** for semantic embedding
- **Torch** for vector computations
- **NLTK & Regex** for rule-based info extraction
- **FastAPI (optional)** for backend API (if extended to web)

---

## 📁 Project Structure

```

cv\_analysis/
│
├── app/
│   ├── parsers/
│   │   └── document\_parser.py          # Extract text from resumes
│   ├── extractors/
│   │   └── information\_extractor.py    # Extract structured info from CVs & JD
│   ├── services/
│   │   └── matcher/
│   │       └── semantic\_matcher.py     # BERT-based similarity scoring
│
├── test\_semantic\_matcher.py            # Test script for semantic matcher
├── test\_parsing\_extraction.py          # Test script for parsing + info extraction
├── requirements.txt
└── README.md

````

---

## 🚀 Getting Started

1. **Clone the repo:**
```bash
git clone [https://github.com/yourusername/cv_analysis](https://github.com/missLaiba22/CV_Analysis_Project).git
cd cv_analysis
````

2. **Create and activate virtual environment:**

```bash
python -m venv venv
venv\Scripts\activate  # on Windows
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## 🧪 Running Tests

### ✅ Test CV & JD Information Extraction:

```bash
python test_parsing_extraction.py
```

This script will:

* Parse resumes and JD documents
* Extract and display structured info like name, email, skills, education, etc.

### ✅ Test Semantic Matching:

```bash
python test_semantic_matcher.py
```

This script will:

* Compare resumes against the job description
* Print match scores with semantic similarity breakdown

---

## 📊 Output Sample

```
--- Resume 1 (resume_alex.pdf) ---
Match Score: 0.36
{'semantic_similarity_score': 0.3561}

--- Resume 2 (resume_taylor.pdf) ---
Match Score: 0.17
{'semantic_similarity_score': 0.1682}
```

## 📄 License

This project is licensed under the MIT License.

---

## 👩‍💻 Author

**Laiba Idrees**

```
