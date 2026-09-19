import re
import spacy
import numpy as np 
from backend.core.remote_embedder import RemoteEmbedder
from backend.core.config import HF_MODEL_ID, HF_TOKEN
from typing import Dict,List,Optional,Tuple

from backend.utils.file_utils import log_warning
from backend.utils.matching import fuzzy_match_keywords



#We have defined the regex pattern here but not in function coz ye har baar compile honge and so we dont want hr baar function call pr ye compile ho 
ZIP_CODE_PATTERN = r'\b\d{5}(?:-\d{4})?\b'

STREET_ADDRESS_PATTERN = (
    r'\b\d+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+'
    r'(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Circle|'
)


#lazy loaded singleton so hum apna finetuned model ek hi baar load kre baar baar nai, sb functions isko use krenge jab tk khud ka embedder na diya ho
_default_embedder: Optional[RemoteEmbedder] = None

def _get_default_embedder() -> RemoteEmbedder:
    global _default_embedder
    if _default_embedder is None:
        _default_embedder = RemoteEmbedder(HF_MODEL_ID, HF_TOKEN)
    return _default_embedder


#ye tier score is we gonna use this helper function later in diff things like for score compairision
def _tier_score(n:float,tiers:list)->float:
    for threshold,pts in tiers:
        if n>=threshold:
            return pts
    return 0.0



#Location detection 
def detect_location_info(text:str,nlp:spacy.language)->Dict:
    locations=[]


    #Now we gonna use 3 method to abstract the address for 2 reasons 1st of as a fallback and 2nd is ki like kabhi spaCY model detect na kr ske ZIP code vagera detect to vo bhi ho jay detect 

    #Method 1st is using spacy NER method isme location hum simply pta krte hai using the spaCY model
    doc=nlp(text)
    for ent in doc.ents:
        if ent.label_ in ['GPE','LOC']:
            locations.append({'text':ent.text,'type':ent.label_.lower(),'start': ent.start_char})


    #method 2 street address using the regex this is a fallback for mthd:-1
    for match in re.finditer(STREET_ADDRESS_PATTERN, text, re.IGNORECASE):
        locations.append({'text': match.group(), 'type': 'address', 'start': match.start()})


    #ZIP/PIN code regex pattern this is a fallback for mthd 2nd like agr 2nd mthd fail hota hai to we gonna use ZIP code 
    for match in re.finditer(ZIP_CODE_PATTERN, text):
        locations.append({'text': match.group(), 'type': 'zip', 'start': match.start()})

    #Then simply getting the extraxted locartion 
    has_address = any(loc['type'] == 'address' for loc in locations)
    has_zip     = any(loc['type'] == 'zip' for loc in locations)


    #To now we gonna add panalty if user nai proper ghr ka address bhi daal rakha hai to.
    if has_address and has_zip:
        privacy_risk,penalty='high',5.0
    elif has_address or has_zip:
        privacy_risk,penalty='high',4.0
    elif len(locations)>3:
        privacy_risk,penalty='medium',3.0
    elif locations:
        privacy_risk,penalty='low',2.0
    else:
        privacy_risk,penalty='none',0.0


    #Now we simply gonna give recomendation ki bhai yha yha dikkat hai acc to the info user exposes in resume
    recommendations=[]

    if not locations:
        recommendations.append("No privacy concerns detected.")
    if has_address:
        recommendations.append("Remove full street address - ATS system dosent need address")
    if has_zip:
        recommendations.append("Remove ZIP code - This level of location detail is unnecssary ")
    if privacy_risk in ('low','medium') and not has_address and not has_zip:
        recommendations.append("Consider reducing location mentions. 'City', 'State' in contact header is sufficient.")

    return {
        'location_found': len(locations) > 0,
        'detected_locations': locations,
        'privacy_risk': privacy_risk,
        'recommendations': recommendations,
        'penalty_applied': penalty,
    }




