import numpy as np

from ultralytics import YOLO

model = YOLO("yolo26n-seg.pt") 

def segment_objects(image):
    results = model(image, retina_masks=True)
    result = results[0]  

    if result.masks is None:
        print("Não foram detetados objetos com máscara.")
        return None

    print("Dimensões das máscaras:", result.masks.data.shape)
    print("Classes detetadas:", result.boxes.cls)
    print("Confiança:", result.boxes.conf)

    masks = get_masks(result)

    return masks

def get_masks(result):
    masks = []

    for index, mask_data in enumerate(result.masks.data):

        print(f"\n--- Objeto {index + 1} ---")

        mask = mask_data.cpu().numpy()
        mask = (mask > 0).astype(np.uint8) * 255

        class_id = int(result.boxes.cls[index].item()) 
        class_name = result.names[class_id] 
        confidence = float(result.boxes.conf[index].item()) 
        
        print("Classe:", class_name)
        print("Confiança:", round(confidence, 4))

        mask_metadata = {
                "mask": mask,
                "object_id": index + 1,
                "class_id": class_id,
                "class_name": class_name,
                "confidence": confidence
                }
        
        masks.append(mask_metadata)

    return masks




    