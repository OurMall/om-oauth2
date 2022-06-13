from beanie import PydanticObjectId
from fastapi import APIRouter, Response, HTTPException, Depends, Query, Path
from fastapi.responses import JSONResponse

from app.common import Category
from app.common.dependencies import user, security
from app.common.models.category_model import CategoryCreate, CategoryModel
from app.common.models.response_model import SuccessResponseModel
from app.core.http import HttpResponse

router = APIRouter(
    prefix="/category",
)

@router.get("/", response_model=SuccessResponseModel, status_code=200)
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
        ).to_list()
        categories_response: list[CategoryModel] = [CategoryModel(**category.dict()) for category in categories]
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
        return HttpResponse(
            status_code=200,
            body=categories_response
        ).response()

@router.get("/{id}", response_model=CategoryModel, status_code=200)
async def category(
    id: str = Path(..., title="ID", description="Category ID for finding")
) -> Response | HTTPException:
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

@router.post("/", response_model=SuccessResponseModel, status_code=201, dependencies=[
    Depends(security.verify),
    Depends(user.verify_account),
    Depends(user.has_groups("admin")),
    Depends(user.has_permissions("categories"))
])
async def create_category(
    category: CategoryCreate,
) -> Response | HTTPException:
    try:
        new_category = Category(
            code_name=category.code_name,
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
                    "message": "Something went wrong"
                }
            }
        )
    else:
        return HttpResponse(
            status_code=201,
            body={
                "status": "success",
                "response": {
                    "message": "Created"
                }
            }
        ).response()

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

@router.delete("/{id}", response_model=None, status_code=204, dependencies=[
    Depends(security.verify),
    Depends(user.verify_account),
    Depends(user.has_groups("admin")),
    Depends(user.has_permissions("categories"))
])
async def delete_category(
    id: str = Path(..., title="ID", description="Category unique identifier")
) -> Response | HTTPException:
    try:
        if isinstance(id, str):
            id = PydanticObjectId(id)
        category = await Category.find_one(Category.id == id)
        await category.delete()
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
            status_code=204,
            body={
                "status": "success",
                "response": {
                    "message": "Deleted"
                }
            }
        ).response()