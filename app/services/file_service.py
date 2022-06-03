import boto3

class FileService:
    
    __allowed_extensions__: list[str] = ["png", "svg", "jpg", "jpeg"]
    
    def __init__(self) -> None:
        self.s3_client = boto3.resource('s3')
    
    async def upload(
        self,
        files: list[bytes]
    ):
        if isinstance(files, bytes):
            files = [files]
        try:
            bucket = self.s3_client.Bucket('our-mall-storage')
            for file in files:
                pass
        except:
            pass
        else:
            pass
    
    async def download(
        self
    ):
        pass