def _calculate_semantic_similarity(skill:str,text:str,embedder:RemoteEmbedder)->float:
    #Similarity calculate by isng cosin similarity:- (A.B)/(|A|x|B|)
    if not skill or not text:
        return 0.0
    try:
        skill_vec=embedder.encode(skill,convert_to_tensor=False)
        text_vec=embedder.encode(text,convert_to_tensor=False)
        #(A.B)/(|A|x|B|)
        similarity=np.dot(skill_vec,text_vec)/(np.linalg.norm(skill_vec)*np.linalg.norm(text_vec))
        return float(max(0.0,min(1.0,similarity)))  #0-1 ke bitch m
    except Exception as e:
        log_warning(f'Similarity error for {skill}:{e}')
        return 0.0
    



#Yhe hum skils ka exect match krenge from the user's project or exp
def _skill_matches(skill:str,text:str,embedder:RemoteEmbedder,threshold:float)->Tuple[bool,float]:
    if skill.lower() in text.lower():
        return True,1.0
    #To scores ke lia we gonna call _calculate_semantic_similarity helper func which gonna use cosin to find similarity
    sim=_calculate_semantic_similarity(skill,text,embedder)
    return sim>=threshold,sim





#Yha hum particularly user ke projects se dhund rhe hai ki jo skills project mai use kri h vo de
def validate_skills_with_projects(skills: List[str],projects: List[Dict],experience_entries: List[Dict], embedder: Optional[RemoteEmbedder] = None,threshold: float = 0.6,) -> Dict:
    #agr koi embedder pass nai kia to apna finetuned wala use kr lenge (SENTENCE_TRANSFORMER_MODEL wala)
    embedder = embedder or _get_default_embedder()

    if not skills:
        return {
            'validated_skills': [],
            'unvalidated_skills': [],
            'validation_percentage': 0.0,
            'skill_project_mapping': {},
            'validation_score': 0.0,
        }
  
    experience_text = ' '.join(
        f"{e.get('job_title', '')} {e.get('company', '')} {e.get('description', '')}"
        for e in experience_entries
        if isinstance(e, dict)
    ).strip()

    validated_skills = []
    unvalidated_skills = []
    skill_project_mapping = {}

    for skill in skills:
        matching_projects = []
        max_similarity = 0.0

        for project in projects:
            project_text = (
                f"{project.get('title', '')} "
                f"{project.get('description', '')}"
            )
            matched, sim = _skill_matches(
                skill,
                project_text,
                embedder,
                threshold
            )

            max_similarity = max(max_similarity, sim)

            if matched:
                matching_projects.append(
                    project.get('title', 'Untitled Project')
                )

        if experience_text:
            matched, sim = _skill_matches(
                skill,
                experience_text,
                embedder,
                threshold
            )
            max_similarity = max(max_similarity, sim)

        if matching_projects:
            validated_skills.append({
                'skill': skill,
                'projects': matching_projects
            })
            skill_project_mapping[skill] = matching_projects
        else:
            unvalidated_skills.append(skill)
            skill_project_mapping[skill] = []

    validation_percentage = (
        len(validated_skills) / len(skills)
    ) * 100

    validation_score = validation_percentage * 15.0

    return {
        'validated_skills': validated_skills,
        'unvalidated_skills': unvalidated_skills,
        'validation_percentage': validation_percentage,
        'skill_project_mapping': skill_project_mapping,
        'validation_score': validation_score,
    }





