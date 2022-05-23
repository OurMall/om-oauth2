from fastapi import APIRouter, Response, HTTPException, Depends, Query, Path
from fastapi.responses import JSONResponse

from app.common import Category
from app.common.dependencies import jwt, user, security
from app.common.models.category_model import CategoryCreate, CategoryModel

router = APIRouter(
    prefix="/category",
)

@router.get("/", response_model=list[CategoryModel], status_code=200)
async def categories(
    limit: int | None = Query(None, title="Limit", description="Categories limit"),
    sort: str | None = Query("name", title="Order", description="Categories order method"),
    skip: int | None = Query(None, title="Skip", description="Categories skipper"),
) -> Response:
    try:
        categories: list[Category] = await Category.find_all(
            skip=skip,
            limit=limit,
            sort=sort
        ).project(CategoryModel).to_list()
    except:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "fail",
                "response": {
                    "message": "We can't found categories"
                }
            }
        )
    else:
        return categories

@router.get("/{id}", response_model=CategoryModel, status_code=200)
async def category(
    id: str = Path(..., title="ID", description="Category ID for finding")
) -> Response:
    try:
        category: Category = await Category.find_one(Category.id == id).project(CategoryModel)
    except:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "fail",
                "response": {
                    "message": "Category not found"
                }
            }
        )
    else:
        return JSONResponse(
            content={
                "status": "success",
                "response": {
                    "category": category
                }
            }
        )

@router.post("/", response_model=None, status_code=201, dependencies=[
    Depends(user.has_groups("seller"))
])
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