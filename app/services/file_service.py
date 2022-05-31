from boto3 import client

class FileService:
    
    __allowed_extensions__: list[str] = ["png", "svg", "jpg", "jpeg"]
    
    def __init__(self) -> None:
        self.s3_client = client('s3')
    
    async def upload(
        self
    ):
        try:
            pass
        except:
            pass
        else:
            pass
    
    async def download(
        self
    ):
        pass