from fastapi import APIRouter, HTTPException, UploadFile, File
from app.core.http import HttpResponse

from app.services import FileService
from app.common.models.response_model import SuccessResponseModel

router = APIRouter(
    prefix="/file"
)

file_service = FileService()

@router.post("/upload", response_model=SuccessResponseModel, status_code=201)
async def upload(
    files: list[UploadFile] | UploadFile = File(..., title="File", description="Files list to upload")
):
    if isinstance(files, (UploadFile)):
        files = [files]
    try:
        response = await file_service.upload(
            files=files
        )
        if not response:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "fail",
                    "response": {
                        "message": "Not allowed file"
                    }
                }
            )
    except:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "fail",
                "response": {
                    "message": "Something went wrong"
                }
            }
        )
    else:
        return HttpResponse(
            status_code=201,
            body=response
        ).response()

@router.post("/download", response_model=None, status_code=200)
async def download():
    pass