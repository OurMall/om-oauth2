import boto3
from fastapi import Response, UploadFile, HTTPException

class FileService:
    
    __allowed_extensions__: list[str] = ["png", "svg", "jpg", "jpeg"]
    
    def __init__(self) -> None:
        self._s3_client = boto3.resource('s3')
    
    def __is_allowed_file__(self, filename: str) -> bool:
        return filename.split('.')[1] in self.__allowed_extensions__
    
    async def upload(
        self,
        files: list[UploadFile] | UploadFile | bytes
    ) -> Response | HTTPException:
        if isinstance(files, (bytes)):
            files = [UploadFile(**file) for file in files]
        try:
            bucket = self._s3_client.Bucket('our-mall-storage')
            for file in files:
                if self.__is_allowed_file__(file.filename):
                    response = bucket.upload_file(file.file, file.filename)
                else:
                    response = None
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
            return response
    
    async def download(
        self
    ):
        pass