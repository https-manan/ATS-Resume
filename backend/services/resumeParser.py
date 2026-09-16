import io
import magic #Jo use hoga check krne mai file PDF hai ya nahi by internal content and all this gonna check by internal content of the uploaded doc
from typing import Tuple,Optional
import pdfplumber  #These 2 packages pdfplumber and pyPDF2 are for PDF parsing and all and 2 of these coz 1 fail ho jay to 2nd 
import PyPDF2
from docx import Document  #TO help parsing docx file
from backend.utils.file_utils import (FileParsingError,TextExtractionError,FileUploadError,log_error,log_warning,log_info,with_fallback) 
from backend.core.config import (MAX_FILE_SIZE_MB,MAX_FILE_SIZE_BYTES,SUPPORTED_MIME_TYPES)



#This is for parsing issues ki hum file ko parse he nahi kr pa rhe usme data proper format mai nahi hai 
class FileParsingError(Exception):
    pass


#and this is validatuion mai he issue hai like file size bda hai ya something 
class FileValidationError(Exception):
    pass


def validate_file(file_data:bytes,filename:str)->tuple[bool,str,Optional[str]]:
    #Here we gonna just validate the size of the file
    file_size_bytes=len(file_data)
    if file_size_bytes>MAX_FILE_SIZE_BYTES: 
        size_mb=file_size_bytes/(1024*1024)
        return False,(f'Your uploaded file size {size_mb} MB exceeds the maximum limit of {MAX_FILE_SIZE_MB} please upload a smaller file.'),None

    if file_size_bytes==0:
        return False,"Uploaded file is empty...Please upload a valid resume."


    #to aab agr file validated hai and all then we just abstract the file components 
    try:
        mime_type=magic.from_buffer(file_data,mime=True)   #Mime file ke aandar ja kr btata hai file ka d_type hai kya by checking inside the file not just by extention
    except Exception as e:
        return False, f'Error determining the file type {e}',None
 

    #Now we validate that file types(that we detected from MIME) is supported hai ya nhi
    if mime_type not in SUPPORTED_MIME_TYPES:
        supported=', '.join(SUPPORTED_MIME_TYPES.keys()).upper()
        return False,(f'Unsupported file types:{mime_type}. ' 
                      f'Please upload one of {supported}'),None   #basically uploaded file supported nahi hai so return false and None 

    return True,'',SUPPORTED_MIME_TYPES[mime_type] #Else agr mime type supported ke aandar aata hai then return True



#so owr resume have 2 layers visible and anotation layer visible is for title and subtitle and all and anotation is to get hyperlinkks and jo content normally abstract nahi ho skta like portfolio and all  
def _extract_pdf_hyperlinks(file_data: bytes) -> str:
    urls = []
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_data)) #reading the file
        for page in reader.pages: 
            if '/Annots' not in page:   #Hyper links are stored in annotation layer we cannot abstract em like pdf.extract_text function
                continue
            for annot_ref in page['/Annots']:
                try:
                    annot = annot_ref.get_object()
                    if annot.get('/Subtype') != '/Link':
                        continue
                    action = annot.get('/A', {})
                    uri = action.get('/URI', '')
                    if uri and isinstance(uri, (str, bytes)):
                        # PyPDF2 may return bytes for URI values
                        if isinstance(uri, bytes):
                            uri = uri.decode('utf-8', errors='ignore')
                        uri = uri.strip()
                        if uri.startswith('http'):
                            urls.append(uri)
                except Exception:
                    pass
    except Exception:
        pass
    return '\n'.join(urls)




def _extract_pdf_with_pdfplumber(file_data:bytes)->str:
    text=''
    with pdfplumber.open(io.BytesIO(file_data)) as pdf:
        for page in pdf.pages:
            page_text=page.extract_text()
            if page_text:
                text+=page_text+'\n'    #basically saare text ko save krenge by using pdfplumber

    if not text.strip():   #If no text means PDF is empty
        raise TextExtractionError(
            'pdfplumer extract no text',
            user_message='No text could be extracted from the PDF.'
        )
    hyperlinks=_extract_pdf_hyperlinks(file_data) #We gonna extract the hyperlinks using func we defined
    if hyperlinks:
        text=text.strip()+'\n'+hyperlinks

    return text.strip()




