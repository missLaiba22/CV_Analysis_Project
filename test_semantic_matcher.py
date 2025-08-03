import os
from pprint import pprint
from app.services.parser.document_parser import DocumentParser
from app.services.extractor.information_extractor import InformationExtractor
from app.services.embedding.embedding_generator import EmbeddingGenerator  # Your custom module
from app.services.matcher.semantic_matcher import SemanticMatcher        # Your custom module

def main():
    # Initialize components
    parser = DocumentParser()
    extractor = InformationExtractor()
    embedder = EmbeddingGenerator()  # Uses "all-MiniLM-L6-v2" by default
    matcher = SemanticMatcher()      # Uses weights={"skills": 0.4, "experience": 0.3, ...}

    # --- Step 1: Load and process Job Description ---
    with open("sample_job.txt", "r", encoding="utf-8") as f:
        jd_text = f.read()
        jd_info = extractor.extract_job_information(jd_text)  # Returns dict (e.g., {"required_skills": [...], "min_experience": X})

    # Generate JD embeddings
    jd_embedding = embedder.generate_embeddings(jd_text)

    # --- Step 2: Load and process Resumes ---
    resume_dir = "resumes"  # Directory containing CVs (PDF/DOCX)
    data_list = []

    for file in os.listdir(resume_dir):
        if file.endswith((".pdf", ".docx", ".txt")):
            filepath = os.path.join(resume_dir, file)
          
            # Parse and extract CV data
            parsed = parser.parse_document(filepath)
            extracted = extractor.extract_cv_information(parsed["content"])  # Returns dict (e.g., {"name": "...", "skills": [], ...})
            data_list.append(extracted)

    # --- Step 3: Match and Rank Candidates ---
    ranked_candidates = matcher.rank_candidates(
        resumes=data_list,
        jd_embedding=jd_embedding,
        jd_data=jd_info,
        embedder=embedder
    )

    # --- Step 4: Display Results ---
    print("=== Top Candidates ===")
    for rank, (score, resume, details) in enumerate(ranked_candidates, 1):
        print(f"\n--- Rank #{rank} (Score: {score:.2f}) ---")
        print("Name:", resume.get("name", "N/A"))
        # print("Explanation:")
        # pprint(matcher.generate_explanation(resume, jd_info))
        print("Details:")
        pprint(details)

if __name__ == "__main__":
    main()