#01: formatting score
def _calc_formatting_score(parsed_resume: Dict, text: str) -> float:

    score = 0.0

    #Basicaally we are extracting the diff entiries from the parsed resume data 
    exp_entries  = [e for e in parsed_resume.get('experience', []) if isinstance(e, dict)]
    edu_entries  = [e for e in parsed_resume.get('education', [])  if isinstance(e, dict)]
    skills       = parsed_resume.get('skills', [])
    summary      = parsed_resume.get('professional_summary', '')
    proj_entries = [p for p in parsed_resume.get('projects', [])   if isinstance(p, dict)]

    #Then what we are doing is simply scoring on basis of the entires
    if exp_entries and any(e.get('job_title') or e.get('description') for e in exp_entries):
        score += 3.0
    if edu_entries:
        score += 2.0
    if len(skills) >= 3:
        score += 2.0
    if len(summary) > 30:
        score += 1.5
    if proj_entries:
        score += 1.5

    #Now we gonna check the bullet parrerns
    bullet_count = sum(
        1 for line in text.split('\n')
        if re.match(r'^\s*[•\-\*\◦]', line) or re.match(r'^\s*\d+\.', line) #Regex  
    )
    score += _tier_score(bullet_count, [(15,5.0),(10,4.0),(5,3.0),(3,2.0),(1,1.0)])

    #Agr saari fields hai to good score bhada dega
    filled = sum(1 for has_it in [
        bool(exp_entries), bool(edu_entries), bool(skills),
        bool(summary.strip()), bool(proj_entries),
    ] if has_it)    
    score += _tier_score(filled, [(4,5.0),(3,4.0),(2,3.0),(1,2.0)])

    return min(20.0, max(0.0, score)) #And yhe we are makig sure ki sscore is range ke bhar na .jay 




#02 for JD jeywords score
def _calc_keywords_score(resume_keywords: List[str],skills: List[str],jd_keywords: Optional[List[str]] = None) -> float:

    score = 0.0
    score += _tier_score(len(resume_keywords), [(20,10.0),(15,8.0),(10,6.0),(5,4.0),(3,2.0)])
    score += _tier_score(len(skills),          [(15,10.0),(10,8.0),(7,6.0),(5,4.0),(3,2.0)])

    if jd_keywords:
        all_resume_terms = list(set(resume_keywords + skills))
        fuzzy_result     = fuzzy_match_keywords(all_resume_terms, jd_keywords, threshold=80)
        match_pct        = len(fuzzy_result['matched']) / len(jd_keywords) if jd_keywords else 0
        score += _tier_score(match_pct, [(0.7,5.0),(0.5,4.0),(0.3,3.0),(0.2,2.0),(0.1,1.0)])
    
    elif len(resume_keywords) >= 10:
        score += 3.0

    return min(25.0, max(0.0, score))




#3. CONTENT QUALITY SCORE
def _calc_content_score(text: str, action_verbs: List[str],grammar_results: Dict,)->float:
    score = 0.0
    score += _tier_score(len(action_verbs), [(15,10.0),(10,8.0),(7,6.0),(5,4.0),(3,2.0)])

    number_patterns = [
        r'\d+%',
        r'\$\d+',
        r'\d+[kKmMbB]',
        r'\d+\s*(?:users|customers|clients|projects|hours|days|months|years)',
        r'(?:increased|decreased|improved|reduced|grew|saved)\s+(?:by\s+)?\d+',
    ]
    achievement_count = sum(len(re.findall(p, text, re.IGNORECASE)) for p in number_patterns)
    score += _tier_score(achievement_count, [(10,5.0),(7,4.0),(5,3.0),(3,2.0),(1,1.0)])

    grammar_penalty = grammar_results.get('penalty_applied', 0.0)
    score += max(0.0, 10.0 - grammar_penalty / 2.0)

    return min(25.0, max(0.0, score))





#4. SKILL VALIDATION SCORE
def _calc_skill_validation_score(validation_results: Dict) -> float:
    return min(15.0, max(0.0, validation_results.get('validation_score', 0.0)))




