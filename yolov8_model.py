from ultralytics import YOLO
from PIL import Image, ImageDraw
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load YOLOv8 model
model = YOLO('yolov8s.pt')

def detect_objects(image_path: str, conf_threshold: float = 0.2):
    """Detect objects in the given image and return their names."""
    try:
        # Load the input image
        image = Image.open(image_path)
        original_image = image.copy()

        # Run YOLOv8 object detection
        results = model(image)

        # Extract detected objects and draw bounding boxes
        detected_objects = []
        boxes = results[0].boxes  # Access the first result

        for box in boxes:
            confidence = box.conf[0].item()
            if confidence >= conf_threshold:
                cls = int(box.cls[0].item())
                detected_objects.append(model.names[cls])

                # Draw bounding box and label on the original image
                draw = ImageDraw.Draw(original_image)
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
                draw.text((x1, y1), f"{model.names[cls]}: {confidence:.2f}", fill="red")

        # Save the annotated image to the 'temp/' directory
        annotated_path = os.path.join("temp", "annotated_image.jpg")
        original_image.save(annotated_path)

        logging.info(f"Detected objects: {detected_objects}")
        return detected_objects

    except FileNotFoundError as e:
        logging.error(f"File not found: {image_path}")
        raise e  # Re-raise to be handled in the main API

    except Exception as e:
        logging.error(f"Error in detect_objects: {str(e)}")
        raise e  # Re-raise to be handled in main.py
