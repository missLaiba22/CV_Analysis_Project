from app.services.parser.document_parser import DocumentParser
from app.services.extractor.information_extractor import InformationExtractor

# 1. Parse the CV file
parser = DocumentParser()
cv_result = parser.parse_document("Tooba Idrees - Resume.pdf")  # Change to your file path

print("=== Parsed CV Content ===")
print(cv_result["content"])
print()

# 2. Extract information from the CV
extractor = InformationExtractor()
cv_info = extractor.extract_cv_information(cv_result["content"])

print("=== Extracted CV Information ===")
for k, v in cv_info.items():
    print(f"{k}: {v}")
print()

# 3. Extract information from a job description (as string or file)
with open("sample_job.txt", "r", encoding="utf-8") as f:
    job_text = f.read()

job_info = extractor.extract_job_information(job_text)

print("=== Extracted Job Information ===")
for k, v in job_info.items():
    print(f"{k}: {v}")