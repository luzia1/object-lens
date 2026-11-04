from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.image_validator import validate_format, validate_size, validate_image

router = APIRouter(
    prefix="/images",
    tags=["Images"]
)

@router.post("/analyze")
async def analyze_image(image: UploadFile = File(...)):
    
    validate_format(image.content_type)

    contents = await image.read()

    validate_size(contents)
    validate_image(contents)

    return{
        "filename": image.filename,
        "content_type": image.content_type,
        "size": len(contents)
    }