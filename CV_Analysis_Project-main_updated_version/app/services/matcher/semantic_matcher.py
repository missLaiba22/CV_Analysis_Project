from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple, Union, Any
from pprint import pprint
import logging
import re

logger = logging.getLogger(__name__)

class SemanticMatcher:
    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or {
            "domain": 0.6,  # Highest weight for domain match
            "skills": 0.25,
            "experience": 0.1,
            "education": 0.05
        }
        
        # Strict domain incompatibility rules
        self.incompatible_domains = {
            'accounting': ['ai_ml', 'engineering'],
            'ai_ml': ['accounting'],
            'engineering': ['accounting'],
            'general': []  # General can match with anything
        }

    def match(self, resume_embedding: List[float], jd_embedding: List[float], 
              resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhanced matching with strict domain checks and weighted scoring
        Returns: {
            "score": weighted match score (0-1),
            "details": {
                "base_score": cosine similarity,
                "domain_match": 0/1,
                "skills_match": ratio,
                "education_match": 0/1,
                "experience_match": ratio
            }
        }
        """
        try:
            # Calculate base embedding similarity
            base_score = cosine_similarity([resume_embedding], [jd_embedding])[0][0]
            
            # Get domains
            resume_domain = resume_data.get("domain", "general")
            jd_domain = jd_data.get("domain", "general")
            
            # Strict domain compatibility check
            domain_match = self._check_domain_compatibility(resume_domain, jd_domain)
            
            if not domain_match:
                return {
                    "score": 0.0,  # Zero score for incompatible domains
                    "details": {
                        "base_score": float(base_score),
                        "domain_match": 0.0,
                        "skills_match": 0.0,
                        "education_match": 0.0,
                        "experience_match": 0.0
                    }
                }
            
            # Calculate component matches
            skills_match = self._calculate_skills_match(
                resume_data.get("skills", []),
                jd_data.get("required_skills", [])
            )
            
            education_match = self._check_education(resume_data, jd_data)
            experience_match = self._check_experience(resume_data, jd_data)
            
            # Calculate weighted score
            weighted_score = (
                (1.0 if domain_match else 0.0) * self.weights["domain"] +
                skills_match * self.weights["skills"] +
                education_match * self.weights["education"] +
                experience_match * self.weights["experience"]
            )
            
            return {
                "score": min(1.0, max(0.0, weighted_score)),  # Clamp between 0-1
                "details": {
                    "base_score": float(base_score),
                    "domain_match": 1.0 if domain_match else 0.0,
                    "skills_match": skills_match,
                    "education_match": education_match,
                    "experience_match": experience_match
                }
            }
            
        except Exception as e:
            logger.error(f"Matching error: {str(e)}")
            return {
                "score": 0.0,
                "details": {
                    "base_score": 0.0,
                    "domain_match": 0.0,
                    "skills_match": 0.0,
                    "education_match": 0.0,
                    "experience_match": 0.0
                }
            }

    def _check_domain_compatibility(self, resume_domain: str, jd_domain: str) -> bool:
        """Strict domain compatibility check with exact matching"""
        if resume_domain == jd_domain:
            return True
            
        # Check explicit incompatibility rules
        for domain, incompatible in self.incompatible_domains.items():
            if jd_domain.startswith(domain):
                return not any(resume_domain.startswith(d) for d in incompatible)
            if resume_domain.startswith(domain):
                return not any(jd_domain.startswith(d) for d in incompatible)
                
        return False  # Default to False for unknown combinations

    def _calculate_skills_match(self, resume_skills: List[str], jd_skills: List[str]) -> float:
        """Calculate Jaccard similarity between skill sets"""
        if not jd_skills:
            return 0.0
            
        resume_set = {s.lower() for s in resume_skills}
        jd_set = {s.lower() for s in jd_skills}
        
        intersection = len(resume_set & jd_set)
        union = len(resume_set | jd_set)
        
        return intersection / union if union > 0 else 0.0

    def _check_education(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> float:
       """Check if education requirements are met - returns float score"""
       if not jd_data.get("strict_requirements", False):
          return 1.0  # No strict requirements
        
       if jd_data.get("domain", "") == "accounting":
          resume_certs = {c.lower() for c in resume_data.get("certifications", [])}
          resume_edu = " ".join(resume_data.get("education", [])).lower()
        
        # Check for required accounting certifications
          required_certs = {'ca', 'acca', 'cpa'}
          if any(c in required_certs for c in resume_certs):
             return 1.0
          if any(term in resume_edu for term in required_certs):
             return 1.0
            
          return 0.0
        
       return 1.0  # Default pass for other domains

    def _check_experience(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> float:
        """Check experience match - returns float score"""
        if not self._check_domain_compatibility(resume_data.get("domain", ""), jd_data.get("domain", "")):
           return 0.0  # Zero if domains are incompatible
        
        resume_exp = resume_data.get("years_of_experience", 0)
        jd_min_exp = jd_data.get("min_experience", 0)
    
        if jd_min_exp == 0:  # No minimum requirement
           return 1.0
        
        return 1.0 if resume_exp >= jd_min_exp else 0.5 * (resume_exp / jd_min_exp)

    def generate_explanation(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate human-readable matching explanation that matches scoring logic"""
        domain_match = self._check_domain_compatibility(
           resume_data.get("domain", ""), 
           jd_data.get("domain", "")
        )
    
    # Use the actual scoring methods for consistency
        education_score = self._check_education(resume_data, jd_data)
        experience_score = self._check_experience(resume_data, jd_data)
    
        required_skills = set(s.lower() for s in jd_data.get("required_skills", []))
        resume_skills = set(s.lower() for s in resume_data.get("skills", []))
    
        return {
           "domain_match": domain_match,
           "education_met": education_score >= 0.5,  # Consider scores >= 0.5 as "met"
           "experience_met": experience_score >= 0.5,
           "matched_skills": sorted(required_skills & resume_skills),
           "missing_skills": sorted(required_skills - resume_skills),
           "jd_domain": jd_data.get("domain", ""),
           "resume_domain": resume_data.get("domain", ""),
           "education_score": education_score,  # Add actual scores for transparency
           "experience_score": experience_score
       }

    def rank_candidates(self, resumes: List[Dict[str, Any]], jd_embedding: List[float], 
                       jd_data: Dict[str, Any], embedder: Any) -> List[Tuple[float, Dict[str, Any], Dict[str, Any]]]:
        """Rank candidates by match score"""
        ranked = []
        for resume in resumes:
            try:
                emb = embedder.generate_embeddings(resume.get("content", ""))
                match_result = self.match(emb, jd_embedding, resume, jd_data)
                ranked.append((
                    match_result["score"],
                    resume,
                    match_result["details"]
                ))
            except Exception as e:
                logger.error(f"Error processing resume: {str(e)}")
                continue
                
        return sorted(ranked, key=lambda x: x[0], reverse=True)