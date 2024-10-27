from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.requests import Request
import os
import logging

# Import detect_objects function from yolov8_model.py
from yolov8_model import detect_objects
from gpt2_chatbot import generate_response

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create FastAPI instance
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define template directory
templates = Jinja2Templates(directory="templates")

class QuestionRequest(BaseModel):
    question: str
    objects: list

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload_image/")
async def upload_image(file: UploadFile = File(...)):
    """Upload an image and detect objects."""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image.")

    file_location = f"temp/{file.filename}"

    try:
        # Save the uploaded image to the temp directory
        with open(file_location, "wb") as f:
            f.write(file.file.read())

        # Detect objects in the uploaded image
        objects_detected = detect_objects(file_location)

        logging.info(f"Objects detected: {objects_detected}")
        return {"objects_detected": objects_detected}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Clean up: Remove the uploaded image after processing
        if os.path.exists(file_location):
            os.remove(file_location)

@app.post("/ask_question/")
async def ask_question(request: QuestionRequest):
    """Generate a chatbot response based on the objects and user question."""
    if not isinstance(request.objects, list):
        raise HTTPException(status_code=400, detail="Objects must be a list.")

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    response = generate_response(request.objects, request.question)
    return JSONResponse(content={"response": response})
