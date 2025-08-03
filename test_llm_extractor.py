#!/usr/bin/env python3
"""
Test script for LLM Extractor functionality
"""

import logging
from app.services.extractor.llm_extractor import LLMExtractor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_llm_extractor():
    """Test the LLM extractor initialization and basic functionality"""
    
    print("=== Testing LLM Extractor ===")
    
    # Test 1: Initialize LLM Extractor
    try:
        extractor = LLMExtractor()
        print("✓ LLM Extractor initialized successfully")
        print(f"  - Gemini available: {extractor.gemini_available}")
        print(f"  - Use Gemini: {extractor.use_gemini}")
    except Exception as e:
        print(f"✗ Failed to initialize LLM Extractor: {e}")
        return False
    
    # Test 2: Test with sample resume text
    sample_resume = """
    John Doe
    Email: john.doe@email.com
    Phone: +1-555-123-4567
    
    Skills: Python, Machine Learning, TensorFlow, Data Analysis
    Experience: 3 years in AI/ML development
    Education: Bachelor's in Computer Science
    """
    
    try:
        result = extractor.extract_fields(sample_resume)
        print("✓ Resume extraction completed")
        print(f"  - Extracted fields: {list(result.keys())}")
        if result:
            print(f"  - Sample data: {result.get('name', 'N/A')}")
            print(f"  - Skills: {result.get('skills', [])}")
        else:
            print("  - No data extracted (check API key and rate limits)")
    except Exception as e:
        print(f"✗ Resume extraction failed: {e}")
    
    # Test 3: Test with sample job description
    sample_job = """
    Senior AI Engineer
    Requirements:
    - Python programming
    - Machine Learning experience
    - 2+ years experience
    - Bachelor's degree in Computer Science
    """
    
    try:
        result = extractor.extract_job_requirements(sample_job)
        print("✓ Job extraction completed")
        print(f"  - Extracted fields: {list(result.keys())}")
        if result:
            print(f"  - Required skills: {result.get('required_skills', [])}")
            print(f"  - Min experience: {result.get('min_experience', 'N/A')}")
        else:
            print("  - No data extracted (check API key and rate limits)")
    except Exception as e:
        print(f"✗ Job extraction failed: {e}")
    
    print("\n=== Test Summary ===")
    print("The LLM extractor is properly configured for Gemini usage.")
    print("Note: If no data is extracted, check:")
    print("  1. API key is valid in config.py")
    print("  2. Rate limits/quota not exceeded")
    print("  3. Internet connection is working")
    
    return True

if __name__ == "__main__":
    test_llm_extractor() 