#5. ATS COMPATIBILITY SCORE (basically this is for ki humeri machine resume ko kitni aasani se read and all kr skti hai ye ye batayga)
def _calc_ats_compatibility_score(text: str,location_results: Dict, parsed_resume: Dict,) -> float:
    score = 15.0
    #dedeuction01
    score -= location_results.get('penalty_applied', 0.0)

    #deduction02
    special_chars = len(re.findall(r'[│┤├┼┴┬╔╗╚╝═║╠╣╦╩╬]', text))  #Regex
    if special_chars > 20:    score -= 2.0
    elif special_chars > 10:  score -= 1.0

    exp_entries  = [e for e in parsed_resume.get('experience', []) if isinstance(e, dict)]
    edu_entries  = [e for e in parsed_resume.get('education', [])  if isinstance(e, dict)]
    skills_count = len(parsed_resume.get('skills', []))

    exp_desc_len = sum(len(e.get('description', '')) for e in exp_entries)
    edu_desc_len = sum(len((e.get('degree') or '') + (e.get('institution') or '')) for e in edu_entries)  # Handle None to prevent string concatenation errors

    #deduction03
    short_sections = sum([
        bool(exp_entries) and exp_desc_len < 20,
        bool(edu_entries) and edu_desc_len < 20,
        bool(parsed_resume.get('skills')) and skills_count < 2,
    ])
    if short_sections >= 2:    score -= 2.0
    elif short_sections >= 1:  score -= 1.0

    if exp_entries and skills_count > 5:
        score += 1.0

    return min(15.0, max(0.0, score))




#Score aggregation and final interpretation
def calculate_overall_score(text: str,parsed_resume: Dict,skills: List[str],keywords: List[str],action_verbs: List[str], skill_validation_results: Dict,
    grammar_results: Dict,location_results: Dict,jd_keywords: Optional[List[str]] = None,experience_months: int = 0,)->Dict:

    formatting_score        = _calc_formatting_score(parsed_resume, text)
    keywords_score          = _calc_keywords_score(keywords, skills, jd_keywords)
    content_score           = _calc_content_score(text, action_verbs, grammar_results)
    skill_validation_score  = _calc_skill_validation_score(skill_validation_results)
    ats_compatibility_score = _calc_ats_compatibility_score(text, location_results, parsed_resume)

    COMPONENT_MAX = {
        'formatting': 20.0, 'keywords': 25.0, 'content': 25.0,
        'skill_validation': 15.0, 'ats_compatibility': 15.0,
    }

    formatting_pct        = (formatting_score        / COMPONENT_MAX['formatting'])        * 100.0
    keywords_pct          = (keywords_score          / COMPONENT_MAX['keywords'])          * 100.0
    content_pct           = (content_score           / COMPONENT_MAX['content'])           * 100.0
    skill_validation_pct  = (skill_validation_score  / COMPONENT_MAX['skill_validation'])  * 100.0
    ats_compatibility_pct = (ats_compatibility_score / COMPONENT_MAX['ats_compatibility']) * 100.0

    skills_keywords_pct = (keywords_pct * 0.6) + (skill_validation_pct * 0.4)

    base_score = (
        skills_keywords_pct   * 0.40 +
        content_pct           * 0.30 +
        formatting_pct        * 0.15 +
        ats_compatibility_pct * 0.15
    )

    penalties = {}
    bonuses   = {}
    score     = base_score

    if grammar_results.get('penalty_applied', 0.0) > 0:
        penalties['grammar'] = grammar_results['penalty_applied']

    if location_results.get('penalty_applied', 0.0) > 0:
        penalties['location_privacy'] = location_results['penalty_applied']

    validation_pct = skill_validation_results.get('validation_percentage', 0.0)
    if validation_pct >= 0.9:
        bonuses['excellent_skill_validation'] = 2.0
        score += 2.0
    elif validation_pct >= 0.8:
        bonuses['good_skill_validation'] = 1.0
        score += 1.0

    if grammar_results.get('total_errors', 0) == 0:
        bonuses['perfect_grammar'] = 1.0
        score += 1.0

    if jd_keywords and len(jd_keywords) > 0:
        all_resume_terms = list(set((keywords or []) + (skills or [])))
        fuzzy_result     = fuzzy_match_keywords(all_resume_terms, jd_keywords, threshold=80)
        missing_pct      = len(fuzzy_result['missing']) / len(jd_keywords)

        if missing_pct > 0.7:
            penalties['missing_jd_keywords'] = 15.0
            score -= 15.0
        elif missing_pct > 0.5:
            penalties['missing_jd_keywords'] = 10.0
            score -= 10.0
        elif missing_pct > 0.3:
            penalties['missing_jd_keywords'] = 5.0
            score -= 5.0

    overall_score = min(100.0, max(0.0, score))
    interpretation = _generate_score_interpretation(overall_score)

    return {
        'overall_score':           round(overall_score, 1),
        'formatting_score':        round(formatting_score, 1),
        'keywords_score':          round(keywords_score, 1),
        'content_score':           round(content_score, 1),
        'skill_validation_score':  round(skill_validation_score, 1),
        'ats_compatibility_score': round(ats_compatibility_score, 1),
        'overall_interpretation':  interpretation,
        'penalties':               penalties,
        'bonuses':                 bonuses,
    }





