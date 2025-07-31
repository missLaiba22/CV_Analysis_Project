import re
import spacy
import nltk
from typing import Dict, List, Any, Optional
import logging

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

logger = logging.getLogger(__name__)

class InformationExtractor:
    """Enhanced information extractor with domain awareness"""
    
    def __init__(self):
        spacy_model = 'en_core_web_sm'
        try:
            self.nlp = spacy.load(spacy_model)
        except OSError:
            logger.warning(f"Spacy model {spacy_model} not found. Installing...")
            spacy.cli.download(spacy_model)
            self.nlp = spacy.load(spacy_model)
        
        # Enhanced skill patterns with domain identifiers
        self.skill_patterns = [
            r'\b(?:Python|Java|C\+\+|TensorFlow|PyTorch|Scikit-learn)\b',
            r'\b(?:Machine Learning|Deep Learning|Computer Vision|NLP)\b',
            r'\b(?:IFRS|GAAP|ISA|Audit|Taxation|Financial Reporting)\b',
            r'\b(?:ACCA|CA|CPA|Chartered Accountant)\b',
            r'\b(?:Excel|QuickBooks|SAP|Oracle|ERP)\b'
        ]
        
        # Education patterns
        self.education_patterns = [
            r'\b(?:Bachelor|BSc|MSc|MBA|PhD|B\.Tech|M\.Tech)\b',
            r'\b(?:Computer Science|Engineering|Accounting|Finance)\b',
            r'\b(?:University|College|Institute)\b'
        ]

    def extract_cv_information(self, text: str) -> Dict[str, Any]:
        """Extract information from CV text"""
        doc = self.nlp(text)
        experience = self._extract_experience(text)
        
        return {
            "name": self._extract_name(doc, text),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "skills": self._extract_skills(text),
            "years_of_experience": experience[0]["total_years"] if experience else 0,
            "domain": self._infer_domain(text),
            "education": self._extract_education_details(text),
            "certifications": self._extract_certifications(text),
            "projects": self._extract_projects(text)
        }

    def extract_job_information(self, text: str) -> Dict[str, Any]:
        """Extract information from job description"""
        doc = self.nlp(text)
        req_edu = self._extract_required_education(text)
        
        return {
            "required_skills": self._extract_required_skills(text),
            "min_experience": self._extract_required_experience(text) or 0,
            "required_education": req_edu,
            "strict_requirements": self._has_strict_requirements(text),
            "domain": self._infer_domain(text),
            "location": self._extract_location(doc),
            "requirements": self._extract_requirements(text)
        }

    # ===== DOMAIN-SPECIFIC METHODS =====
    def _infer_domain(self, text: str) -> str:
        text_lower = text.lower()
    
    # 1. Accounting/Audit detection
        accounting_terms = [
            'audit', 'accounting', 'ifrs', 'isa', 'acca', 'ca', 'cpa', 
            'financial report', 'chartered accountant', 'taxation',
            'financial statement', 'auditing standards', 'gaap'
        ]
        if any(re.search(rf'\b{term}\b', text_lower) for term in accounting_terms):
           return "accounting"
    
    # 2. AI/ML detection with higher priority for specific terms
        ml_terms = [
            'machine learning', 'computer vision', 'ai\b', 'neural network',
            'deep learning', 'tensorflow', 'pytorch', 'data science',
            'reinforcement learning', 'image recognition'
        ]
        if any(re.search(rf'\b{term}\b', text_lower) for term in ml_terms):
            return "ai_ml"
    
    # 3. Engineering fields
        engineering_terms = {
           'electrical': ['electrical', 'circuit', 'pcb', 'power systems'],
           'mechanical': ['mechanical', 'cad', 'thermodynamics'],
           'software': ['software', 'developer', 'programming']
          }
        for domain, terms in engineering_terms.items():
             if any(re.search(rf'\b{term}\b', text_lower) for term in terms):
                return f"engineering_{domain}"
    
        return "general"
    
    def _has_strict_requirements(self, text: str) -> bool:

        """Check if JD has strict qualification requirements"""
        return bool(re.search(r'\b(?:CA|ACCA|CPA)\s+(?:required|mandatory)\b', text, re.I))

    # ===== EDUCATION EXTRACTION =====
    def _extract_education_details(self, text: str) -> List[str]:
        """Get detailed education information from CV"""
        education = []
        # Extract degrees
        degree_matches = re.finditer(
            r'\b(?:Bachelor|BSc|Master|MSc|MBA|PhD|B\.Tech|M\.Tech)\b.*?\b(?:in\s+)?([A-Za-z\s]+)',
            text, re.I
        )
        education.extend(match.group(0).strip() for match in degree_matches if match.group(1).strip())
        return education

    def _extract_required_education(self, text: str) -> List[str]:
        """Extract required education from job description"""
        education = []
        # Look for education requirements
        matches = re.finditer(
            r'\b(?:Bachelor|Master|PhD|BSc|MSc|MBA|CA|ACCA)\b.*?\b(?:in\s+)?([A-Za-z\s]+)',
            text, re.I
        )
        education.extend(match.group(0).strip() for match in matches if match.group(1).strip())
        return education

    # ===== CORE EXTRACTION METHODS =====
    def _extract_name(self, doc, text) -> Optional[str]:
        """Extract person name using NER"""
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text.strip()
        for line in text.splitlines():
            line = line.strip()
            if line and len(line.split()) in [2, 3, 4] and all(w[0].isupper() for w in line.split() if w):
                return line
        return None

    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group() if match else None

    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number"""
        phone_patterns = [
            r'(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4}',
            r'Cell[:\s]*([\d\-\+\(\)\s]+)',
            r'Phone[:\s]*([\d\-\+\(\)\s]+)',
        ]
        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group().strip()
        return None

    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from text"""
        skills = set()
        for pattern in self.skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.update([match.lower() for match in matches])
        return list(skills)

    def _extract_experience(self, text: str) -> List[Dict[str, Any]]:
        """Extract experience details"""
        experience = []
        exp_pattern = r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)'
        matches = re.findall(exp_pattern, text, re.IGNORECASE)
        if matches:
            total_years = max([int(match) for match in matches])
            experience.append({"total_years": total_years})
        return experience

    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications with proper word boundaries"""
        cert_patterns = [
           r'\bAWS\s+Certified\b',
           r'\bAzure\s+Certified\b',
           r'\bGCP\s+Certified\b',
           r'\bPMP\b', r'\bCISSP\b', r'\bCCNA\b', r'\bCCNP\b', r'\bCEH\b', r'\bCompTIA\b',
           r'\bCA\b', r'\bACCA\b', r'\bCPA\b'
        ]
        certifications = []
        for pattern in cert_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            certifications.extend([match.strip() for match in matches if match.strip()])
        return list(set(certifications))

    def _extract_projects(self, text: str) -> List[Dict[str, Any]]:
        """Extract project information"""
        projects = []
        project_patterns = [
            r'\b(?:Project|Developed|Built):?\s*([A-Za-z0-9\s\-_]+)',
            r'\b(?:Led|Managed)\s+([A-Za-z0-9\s\-_]+)\s+(?:project|initiative)\b'
        ]
        for pattern in project_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            projects.extend({"name": match.strip()} for match in matches if match.strip())
        return projects

    def _extract_required_skills(self, text: str) -> List[str]:
        """Extract required skills from job description"""
        required_skills = []
        required_patterns = [
            r'\b(?:Required|Must have|Essential):?\s*([A-Za-z0-9\s,]+)',
            r'\b(?:Skills|Technologies):?\s*([A-Za-z0-9\s,]+)',
            r'\b(?:Experience with|Knowledge of)\s+([A-Za-z0-9\s,]+)\b'
        ]
        for pattern in required_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                skills = [skill.strip() for skill in match.split(',')]
                required_skills.extend(skills)
        return list(set(required_skills))

    def _extract_required_experience(self, text: str) -> Optional[int]:
        """Extract required years of experience"""
        exp_patterns = [
            r'\b(\d+)\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)\s+(?:required|needed)\b',
            r'\b(?:Minimum|At least)\s+(\d+)\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)\b'
        ]
        for pattern in exp_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None

    def _extract_location(self, doc) -> Optional[str]:
        """Extract location using NER"""
        for ent in doc.ents:
            if ent.label_ == "GPE":
                return ent.text.strip()
        return None

    def _extract_requirements(self, text: str) -> List[str]:
        """Extract general requirements"""
        requirements = []
        req_patterns = [
            r'\b(?:Requirements|Qualifications|Must have)\s*:?\s*([A-Za-z0-9\s,\.]+)',
            r'•\s*([A-Za-z0-9\s,\.]+)',
            r'-\s*([A-Za-z0-9\s,\.]+)'
        ]
        for pattern in req_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            requirements.extend([match.strip() for match in matches if match.strip()])
        return requirements

    def extract(self, text: str) -> Dict[str, Any]:
        """Unified extraction method"""
        if self._is_job_description(text):
            return self.extract_job_information(text)
        return self.extract_cv_information(text)

    def _is_job_description(self, text: str) -> bool:
        """Detect if text is a job description"""
        return bool(re.search(r'\b(?:job\s*description|requirements|qualifications)\b', text, re.I))