import logging
from contextlib import asynccontextmanager  #Imp decorator hai this is to making the function async
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import(ALLOWED_ORIGINS,APP_DESCRIPTION,APP_TITLE,APP_VERSION,SPACY_MODEL_PRIMARY,SPACY_MODEL_SECONDRY,SENTENCE_TRANSFORMER_MODEL)
from backend.api.routes import router


logger=logging.getLogger('ats_resume_scorer')#Basically it means that jo logs aab se aana start honge vo iss application ke honge its like logs of this app from now on and its like a mark



@asynccontextmanager  #Basically ye decorator iske inside function ko basically make/provide an async context manager.
async def lifespan(app:FastAPI):
    logger.info('Starting ATS resume Analyzer API...')

    logger.info(f'Loading spaCy NLP model:{SPACY_MODEL_PRIMARY}')
    import spacy
    try:
        app.state.nlp=spacy.load(SPACY_MODEL_PRIMARY)
        logger.info(f'Loading:- {SPACY_MODEL_PRIMARY}')
    except:
        logger.warning(f'{SPACY_MODEL_PRIMARY} not found - falling back to {SPACY_MODEL_SECONDRY}')
        app.state.nlp=spacy.load(SPACY_MODEL_SECONDRY)
        logger.info(f'Loading:- {SPACY_MODEL_SECONDRY} (fallback)')
        
    logger.info(f'Loading Sentance transformer:- {SENTENCE_TRANSFORMER_MODEL}')
    from sentence_transformers import SentenceTransformer  

    app.state.embedder=SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)
    logger.info(f'Loaded {SENTENCE_TRANSFORMER_MODEL}')

    logger.info("All models loaded. API is ready to serve requests")

    yield  #Basically yield keyword se upper likhi hui hai vo server start hone ke sath sath he perform/load ho jati hai. or we can say seerver start hone ke sath sath he start ho jati hai before loding the website
           # and jo yield ke baad likha hai vo server band hone ke baad exicute hota hai.

    logger.info('Shutting down the server') 


#FastAPI configure
app=FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan,
    docs_url='/docs',
    redoc_url='/redoc' 
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)



app.include_router(router)


#uvicorn is fastAPI run hoti hai uvicorn ki help s
if __name__=='__main__':
    import uvicorn
    uvicorn.run(
        'backend.main:app',
        host='0.0.0.0',
        port=8080,
        reload=True
    )