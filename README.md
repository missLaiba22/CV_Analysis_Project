# CV & Job Description Analyzer 🧠📄

An intelligent CV analysis system that matches resumes with job descriptions using advanced NLP techniques, including LLM-powered extraction and semantic similarity matching. Perfect for recruiters and HR professionals to efficiently screen candidates.

---

## 🔧 Features

### 📄 Document Processing
- **Multi-format Support**: Parse resumes (PDF, DOCX, TXT)
- **Smart Extraction**: Extract name, contact, skills, experience, education, certifications
- **Domain Detection**: Automatically identify candidate domain (AI/ML, Accounting, Engineering, etc.)

### 🤖 AI-Powered Analysis
- **LLM Integration**: Google Gemini API for enhanced information extraction
- **Fallback System**: Robust regex-based extraction when LLM unavailable
- **Model Fallback**: Automatic switching between Gemini models (1.5-pro → 1.5-flash → pro)

### 🎯 Intelligent Matching
- **Semantic Similarity**: BERT-based embedding comparison
- **Domain Compatibility**: Strict domain matching rules
- **Weighted Scoring**: Configurable weights for skills, experience, education
- **Candidate Ranking**: Ranked results with detailed explanations

### 🛡️ Reliability Features
- **Rate Limit Handling**: Graceful degradation when API limits exceeded
- **Error Recovery**: Comprehensive error handling and logging
- **Flexible Operation**: Works with or without internet connection

---

## 🛠 Tech Stack

- **Python 3.9+**
- **NLP Libraries**: spaCy, NLTK, regex
- **AI/ML**: transformers (BERT), PyTorch, sentence-transformers
- **LLM Integration**: Google Generative AI (Gemini)
- **Document Processing**: PyPDF2, python-docx, pdfplumber

---

## 🚀 Setup Instructions

### 1. Clone and Setup
```bash
git clone https://github.com/missLaiba22/CV_Analysis_Project.git
cd cv_analysis
python -m venv venv
venv\Scripts\activate  # on Windows
# or
source venv/bin/activate  # on Linux/Mac
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key (Optional)
For enhanced LLM extraction, add your Gemini API key to `config.py`:
```python
GEMINI_API_KEY = "your_api_key_here"
```
Get a free API key from: https://makersuite.google.com/app/apikey

---

## 🧪 Testing & Usage

### Basic Testing
```bash
# Test regex-only extraction (no API key needed)
python test_regex_only.py

# Test LLM extraction (requires API key)
python test_llm_extractor.py

# Test full pipeline
python test_semantic_matcher.py
```

### Individual Components
```bash
# Test parsing and extraction
python test_parsing_extraction.py

# Test semantic matching
python test_semantic_matcher.py
```

---

## 📁 Project Structure

```
cv_analysis/
├── app/
│   ├── services/
│   │   ├── parser/          # Document parsing (PDF, DOCX, TXT)
│   │   ├── extractor/       # Information extraction (regex + LLM)
│   │   ├── embedding/       # BERT embeddings for similarity
│   │   └── matcher/         # Semantic matching and ranking
│   ├── api/                 # FastAPI endpoints (optional)
│   ├── core/               # Core utilities
│   └── models/             # Data models
├── resumes/                # Sample resumes for testing
├── tests/                  # Test scripts
└── config.py              # Configuration (API keys)
```

---

## 🔄 How It Works

1. **Document Parsing**: Extract text from various document formats
2. **Information Extraction**: 
   - Primary: LLM-powered extraction (Gemini API)
   - Fallback: Regex-based extraction
3. **Semantic Matching**: Compare embeddings using BERT
4. **Domain Validation**: Ensure candidate-job domain compatibility
5. **Scoring & Ranking**: Weighted scoring with detailed explanations

---

## ⚙️ Configuration

### LLM Settings
- **Model Priority**: `gemini-1.5-pro` → `gemini-1.5-flash` → `gemini-pro`
- **Rate Limit Handling**: Automatic fallback to regex extraction
- **Error Recovery**: Comprehensive logging and error messages

### Matching Weights
```python
weights = {
    "domain": 0.6,      # Domain compatibility
    "skills": 0.25,     # Skills match
    "experience": 0.1,  # Experience level
    "education": 0.05   # Education requirements
}
```

---

## 🚨 Rate Limits & API Usage

- **Free Tier**: Gemini API has rate limits (requests per minute/day)
- **Fallback Mode**: System automatically switches to regex extraction
- **No API Key**: System works entirely offline with regex extraction

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🆘 Troubleshooting

### Common Issues
- **Rate Limit Errors**: Wait for limits to reset or use regex-only mode
- **Model Not Found**: System automatically tries alternative models
- **Import Errors**: Ensure all dependencies are installed

### Getting Help
- Check the test scripts for usage examples
- Review error logs for detailed information
- Ensure your API key is valid (if using LLM features)



