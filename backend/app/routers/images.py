from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.image_validator import validate_format, validate_size, validate_image
from app.services.image_processor import decode_image, create_test_mask, convert_to_hsv, extract_object_hsv_pixels, convert_hue_to_coordinates, prepare_color_features, cluster_colors, calculate_color_percentages

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
    mask = create_test_mask(decoded_image) #depois remover
    
    hsv_image = convert_to_hsv(decoded_image)
    object_hsv_pixels = extract_object_hsv_pixels(hsv_image, mask)
    
    color_features = prepare_color_features(object_hsv_pixels)
    color_results = cluster_colors(color_features)

    return{
        "filename": image.filename,
        "content_type": image.content_type,
        "size": len(contents),
        "dimensions": decoded_image.shape,
        "colors": color_results
    }