import re
import spacy
import nltk
from typing import Dict, List, Any, Optional
import logging

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

logger = logging.getLogger(__name__)


class InformationExtractor:
    """Extract key information from CVs and job descriptions using NLP"""
    
    def __init__(self):
        spacy_model = 'en_core_web_sm'
        try:
            self.nlp = spacy.load(spacy_model)
        except OSError:
            logging.warning(f"Spacy model {spacy_model} not found. Installing...")
            spacy.cli.download(spacy_model)
            self.nlp = spacy.load(spacy_model)
        
        # Common skill patterns
        self.skill_patterns = [
            r'\b(?:Python|Java|JavaScript|C\+\+|C#|Ruby|PHP|Go|Rust|Swift|Kotlin)\b',
            r'\b(?:React|Angular|Vue|Node\.js|Django|Flask|Spring|Laravel|Express)\b',
            r'\b(?:AWS|Azure|GCP|Docker|Kubernetes|Jenkins|Git|GitHub)\b',
            r'\b(?:SQL|MySQL|PostgreSQL|MongoDB|Redis|Elasticsearch)\b',
            r'\b(?:Machine Learning|AI|Deep Learning|TensorFlow|PyTorch|Scikit-learn)\b',
            r'\b(?:Data Analysis|Data Science|Pandas|NumPy|Matplotlib|Seaborn)\b',
            r'\b(?:HTML|CSS|Bootstrap|SASS|LESS|Webpack|Babel)\b',
            r'\b(?:Linux|Unix|Windows|macOS|Shell|Bash|PowerShell)\b',
            r'\b(?:REST|API|GraphQL|SOAP|Microservices|Agile|Scrum)\b',
            r'\b(?:Excel|Power BI|Tableau|JIRA|Confluence|Slack|Teams)\b'
        ]
        
        # Education patterns
        self.education_patterns = [
            r'\b(?:Bachelor|Master|PhD|BSc|MSc|MBA|B\.Tech|M\.Tech)\b',
            r'\b(?:Computer Science|Engineering|Information Technology|Data Science)\b',
            r'\b(?:University|College|Institute|School)\b'
        ]
        
        # Experience patterns
        self.experience_patterns = [
            r'\b(\d+)\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)\b',
            r'\b(?:Senior|Junior|Lead|Principal|Staff|Associate)\b',
            r'\b(?:Developer|Engineer|Analyst|Manager|Consultant|Architect)\b'
        ]
    
    def extract_cv_information(self, text: str) -> Dict[str, Any]:
        """
        Extract key information from CV text
        
        Args:
            text: Raw CV text content
            
        Returns:
            Dictionary containing extracted information
        """
        doc = self.nlp(text)
        
        return {
            "name": self._extract_name(doc, text),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "skills": self._extract_skills(text),
            "experience": self._extract_experience(text),
            "education": self._extract_education(text),
            "certifications": self._extract_certifications(text),
            "projects": self._extract_projects(text)
        }
    
    def extract_job_information(self, text: str) -> Dict[str, Any]:
        """
        Extract key information from job description
        
        Args:
            text: Raw job description text
            
        Returns:
            Dictionary containing extracted job requirements
        """
        doc = self.nlp(text)
        
        return {
            "skills_required": self._extract_required_skills(text),
            "experience_required": self._extract_required_experience(text),
            "education_required": self._extract_required_education(text),
            "location": self._extract_location(doc),
            "requirements": self._extract_requirements(text)
        }
    
    def _extract_name(self, doc, text) -> Optional[str]:
        """Extract person name using NER"""
        # Try NER first
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text.strip()
        # Fallback: first non-empty line, likely the name
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
            r'(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4}',  # General
            r'Cell[:\s]*([\d\-\+\(\)\s]+)',  # Cell: ...
            r'Phone[:\s]*([\d\-\+\(\)\s]+)', # Phone: ...
        ]
        
        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group().strip()
        return None
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical and soft skills"""
        # Try to find a "Skills" section
        skills_section = ""
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if "skills" in line.lower():
                # Collect lines under "Skills" until next section or empty line
                section_lines = []
                for l in lines[i:i+10]:
                    if l.strip() == "" or any(h in l.lower() for h in ["education", "experience", "project", "certification"]):
                        break
                    section_lines.append(l)
                skills_section = " ".join(section_lines)
                break
        if skills_section:
            # Split by comma or semicolon
            skills = [s.strip() for s in re.split(r'[;,]', skills_section) if s.strip()]
            return skills
        # Fallback to previous method
        skills = set()
        for pattern in self.skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.update([match.lower() for match in matches])
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT"]:
                # Filter out common non-skill entities
                if not any(word in ent.text.lower() for word in ["inc", "corp", "ltd", "company"]):
                    skills.add(ent.text.lower())
        return list(skills)
    
    def _extract_experience(self, text: str) -> List[Dict[str, Any]]:
        """Extract work experience details"""
        experience = []
        
        # Look for experience patterns
        exp_pattern = r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)'
        matches = re.findall(exp_pattern, text, re.IGNORECASE)
        
        if matches:
            total_years = max([int(match) for match in matches])
            experience.append({
                "total_years": total_years,
                "description": f"{total_years} years of experience"
            })
        
        # Extract job titles
        title_pattern = r'\b(?:Senior|Junior|Lead|Principal|Staff|Associate)?\s*(?:Software|Data|DevOps|Frontend|Backend|Full Stack|Machine Learning|AI|Cloud|Security)?\s*(?:Developer|Engineer|Analyst|Manager|Consultant|Architect|Scientist)\b'
        titles = re.findall(title_pattern, text, re.IGNORECASE)
        
        for title in titles:
            if title.strip():
                experience.append({
                    "title": title.strip(),
                    "type": "job_title"
                })
        
        return experience
    
    def _extract_education(self, text: str) -> List[Dict[str, Any]]:
        """Extract education details"""
        education = []
        
        # Look for degree patterns
        degree_pattern = r'\b(?:Bachelor|Master|PhD|BSc|MSc|MBA|B\.Tech|M\.Tech)\s+(?:in\s+)?([A-Za-z\s]+)'
        matches = re.findall(degree_pattern, text, re.IGNORECASE)
        
        for match in matches:
            if match.strip():
                education.append({
                    "degree": match.strip(),
                    "type": "degree"
                })
        
        # Look for institution patterns
        institution_pattern = r'\b(?:University|College|Institute|School)\s+of\s+([A-Za-z\s]+)'
        institutions = re.findall(institution_pattern, text, re.IGNORECASE)
        
        for institution in institutions:
            if institution.strip():
                education.append({
                    "institution": institution.strip(),
                    "type": "institution"
                })
        
        return education
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        cert_patterns = [
            r'\b(?:AWS|Azure|GCP)\s+(?:Certified|Certification)\b',
            r'\b(?:PMP|CISSP|CCNA|CCNP|CEH|CompTIA)\b',
            r'\b(?:Certified|Certification)\s+([A-Za-z\s]+)\b'
        ]
        
        certifications = []
        for pattern in cert_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            certifications.extend([match.strip() for match in matches if match.strip()])
        
        return list(set(certifications))
    
    def _extract_projects(self, text: str) -> List[Dict[str, Any]]:
        """Extract project information"""
        projects = []
        
        # Look for project patterns
        project_patterns = [
            r'\b(?:Project|Developed|Built|Created|Implemented)\s*:?\s*([A-Za-z0-9\s\-_]+)',
            r'\b(?:Led|Managed|Completed)\s+([A-Za-z0-9\s\-_]+)\s+(?:project|initiative)\b'
        ]
        
        for pattern in project_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if match.strip() and len(match.strip()) > 3:
                    projects.append({
                        "name": match.strip(),
                        "description": f"Project: {match.strip()}"
                    })
        
        return projects
    
    def _extract_required_skills(self, text: str) -> List[str]:
        """Extract required skills from job description"""
        required_skills = []
        
        # Look for required skills patterns
        required_patterns = [
            r'\b(?:Required|Must have|Essential)\s*:?\s*([A-Za-z0-9\s,]+)',
            r'\b(?:Skills|Technologies)\s*:?\s*([A-Za-z0-9\s,]+)',
            r'\b(?:Experience with|Knowledge of)\s+([A-Za-z0-9\s,]+)\b'
        ]
        
        for pattern in required_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                skills = [skill.strip() for skill in match.split(',')]
                required_skills.extend(skills)
        
        # Also extract using general skill patterns
        general_skills = self._extract_skills(text)
        required_skills.extend(general_skills)
        
        return list(set(required_skills))
    
    def _extract_required_experience(self, text: str) -> Optional[int]:
        """Extract required years of experience"""
        exp_patterns = [
            r'\b(\d+)\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)\s+(?:required|needed|preferred)\b',
            r'\b(?:Minimum|At least)\s+(\d+)\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)\b'
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def _extract_required_education(self, text: str) -> List[str]:
        """Extract required education"""
        education = []
        
        # Look for education requirements
        edu_patterns = [
            r'\b(?:Bachelor|Master|PhD|BSc|MSc|MBA|B\.Tech|M\.Tech)\s+(?:degree|required|preferred)\b',
            r'\b(?:Education|Degree)\s*:?\s*([A-Za-z\s]+)\b'
        ]
        
        for pattern in edu_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            education.extend([match.strip() for match in matches if match.strip()])
        
        return list(set(education))
    
    def _extract_location(self, doc) -> Optional[str]:
        """Extract location using NER"""
        for ent in doc.ents:
            if ent.label_ == "GPE":  # Geographical Entity
                return ent.text.strip()
        return None
    
    def _extract_requirements(self, text: str) -> List[str]:
        """Extract general requirements"""
        requirements = []
        
        # Look for requirement patterns
        req_patterns = [
            r'\b(?:Requirements|Qualifications|Must have|Should have)\s*:?\s*([A-Za-z0-9\s,\.]+)',
            r'•\s*([A-Za-z0-9\s,\.]+)',
            r'-\s*([A-Za-z0-9\s,\.]+)'
        ]
        
        for pattern in req_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if match.strip() and len(match.strip()) > 5:
                    requirements.append(match.strip())
        
        return requirements 