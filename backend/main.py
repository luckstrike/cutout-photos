import io
import uuid
from PIL import Image
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.processor import ImageProcessor
from core.utils import hex_to_rgb

app = FastAPI(title="Paper Cutout API", version="1.0.0")

MAX_FILE_SIZE = 10 * 1024 * 1024;

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Svelte dev server
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Paper Cutout API", "docs": "/docs"}

@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...), 
                        outline_thickness: int = Form(...), 
                        detail: int = Form(...),
                        outline_color: str = Form(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File too large. Maximum size is 10MB"
        )
    
    content = await file.read()

    image_stream = io.BytesIO(content)

    input_image = Image.open(image_stream)

    try:
        # Create processor with selected settings
        processor = ImageProcessor(
            background_color=hex_to_rgb(outline_color),
            detail=detail,
            outline_thickness=outline_thickness
        )

        random_id = str(uuid.uuid4())
        output_path = "output/" + random_id + "_processed.png"

        success = processor.process_image(image_stream, output_path)
    except Exception as e:
        # Log the error for debugging
        print(f"Error processing image: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Failed to process image. Please try again."
        )


    return {
        "filename": output_path,
        "format": input_image.format,
        "size": input_image.size,
        "mode": input_image.mode,
        "file_size_bytes": len(content)
    }

@app.post("/api/process")
async def process_image():
    pass

@app.post("/api/download/{filename}")
async def download_result(filename: str):
    pass

@app.get("/api/preview/{filename}")
async def preview_image(filename: str):
    pass