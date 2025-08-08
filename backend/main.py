import io
import uuid
import urllib.parse
from pathlib import Path
from PIL import Image
from fastapi import FastAPI, File, Response, UploadFile, Form, HTTPException
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
async def upload_image(
    file: UploadFile = File(...),
    outline_thickness: int = Form(...),
    detail: int = Form(...),
    outline_color: str = Form(...)
    ):
    # Read with a hard cap so we don’t blow memory
    content = await file.read(MAX_FILE_SIZE + 1)
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB")

    # Basic content-type guard
    if not (file.content_type and file.content_type.startswith("image/")):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Decode image
        image_stream = io.BytesIO(content)
        input_image = Image.open(image_stream)

        # Process
        processor = ImageProcessor(
            background_color=hex_to_rgb(outline_color),
            detail=detail,
            outline_thickness=outline_thickness
        )
        processed_image = processor.process_PIL_image(input_image)
        if processed_image is None:
            raise RuntimeError("Failed to process image")

        # Encode PNG to bytes
        output_stream = io.BytesIO()
        processed_image.save(output_stream, format="PNG")
        image_bytes = output_stream.getvalue()

        # Build a nice filename (fallback-safe, UTF-8 encoded)
        base = Path(file.filename or f"upload-{uuid.uuid4().hex}").stem
        out_name = f"{base}-cutout.png"
        out_name_quoted = urllib.parse.quote(out_name)

        return Response(
            content=image_bytes,
            media_type="image/png",
            headers={
                # Use attachment to strongly hint “download” semantics
                "Content-Disposition": f'attachment; filename="{out_name}"; filename*=UTF-8\'\'{out_name_quoted}',
                "Content-Length": str(len(image_bytes)),
                "X-Original-Size": f"{processed_image.size[0]}x{processed_image.size[1]}",
                "X-File-Size": str(len(image_bytes)),
                # Optional, helps with dev caching behavior
                "Cache-Control": "no-store",
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail="Failed to process image. Please try again.")


@app.post("/api/process")
async def process_image():
    pass

@app.post("/api/download/{filename}")
async def download_result(filename: str):
    pass

@app.get("/api/preview/{filename}")
async def preview_image(filename: str):
    pass