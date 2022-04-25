from fastapi import APIRouter

router = APIRouter(
    prefix="/authentication",
)

@router.post("/login", response_model=None, status_code=200)
async def login():
    pass

@router.post("/signup", response_model=None, status_code=200)
async def signup():
    pass