#Abb same kaam hum pyPDF 2 se krvaynge coz as a fallback use krenge hum pyPDF 2 ko
def _extract_pdf_with_pypdf2(file_data: bytes)->str:
    text = ''
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_data))
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + '\n'

    if not text.strip():
        raise TextExtractionError(
            'PyPDF2 extracted no text',
            user_message='No text could be extracted from the PDF.'
        )

    hyperlinks = _extract_pdf_hyperlinks(file_data)
    if hyperlinks:
        text = text.strip() + '\n' + hyperlinks

    return text.strip()




def extract_text_from_pdf(file_data: bytes) -> str:
    try:
        result, used_fallback = with_fallback(    #fallback is ki hum phale pdfplumber use krenge and then pyPDF2
            _extract_pdf_with_pdfplumber,
            _extract_pdf_with_pypdf2,
            file_data,
            log_fallback=True
        )
 
        if used_fallback:  #Means humne fallback me 2 me se 1 function use kr lia hai 
            log_info("PDF EXTRACTED successfully using the PyPDF2 fallback",context="resume_parser")

        return result   #FIX: this was only returned inside the `if used_fallback` block before,
                         #so when pdfplumber (the primary method) succeeded, the function fell through
                         #and returned None -> caused "object of type 'NoneType' has no len()" in routes.

    except Exception as e:
        log_error(e, context="extract_text_from_pdf")
        raise FileParsingError(
            "Failed to extract text from the PDF using both PyPDF2 and pdfplumber",
            "The PDF may be corrupted. Try uploading another.",
            "Please ensure it contains selectable text."
        )




#Now we gonna abstract the docx
def extract_text_from_docx(file_data:bytes)->str:  #This docx is for kabhi kabhi user table ki form me aapna data daal dete hai so to abstrarct that we use this 
    try:
        doc=Document(io.BytesIO(file_data))
        text_parts=[]

        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text)


        for table in doc.tables:#Docx file mai user kabhi kabhi table k form ma bhi data upload krte hai so make sure to abstract that also 
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        text_parts.append(cell.text)

        text='\n'.join(text_parts)

        if not text.strip():
            raise FileParsingError('No text could be abstracted from the document.','The document may be empty or curropted.')

    except Exception as e:
        log_error(e, context='extract_text_from_docx')
        raise FileParsingError(
            'Failed to extract text from DOCX. '
            'The document may be corrupted or in an unsupported format. '
            'Please try re-saving or converting to PDF.'
        ) from e





#So agr doc type hai to we dont support that 
def extract_text_from_doc(file_data: bytes) -> str:
    raise FileParsingError(
        'Legacy .doc format is not supported. '
        'Please convert your document to .docx or .pdf and try again. '
        'You can convert using Microsoft Word, Google Docs, or online tools'
    )





#So this is the orchestrator function basically manager of owr this file ki kunsa type of PDF ya doc haiuske hisab se function call
def extract_text(file_data:bytes,file_type:str)->str:
    if file_type=='pdf':
        return extract_text_from_pdf(file_data)
    elif file_type=='docx':
        return extract_text_from_docx(file_data)
    elif file_type=='doc':
        return extract_text_from_doc(file_data)
    else:
        raise FileParsingError(f"Invalid file type:{file_type}. kindly upload in: pdf,docx")





#This is the main master function of this file 
def parse_resume_file(file_data: bytes, filename:str)->Tuple[str, dict]:
    log_info(f'parsing file :{filename}', context='parse_resume_file') #to check kunsi file p kaam kr rhe hai hum 

    #phase01:validate file
    try:
        is_valid, error_msg, file_type=validate_file(file_data, filename)
        if not is_valid:
            log_warning(f'valiudation failed for file {filename}', context='parse_resume_file')
            raise FileValidationError(error_msg)
    
    except FileValidationError as e:
        raise 

    except Exception as e:
        log_error(e, context='parse_resume_file_validation')
        raise FileValidationError(
            'Could not validate the uploaded file. Please ensure it is a valid PDF or DOCX.') from e


    
    #phase02: extraction of file
    try:
        text = extract_text(file_data, file_type)
        log_info(f'Extracted {len(text)} chars from {filename}', context='parse_resume_file')

    except FileParsingError:
        raise   # Re-raise unchanged

    except Exception as e:
        log_error(e, context='parse_resume_file_extraction')
        raise FileParsingError(
            'An unexpected error occurred while processing the file. '
            'Please try again or contact support if the problem persists.'
        ) from e

    metadata = {
        'filename':        filename,
        'file_type':       file_type,
        'file_size_bytes': len(file_data),
        'text_length':     len(text),
        'success':         True,
    }
    return text, metadata   #Returning file data to whome so ever calls this function