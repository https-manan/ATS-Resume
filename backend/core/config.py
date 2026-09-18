#Here we gonna store all the setting and configration files we wanna save.

import os 
from pathlib import Path
from tarfile import SUPPORTED_TYPES


try:
    from dotenv import load_dotenv
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    load_dotenv(PROJECT_ROOT / '.env')

except ImportError:
    pass



#API metadata
APP_TITLE='ATS RESUME ANALYZER API'
APP_VERSION='1.0.0'
APP_DESCRIPTION='Analyse resume against job description using NLP + ML'


#CORS
ALLOWED_ORIGINS=[
    'http://localhost:5173',    #Vite dev server(React)
    'http://localhost:3000',    #Fallback for react
    'http://127.0.0.1:5173'
]


#FILE size setting 
MAX_FILE_SIZE_MB=5
MAX_FILE_SIZE_BYTES=5*1024*1024




#Type of files we gonna support :-PDF,DOC and word-docx
SUPPORTED_MIME_TYPES={
    'application/pdf':'pdf',
    'application/msword':'doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document':'docx'
}
SUPPORTED_EXTENTIONS={'.pdf','.doc','.docx'}



#Basically SpaCY ka primary model use krenge and if in case its not load and work we gonna fallback to secondary model of spaCY 
SPACY_MODEL_PRIMARY = 'en_core_web_md'
SPACY_MODEL_SECONDRY = 'en_core_web_sm'


#This is sentance transformation model which we have fine tuned the BERT model
# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"
# Sentence Transformer model
SENTENCE_TRANSFORMER_MODEL = str(
    BACKEND_ROOT / "bert_fineTuned_model"
)



#Basically jo weightage hogi for total 100 score of the resume
#And yha isi liya hai(not in a function in a file) coz hum aapne hiab se baad me he change kr ske
SCORE_WEIGHTS = {
    "formatting": 20,
    "keywords": 25,
    "content": 25,
    "skill_validation": 15,
    "ats_compatibility": 15
}


JD_KEYWORD_WEIGHT = 0.6
JD_SEMANTIC_WEIGHT = 0.4


GROQ_API_KEY=os.getenv('GROQ_API_KEY','')
SUPABASE_URL=os.getenv('SUPABASE_URL')
SUPABASE_KEY=os.getenv('SUPABASE_KEY')
SUPABASE_JWT_SECRET="basdjahvbuhbjhnkjb"