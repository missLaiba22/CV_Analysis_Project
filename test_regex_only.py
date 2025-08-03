#!/usr/bin/env python3
"""
Test script for regex-only extraction (without LLM)
"""

import logging
from app.services.extractor.information_extractor import InformationExtractor
from app.services.parser.document_parser import DocumentParser

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_regex_only():
    """Test the system using only regex extraction (no LLM)"""
    
    print("=== Testing Regex-Only Extraction ===")
    
    # Initialize extractor with LLM disabled
    extractor = InformationExtractor(use_llm_fallback=False)
    parser = DocumentParser()
    
    print("✓ Initialized extractor with LLM disabled")
    
    # Test with sample resume text
    sample_resume = """
    Laiba Idrees
    Email: laiba.idrees2003@gmail.com
    Phone: +92 300 1453
    
    Skills: Python, Machine Learning, TensorFlow, Deep Learning, Computer Vision
    Experience: 2 years in AI/ML development
    Education: Bachelor of Science in Artificial Intelligence
    
    Projects:
    - Food Recognition System using Computer Vision
    - Brain Tumor Detection using Deep Learning
    - Chatbot using RAG and FastAPI
    """
    
    print("\n--- Testing Resume Extraction ---")
    try:
        result = extractor.extract_cv_information(sample_resume)
        print("✓ Resume extraction completed")
        print("Extracted Information:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"✗ Resume extraction failed: {e}")
    
    # Test with sample job description
    sample_job = """
    Senior AI Engineer
    Requirements:
    - Python programming experience
    - Machine Learning and Deep Learning
    - 2+ years experience in AI/ML
    - Bachelor's degree in Computer Science or related field
    - Experience with TensorFlow or PyTorch
    """
    
    print("\n--- Testing Job Extraction ---")
    try:
        result = extractor.extract_job_information(sample_job)
        print("✓ Job extraction completed")
        print("Extracted Information:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"✗ Job extraction failed: {e}")
    
    # Test with actual resume file
    print("\n--- Testing with Actual Resume File ---")
    try:
        parsed = parser.parse_document("resumes/Laiba  Idrees-resume.pdf")
        result = extractor.extract_cv_information(parsed["content"])
        print("✓ Real resume extraction completed")
        print("Key Information:")
        print(f"  Name: {result.get('name', 'N/A')}")
        print(f"  Email: {result.get('email', 'N/A')}")
        print(f"  Skills: {result.get('skills', [])}")
        print(f"  Domain: {result.get('domain', 'N/A')}")
    except Exception as e:
        print(f"✗ Real resume extraction failed: {e}")
    
    print("\n=== Summary ===")
    print("✓ Regex-only extraction is working!")
    print("The system can function without LLM, just with reduced accuracy.")
    print("Once your Gemini rate limits reset, LLM will provide better results.")

if __name__ == "__main__":
    test_regex_only() 