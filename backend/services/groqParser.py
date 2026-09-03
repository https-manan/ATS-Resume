from email import message
import os
import json
import logging
from typing import Dict
from groq import Groq


logger=logging.getLogger('ats_resume_scorer')


GROQ_MODEL='llama-3.3-70b-versatile'

_client=None

#Basically ek baar he client create kr lia hai and bs call this client later not the API all the time
def _get_client()->Groq:
    global _client
    if _client is None:
        api_key=os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in env file.")
        _client=Groq(api_key=api_key)
    return _client

RESUME_SYSTEM_PROMPT=(
    "You are a resume parser. Extract information out of resume "
    "and return only a valid JSON object.No explaination,no markdown."
)



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
{raw_text}"""



def _call_groq(client:Groq,system_prompt:str,user_prompt:str)->str:

    res=client.chat.completition.create(
        model=GROQ_MODEL,
        messages=[
            {'role':'system','content':system_prompt},
            {'role':'user','content':user_prompt}
        ]
        temprature=0.0,
        max_token=4096  
    )
    return res.choices[0].message.content.strip()



def _try_parse_json(text: str)->dict:
    # Strip markdown code fences if present
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


def parse_resume(raw_text:str)->Dict:
    client=_get_client()
    prompt=