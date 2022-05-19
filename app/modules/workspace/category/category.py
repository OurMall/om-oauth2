from fastapi import APIRouter, Response, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.common import Category
from app.common.dependencies import jwt, user, security
from app.common.models.category_model import CategoryCreate, CategoryModel

router = APIRouter(
    prefix="/category",
    dependencies=[
        #Depends(security.verify),
        #Depends(user.has_groups("client"))
    ]
)

@router.get("/", response_model=None, status_code=200)
async def categories() -> Response:
    pass

@router.get("/{id}", response_model=None, status_code=200)
async def category(
    id: str
) -> Response:
    pass

@router.post("/", response_model=CategoryModel, status_code=201, dependencies=[Depends(user.has_groups("admin")), Depends(user.has_permissions("categories"))])
async def create_category(
    category: CategoryCreate,
) -> Response:
    try:
        new_category = Category(
            name=category.name,
            description=category.description
        )
        await Category.insert_one(new_category)
    except:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "fail",
                "response": {
                    "message": "An error was ocurred"
                }
            }
        )
    else:
        return JSONResponse(
            content={
                "status": "success",
                "response": {
                    "message": "Category created"
                }
            },
            status_code=201
        )

@router.patch("/{id}", response_model=None, status_code=201)
async def edit_category(
    id: str
) -> Response:
    pass

@router.put("/{id}", response_model=None, status_code=201)
async def update_category(
    id: str
) -> Response:
    pass

@router.delete("/{id}", response_model=None, status_code=204)
async def delete_category(
    id: str
) -> Response:
    pass