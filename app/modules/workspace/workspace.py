from fastapi import APIRouter, Response, Depends

from app.common.dependencies import jwt, user, security

from .category import category

router = APIRouter(
    prefix="/workspace",
    tags=["Workspaces"],
    dependencies=[
        #Depends(security.verify),
        #Depends(user.has_groups("seller"))
    ]
)

router.include_router(
    router=category.router,
    tags=["Categories"]
)

@router.get("/", response_model=None, status_code=200)
async def workspaces() -> Response:
    pass

@router.get("/{id}", response_model=None, status_code=200)
async def workspace(
    id: str
) -> Response:
    pass

@router.post("/", response_model=None, status_code=201)
async def create_workspace() -> Response:
    pass

@router.patch("/{id}", response_model=None, status_code=201)
async def edit_workspace(
    id: str
) -> Response:
    pass

@router.put("/{id}", response_model=None, status_code=201)
async def update_workspace(
    id: str
) -> Response:
    pass

@router.delete("/{id}", response_model=None, status_code=204)
async def delete_workspace(
    id: str
) -> Response:
    pass