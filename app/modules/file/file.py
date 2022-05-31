from fastapi import APIRouter, UploadFile, File

router = APIRouter(
    prefix="/file"
)

@router.post("/upload", response_model=None, status_code=201)
async def upload(
    files: list[UploadFile] | UploadFile = File(..., title="File", description="Files list to upload")
):
    if isinstance(files, (UploadFile)):
        files = [files]
    pass

@router.post("/download", response_model=None, status_code=200)
async def download():
    pass