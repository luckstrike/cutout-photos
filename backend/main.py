from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Paper Cutout API", version="1.0.0")

# Enable CORS
#app.add_middleware(
#    CORSMiddleware,
#    allow_origin=["http://localhost:5173"], # Svelte dev server
#    allow_credential=True,
#    allow_methods=["*"],
#    allow_headers=["*"]
#)

@app.get("/")
async def root():
    return {"message": "Paper Cutout API", "docs": "/docs"}

@app.post("/api/upload")
async def upload_image(file: UploadFile):
    pass

@app.post("/api/process")
async def process_image():
    pass

@app.post("/api/download/{filename}")
async def download_result(filename: str):
    pass

@app.get("/api/preview/{filename}")
async def preview_image(filename: str):
    pass