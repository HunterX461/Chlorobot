from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import logging

# Import your custom modules for object detection and response generation
from yolov8_model import detect_objects
from gpt2_chatbot import generate_response  # Updated import

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create FastAPI instance
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define template directory
templates = Jinja2Templates(directory="templates")

# Define Pydantic model for question request
class QuestionRequest(BaseModel):
    question: str
    objects: list

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload_image/")
async def upload_image(file: UploadFile = File(...)):
    """Upload an image and detect objects in it."""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image.")

    file_location = f"temp/{file.filename}"

    # Save the uploaded file
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    try:
        # Detect objects in the uploaded image
        objects_detected = detect_objects(file_location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup: Remove the temporary file
        if os.path.exists(file_location):
            os.remove(file_location)

    logging.info(f"Objects detected: {objects_detected}")
    return {"objects_detected": objects_detected}

@app.post("/ask_question/")
async def ask_question(request: QuestionRequest):
    """Generate a response based on the detected objects and the user's question."""
    # Validate that objects is a list
    if not isinstance(request.objects, list):
        raise HTTPException(status_code=400, detail="Objects must be a list.")

    # Validate that the question is not empty
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Generate response
    response = generate_response(request.objects, request.question)
    return JSONResponse(content={"response": response})