#Overall score calculation and interpretation  basically yha hum jo jo aacha hai user ke resume me vo return krvaynge
def generate_strengths(score_results: Dict, skill_validation_results: Dict, grammar_results: Dict,)-> List[str]:

    strengths = []
    if score_results['formatting_score']       >= 16:
        strengths.append(' Well-structured with clear sections and bullet points')
    if score_results['keywords_score']          >= 20:
        strengths.append(' Strong keyword optimization and skills presence')
    if score_results['content_score']           >= 20:
        strengths.append(' Excellent use of action verbs and quantifiable achievements')
    if score_results['skill_validation_score']  >= 12:
        pct = skill_validation_results.get('validation_percentage', 0) * 100
        strengths.append(f' {pct:.0f}% of skills are validated by projects')
    if score_results['ats_compatibility_score'] >= 13:
        strengths.append(' Excellent ATS compatibility with clean formatting')
    if grammar_results.get('total_errors', 0)   == 0:
        strengths.append(' Error-free grammar and spelling')

    if not strengths:
        strengths.append('Your resume has potential - focus on the recommendations below')
    return strengths





#Critical issues that could cause ATS rejection mai hum yha vo vo return krvaynge
def generate_critical_issues(score_results: Dict, grammar_results: Dict, location_results: Dict,)->List[str]:
    issues = []

    critical_errors = len(grammar_results.get('critical_errors', []))
    if critical_errors > 0:
        issues.append(f' {critical_errors} critical grammar/spelling error(s) detected')
    if location_results.get('privacy_risk') == 'high':
        issues.append('High privacy risk: Remove detailed location information')
    if score_results['formatting_score']       < 10:
        issues.append(' Poor formatting: Add clear sections and bullet points')
    if score_results['keywords_score']         < 12:
        issues.append(' Insufficient keywords and skills')
    if score_results['skill_validation_score'] < 7:
        issues.append(' Most skills lack supporting evidence in projects')

    return issues







#Actionable improvements to enhance ATS performance
def generate_improvements(score_results: Dict, skill_validation_results: Dict,) ->List[str]:
    improvements = []

    if 12 <= score_results['formatting_score']       < 16:
        improvements.append('Add more bullet points and improve section organization')
    if 14 <= score_results['keywords_score']          < 20:
        improvements.append('Include more relevant keywords and technical skills')
    if 14 <= score_results['content_score']           < 20:
        improvements.append('Add more quantifiable achievements and action verbs')
    if 7  <= score_results['skill_validation_score']  < 12:
        unvalidated_count = len(skill_validation_results.get('unvalidated_skills', []))
        improvements.append(f'Validate {unvalidated_count} skill(s) by adding relevant project details')
    if 9  <= score_results['ats_compatibility_score'] < 13:
        improvements.append('Simplify formatting for better ATS compatibility')

    return improvements






#Interpretation of overall score
def _generate_score_interpretation(overall_score: float) -> str:
    if overall_score >= 90:    return 'Excellent! Your resume is highly optimized for ATS systems.'
    elif overall_score >= 80:  return 'Great! Your resume should perform well with most ATS systems.'
    elif overall_score >= 70:  return 'Good! Your resume is ATS-friendly with room for minor improvements.'
    elif overall_score >= 60:  return 'Fair. Your resume needs some improvements to be fully ATS-compatible.'
    elif overall_score >= 50:  return 'Below Average. Significant improvements needed for ATS compatibility.'
    else:                      return 'Poor. Your resume requires major revisions to pass ATS screening.'