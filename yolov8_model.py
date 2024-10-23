from ultralytics import YOLO
from PIL import Image, ImageDraw
import numpy as np

# Load YOLOv8 model
model = YOLO('yolov8s.pt')

def detect_objects(image_path: str, conf_threshold: float = 0.5):
    # Load image
    image = Image.open(image_path)
    original_image = image.copy()

    # Run YOLOv8 object detection
    results = model(image)

    # Extract detected object names and bounding boxes
    detected_objects = []
    boxes = results[0].boxes  # Access the first result
    for box in boxes:
        confidence = box.conf[0].item()
        if confidence >= conf_threshold:  # Only consider detections above the threshold
            cls = int(box.cls[0].item())
            detected_objects.append(model.names[cls])
            # Draw bounding box on the image for visualization
            draw = ImageDraw.Draw(original_image)
            x1, y1, x2, y2 = box.xyxy[0].tolist()  # Get box coordinates
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            draw.text((x1, y1), f"{model.names[cls]}: {confidence:.2f}", fill="red")

    # Optionally, save or display the modified image
    original_image.show()  # Display the image with bounding boxes

    return detected_objects

