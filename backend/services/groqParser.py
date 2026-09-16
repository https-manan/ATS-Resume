import os
import json
import logging
from typing import Dict, Optional
from groq import Groq


logger=logging.getLogger('ats_resume_scorer') #Hum yha print sattement use nahi kr rhe coz logger gives more advantage like we can classify using logger ki error hai ya warning ha ya so on 

#NOTE: llama-3.3-70b-versatile (and llama-3.1-8b-instant) have moved to Groq's Enterprise-only
#tier and return a 404 model_not_found for regular API keys. openai/gpt-oss-120b is the current
#publicly-available production model with standard per-token pricing. Swap this if Groq changes
#their lineup again — check https://console.groq.com/docs/models for what's currently public.
GROQ_MODEL='openai/gpt-oss-120b'


#Basically ek baar he client create kr lia hai and bs call this client later not the API all the time
_client=None#yha _  (underscore) is for ki yha private variable hai for any particular file 



def _get_client()->Groq:  #This ->Groq means iss se jo o/p aayga vo expected hai as a Groq object 
    global _client
    if _client is None:
        api_key=os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in env file.")

        #So aab client krta ye hai ki Groq se baat krta hai uss LLM se jisse ek baar connection establish ho gua using this API key 
        _client=Groq(api_key=api_key) #To abb ek baar client creat ho gya to ab aage jb bhi client ko call hogo vo bss isi ko hogi  

    return _client



#This is the resume system prompt like for the system and so we are telling the sys how you should behave before getting anything 
#This is like making a base for the system ki bhai you should now act as a resume parser
RESUME_SYSTEM_PROMPT=(
    "You are a resume parser. Extract information out of resume "
    "and return only a valid JSON object.No explaination,no markdown."
)


#This is the user prompt that means user ke data ke sath sath ye prompt jaya whichs gonna tell ki bhai mere data pr aase aase kaam krna 
#To aabh hum client (jo LLM se baat krega) use bta rhe hai ki bhaai phale ye sb abstract kr BC and resume text jo parse hoke aaya hai PyPDF se ya pdfPlumber se use hum end mai as a raw text bhajenge
RESUME_USER_PROMPT = """Extract the following from this resume and return as JSON:
{{
  "name": "full name",
  "email": "email address",
  "phone": "phone number",
  "linkedin": "LinkedIn URL if present, otherwise null",
  "github": "GitHub URL if present, otherwise null",
  "professional_summary": "the full text of the Summary, Profile, About Me, Objective, or Professional Summary section at the top of the resume. Copy the ENTIRE paragraph exactly as written. If no such section exists, return an empty string.",
  "skills": ["list", "of", "skills"],
  "experience": [
    {{
      "job_title": "",
      "company": "",
      "start_date": "",
      "end_date": "",
      "duration_months": 0,
      "description": ""
    }}
  ],
  "education": [
    {{
      "degree": "",
      "institution": "",
      "year": ""
    }}
  ],
  "certifications": ["list of certifications"],
  "projects": [
    {{
      "title": "project name",
      "description": "what the project does and how it was built",
      "technologies": ["tech", "used"]
    }}
  ],
  "action_verbs": ["strong action verbs used in bullet points, e.g. developed, implemented, designed"],
  "keywords": ["important keywords and phrases from the resume for ATS matching"]
}}

Important instructions:
- For duration_months, calculate the number of months between start_date and end_date. If end_date is "Present" or "Current", calculate from start_date to now.
- For skills, extract ALL technical and soft skills mentioned anywhere in the resume.
- For action_verbs, find verbs that start bullet points or describe achievements.
- For keywords, extract noun phrases and technical terms relevant to ATS matching.
- Return ONLY valid JSON. No markdown code fences, no explanation.

Resume Text:
{raw_text}"""     #Basically this full means baski ji double curly brackets mai hai like {{}} vo to as is jayga BERT model mai pr ye {raw_text} variable hai means jo user ke resume se actually extract hua hai vo jayga  




#This is the main function jha hum actual API call kr rhe hai bss only 1 kaam thaat its gonna call the API 
#To yha hum 3 args pass krenge client(jo main LLM ki API se baat krega, then sys_prompts and then user prompts) 
def _call_groq(client: Groq,system_prompt:str,user_prompt:str)->str:
    res = client.chat.completions.create(
        model=GROQ_MODEL, 
        messages=[
            {"role": "system", "content": system_prompt},   #for system ke liya content is sys_prompt
            {"role": "user", "content": user_prompt},  #and for the user content is user_prompt
        ],
        temperature=0.0,  #IMP:- #temp humere model ki randomness ko btata hai means LLM kitna creative hai  to humne yha 0 rakha hai coz jo user ka resume aa rha hai use as is rakhe humera LLM not ki koi changes vagera kr de creative bnke 
        max_tokens=4096
    )
    return res.choices[0].message.content.strip()



#So this function is for safely extracts and parses a JSON string from text,
def _try_parse_json(text: str)->Optional[dict]: 
    # Strip markdown code fences if present:- bascially json file starts and end with ``` to use he remove kr rhe hai 
    cleaned = text.strip()
    if cleaned.startswith("```"):
        # Remove opening fence (```json or ```)
        first_newline = cleaned.index("\n") if "\n" in cleaned else len(cleaned)
        cleaned = cleaned[first_newline + 1:]
        # Remove closing fence
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None



