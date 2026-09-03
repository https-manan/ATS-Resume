from typing import Any,Dict,List,Optional
from pydantic import BaseModel # pydantic is a popular open-source data validation and parsing library for Python
#pydantic is for ki vo input ko validate krta hai, then usko JSON mai convert krta hai and generate krta hai documentation 
#and BaseModel is to define the shape, types, and validation rules of your data objects.


class ComponentScores(BaseModel):  #This is for components score ki total ATS score is 100 and so usme kun kun sa component ka kitna kitna score
    formatting: float
    keywords: float
    content: float
    skill_validation: float
    ats_compatibility: float



class JDComparison(BaseModel): #Jobdescription compairision
    match_percentage: float
    semantic_similarity: float
    matched_keywords: List[str]
    missing_keywords: List[str]
    skills_gap: List[str]



class SkillValidationDetails(BaseModel):
    validated: List[Dict[str, Any]] = []       # [{'skill': str, 'projects': [str]}]
    unvalidated: List[str] = []                # ['Flask', 'A/B Testing', ...]
    total: int = 0
    validated_count: int = 0
    validation_pct: float = 0.0



class IssueDetail(BaseModel):
    issue_title: str
    severity_level: str
    ats_impact: str
    explanation: str
    where_it_appears: str
    how_to_fix: str
    action_items: List[str] = []
    example_improvement: str



class AnalysisResponse(BaseModel):
    ATS_score: float
    component_scores: ComponentScores
    issues_summary: List[str]
    detailed_feedback: List[IssueDetail]
    jd_match_analysis: Optional[JDComparison] = None    #Job description optional hai user daal bhi skta hai and nahi bhi 
    skill_validation_details: Optional[SkillValidationDetails] = None

    ats_score: float
    keyword_match: float = 0.0
    missing_keywords: List[str] = []
    matched_keywords: List[str] = []
    suggestions: List[str] = []
    strengths: List[str] = []
    critical_issues: List[str] = []
    skills: List[str] = []
    jd_comparison: Optional[JDComparison] = None
    warnings: List[str] = []
    interpretation: str = ""