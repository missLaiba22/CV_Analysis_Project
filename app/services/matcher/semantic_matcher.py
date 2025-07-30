import os
from typing import List, Tuple, Dict, Any
from sentence_transformers import SentenceTransformer, util


class SemanticMatcher:
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def flatten_resume_data(self, data: Dict[str, Any]) -> str:
        text_chunks = []
        for field in ['skills', 'experience', 'education', 'projects', 'certifications']:
            for item in data.get(field, []):
                if isinstance(item, str):
                    text_chunks.append(item)
                elif isinstance(item, dict):
                    text_chunks.extend([str(v) for v in item.values()])
        return ' '.join(text_chunks)

    def flatten_jd_data(self, jd_data: Dict[str, Any]) -> str:
        jd_chunks = []
        for field in ['skills', 'experience', 'education', 'location']:
            for item in jd_data.get(field, []):
                if isinstance(item, str):
                    jd_chunks.append(item)
                elif isinstance(item, dict):
                    jd_chunks.extend([str(v) for v in item.values()])
        return ' '.join(jd_chunks)

    def match(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
        resume_text = self.flatten_resume_data(resume_data)
        jd_text = self.flatten_jd_data(jd_data)

        resume_embedding = self.model.encode(resume_text, convert_to_tensor=True)
        jd_embedding = self.model.encode(jd_text, convert_to_tensor=True)

        score = util.cos_sim(resume_embedding, jd_embedding).item()
        explanation = {
            'semantic_similarity_score': round(score, 4)
        }
        return score, explanation

    def rank_resumes(self, resumes: List[Dict[str, Any]], jd_data: Dict[str, Any], top_k: int = 5) -> List[Tuple[int, float]]:
        rankings = []
        for idx, resume in enumerate(resumes):
            score, _ = self.match(resume, jd_data)
            rankings.append((idx, score))
        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings[:top_k]