# okey so this function is for that theek hai humne aapne LLM ko prompts and all de diya ki bhai JSON format me he return ke o/p pr what if it dosent
#So now what we gonna do is we gonna call again and again to LLM from the user side ki bhai o/p de json format mai with more strictness each time
#And ye call again iss liya kr rhe hai coz LLM's are probabilistc so they can give diff o/p each time on same i/p
def parse_resume(raw_text:str)->Dict:
    client=_get_client()
    prompt=RESUME_USER_PROMPT.format(raw_text=raw_text)
    raw_res=_call_groq(client,RESUME_SYSTEM_PROMPT,prompt)
    result=_try_parse_json(raw_res)

    # if result is None:
    #     return _validate_resume_result(result)

    logger.warning("Groq resume parser: first attempt returns invalid JSON, retrying...")

    #Tojb ek baar error aa gya to we gonna try with more stricter prompts.
    strict_prompts=(
        "Your previous prompts was not valid JSON."
        "Return only the raw JSON object, no markdown,no explaination,no coding,no code fences.\n\n"
        +prompt
    )

    raw_res=_call_groq(client,RESUME_SYSTEM_PROMPT,strict_prompts)
    result=_try_parse_json(raw_res)  #Checking iss baar kr result aacha hai 
    if result is not None:
        return _validate_resume_result(result)

    raise ValueError(f'Groq returned unparseable response after retry.Raw response:\n{raw_res}')




#Abb same kaam hum job description ke liya bhi krenge like sys prompt and user prompt for JD
JD_SYSTEM_PROMPT = (
    "You are a job description parser. Extract information and "
    "return ONLY a valid JSON object. No explanation, no markdown."
)



JD_USER_PROMPT = """Extract the following from this job description and return as JSON:
{{
    "job_title": "",
    "required_skills": ["list of must-have skills"],
    "preferred_skills": ["list of nice-to-have skills"],
    "experience_required": "",
    "education_required": "",
    "key_responsibilities": ["list of responsibilities"],
    "keywords": ["important keywords and phrases for ATS matching"]
}}

Important instructions:
- required_skills: skills explicitly stated as required or must-have.
- preferred_skills: skills stated as preferred, nice-to-have, or bonus.
- keywords: extract ALL important terms an ATS system would match against,
  including skills, technologies, certifications, and domain terms.
- Return ONLY valid JSON. No markdown code fences, no explanation.

Job Description Text:
{raw_text}"""


#Same as above the resume parser one
def parse_job_description(raw_text: str) -> Dict:
    client = _get_client()
    prompt = JD_USER_PROMPT.format(raw_text=raw_text)

    raw_response = _call_groq(client, JD_SYSTEM_PROMPT, prompt)
    result = _try_parse_json(raw_response)
    if result is not None:
        return _validate_jd_result(result)

    logger.warning("Groq JD parse: first attempt returned invalid JSON, retrying..")

    #Agr kuch nahi mila to trying with more stricter prompt 
    strict_prompt = ("Your previous response was not valid JSON."
                    "Return ONLY the raw JSON object, no markdown, no explanation, no code," + prompt)
   
    raw_response = _call_groq(client, JD_SYSTEM_PROMPT, strict_prompt)
    result = _try_parse_json(raw_response)
    if result is not None:
        return _validate_jd_result(result)

    raise ValueError(f"Groq returned unparseable response after retry. Raw response:\n{raw_response}" )


def _validate_jd_result(result: dict) -> dict:
    """Ensure JD parse result has all expected keys with correct types."""
    defaults = {
        "job_title": "",
        "required_skills": [],
        "preferred_skills": [],
        "experience_required": "",
        "education_required": "",
        "key_responsibilities": [],
        "keywords": [],
    }
    for key, default in defaults.items():
        if key not in result or result[key] is None:
            result[key] = default
        if isinstance(default, list) and not isinstance(result[key], list):
            result[key] = default

    return result



def _validate_resume_result(result: dict) -> dict:

    defaults = {
        "name": "",
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
        "professional_summary": "",
        "skills": [],
        "experience": [],
        "education": [],
        "certifications": [],
        "projects": [],
        "action_verbs": [],
        "keywords": [],
    }
    for key, default in defaults.items():
        if key not in result or result[key] is None:
            result[key] = default
        # Ensure list fields are actually lists
        if isinstance(default, list) and not isinstance(result[key], list):
            result[key] = default

    for exp in result.get("experience", []):
        if not isinstance(exp, dict):
            continue
        exp.setdefault("job_title", "")
        exp.setdefault("company", "")
        exp.setdefault("start_date", "")
        exp.setdefault("end_date", "")
        exp.setdefault("duration_months", 0)
        exp.setdefault("description", "")
        # Ensure duration_months is an int
        try:
            exp["duration_months"] = int(exp["duration_months"])
        except (ValueError, TypeError):
            exp["duration_months"] = 0

    #Validate project entries
    for proj in result.get("projects", []):
        if not isinstance(proj, dict):
            continue
        proj.setdefault("title", "")
        proj.setdefault("description", "")
        proj.setdefault("technologies", [])


    return result