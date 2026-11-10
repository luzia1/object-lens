from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.image_validator import validate_format, validate_size, validate_image
from app.services.image_processor import decode_image, convert_to_hsv, extract_object_hsv_pixels, prepare_color_features, cluster_colors
from app.services.object_segmenter import segment_objects

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
    decoded_image = decode_image(contents)
    
    objects = segment_objects(decoded_image) 
    
    if objects is None:
                raise HTTPException(
                status_code=422,
                detail="Não foi identificado nenhum objeto para segmentar"
            )
    
    hsv_image = convert_to_hsv(decoded_image)

    objects_metadata = []
    
    for object in objects:
        object_hsv_pixels = extract_object_hsv_pixels(hsv_image, object["mask"])
                
        if object_hsv_pixels.size == 0:
                        raise HTTPException(
                        status_code=422,
                        detail="Não foi encontrado qualquer objeto para analisar."
                    )
                
        color_features = prepare_color_features(object_hsv_pixels)
        color_results = cluster_colors(color_features)

        object_metadata = {
            "object_id": object["object_id"],
            "class_id": object["class_id"],
            "class_name": object["class_name"],
            "confidence": object["confidence"],
            "colors": color_results
        }
                    
        objects_metadata.append(object_metadata)

    return{
        "filename": image.filename,
        "content_type": image.content_type,
        "size": len(contents),
        "dimensions": decoded_image.shape,
        "object_results": objects_metadata
    }