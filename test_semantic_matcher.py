import os
from app.services.parser.document_parser import DocumentParser
from app.services.extractor.information_extractor import InformationExtractor
from app.services.matcher.semantic_matcher import SemanticMatcher  # assuming this file exists
from pprint import pprint

# Instantiate components
parser = DocumentParser()
extractor = InformationExtractor()
matcher = SemanticMatcher()

# Load and parse job description
with open("sample_job.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()
    jd_info = extractor.extract(jd_text)

# Load, parse, and extract info from resumes
resume_dir = "resumes"
data_list = []

for file in os.listdir(resume_dir):
    filepath = os.path.join(resume_dir, file)

    # Parse document using correct method
    parsed = parser.parse_document(filepath)
    text = parsed["content"]

    # Extract structured data
    extracted = extractor.extract(text)
    data_list.append(extracted)

# Match each resume against the JD
for i, resume_data in enumerate(data_list):
    print(f"\n--- Resume {i+1} ---")
    score, explanation = matcher.match(resume_data, jd_info)
    print(f"Match Score: {score:.2f}")
    pprint(explanation)
