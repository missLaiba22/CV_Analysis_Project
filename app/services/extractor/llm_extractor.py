# llm_extractor.py

import json
import logging
import os
from typing import Dict, Any, Optional
import re

logger = logging.getLogger(__name__)

class LLMExtractor:
    def __init__(self, api_key=None, use_gemini=True):
        """
        Initialize LLM extractor with Gemini by default
        Args:
            api_key: API key for Gemini
            use_gemini: Whether to use Gemini (default True)
        """
        self.api_key = api_key
        self.use_gemini = use_gemini
        self.gemini_available = False
        
        # Initialize Gemini
        if use_gemini:
            try:
                import google.generativeai as genai
                
                # Get API key from parameter, environment variable, or config file
                gemini_api_key = api_key or os.getenv('GEMINI_API_KEY')
                
                # Try to import from config file
                if not gemini_api_key:
                    try:
                        from config import GEMINI_API_KEY as config_key
                        if config_key and config_key != "your_gemini_api_key_here":
                            gemini_api_key = config_key
                    except ImportError:
                        pass
                
                if gemini_api_key:
                    genai.configure(api_key=gemini_api_key)
                    self.gemini_available = True
                    logger.info("✓ Using Google Gemini with API key")
                else:
                    logger.warning("No Gemini API key provided - LLM extraction will be disabled")
                    self.gemini_available = False
                    
            except ImportError:
                logger.warning("google-generativeai not installed. Install with: pip install google-generativeai")
                self.gemini_available = False
            except Exception as e:
                logger.warning(f"Gemini initialization failed: {e}")
                self.gemini_available = False

    def extract_fields(self, resume_text: str) -> Dict[str, Any]:
        """
        Extract structured information from resume text using LLM
        """
        try:
            if self.gemini_available:
                return self._extract_with_gemini(resume_text)
            else:
                logger.warning("No LLM available for extraction")
                return {}
        except Exception as e:
            logger.error(f"LLM extraction failed: {e}")
            return {}

    def _extract_with_gemini(self, resume_text: str) -> Dict[str, Any]:
        """Extract using Google Gemini API"""
        try:
            import google.generativeai as genai
            
            prompt = self._create_extraction_prompt(resume_text)
            
            # Try different models in order of preference
            model_names = ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-pro']
            
            for model_name in model_names:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    result_text = response.text
                    return self._parse_llm_response(result_text)
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        logger.warning(f"Model {model_name} not found, trying next...")
                        continue
                    else:
                        raise e
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                logger.warning(f"Gemini rate limit/quota exceeded: {error_msg[:100]}...")
            elif "404" in error_msg:
                logger.error(f"Gemini model not found: {error_msg[:100]}...")
            else:
                logger.error(f"Gemini extraction failed: {error_msg}")
            return {}

    def _create_extraction_prompt(self, resume_text: str) -> str:
        """Create a structured prompt for extraction"""
        return f"""
You are an expert resume parser. Extract the following information from this resume and return ONLY valid JSON.

IMPORTANT: Be very careful with the name extraction. Look for the person's actual name, not programming languages or other terms.

{{
    "name": "Full name of the person (e.g., 'John Doe', not 'Java' or 'Python')",
    "email": "Email address",
    "phone": "Phone number",
    "skills": ["skill1", "skill2", "skill3"],
    "education": ["degree1", "degree2"],
    "years_of_experience": number,
    "domain": "ai_ml|accounting|engineering|general",
    "certifications": ["cert1", "cert2"],
    "projects": [
        {{"name": "project name", "description": "brief description"}}
    ]
}}

Resume text:
{resume_text[:3000]}

Return only the JSON object:
"""

    def _parse_llm_response(self, response_text: str) -> Dict[str, Any]:
        """Parse LLM response and extract JSON"""
        try:
            # Find JSON in response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                logger.warning("No JSON found in LLM response")
                return {}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from LLM response: {e}")
            return {}

    def extract_job_requirements(self, job_text: str) -> Dict[str, Any]:
        """
        Extract job requirements using LLM
        """
        try:
            if self.gemini_available:
                return self._extract_job_with_gemini(job_text)
            else:
                logger.warning("No LLM available for job extraction")
                return {}
        except Exception as e:
            logger.error(f"Job extraction failed: {e}")
            return {}

    def _extract_job_with_gemini(self, job_text: str) -> Dict[str, Any]:
        """Extract job requirements using Gemini"""
        try:
            import google.generativeai as genai
            
            prompt = f"""
You are an expert job requirement parser. Extract job requirements from this job description and return ONLY valid JSON.

{{
    "required_skills": ["skill1", "skill2"],
    "min_experience": number,
    "required_education": ["education1", "education2"],
    "strict_requirements": boolean,
    "domain": "ai_ml|accounting|engineering|general",
    "location": "location",
    "requirements": ["req1", "req2"]
}}

Job description:
{job_text[:2000]}

Return only the JSON object:
"""
            
            # Try different models in order of preference
            model_names = ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-pro']
            
            for model_name in model_names:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    result_text = response.text
                    return self._parse_llm_response(result_text)
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg:
                        logger.warning(f"Model {model_name} not found, trying next...")
                        continue
                    else:
                        raise e
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                logger.warning(f"Gemini rate limit/quota exceeded: {error_msg[:100]}...")
            elif "404" in error_msg:
                logger.error(f"Gemini model not found: {error_msg[:100]}...")
            else:
                logger.error(f"Gemini job extraction failed: {error_msg}")
            return {}
