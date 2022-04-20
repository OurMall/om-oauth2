from fastapi import APIRouter

router = APIRouter(
    prefix="/oauth",
    tags=["Authentication"]
)

@router.post("/login", response_model=None, status_code=200)
async def login():
    pass

@router.post("/signup", response_model=None, status_code=200)
async def signup():
    pass

@router.post("/token")
async def token():
    pass