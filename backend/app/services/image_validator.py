from fastapi import HTTPException
from PIL import Image
from io import BytesIO

MAX_FILE_SIZE = 10 * 1024 * 1024 

def validate_format(content_type: str):
    if content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=415,
                detail="Formato de imagem não suportado."
            )

def validate_size(contents: bytes): 
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="A imagem excede o tamanho máximo permitido de 10 MB."
        )

def validate_image(contents: bytes):
    try:
        Image.open(BytesIO(contents)).verify
    
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="O ficheiro enviado não contém uma imagem válida."
        )
      
      