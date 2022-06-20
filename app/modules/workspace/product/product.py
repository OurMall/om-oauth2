from beanie import PydanticObjectId, WriteRules
from fastapi import APIRouter, Body, Depends, Query, Response, HTTPException, Path

from app.core import HttpResponse
from app.common import Product, Workspace
from app.common.schemas import Price
from app.common.dependencies import security, user
from app.common.models.product_model import ProductCreate, ProductModel
from app.common.models.response_model import SuccessResponseModel

router = APIRouter(
    prefix="/product"
)

@router.get("/", response_model=None, status_code=200)
async def products(
    workspace: str = Query(None, title="Products Workspace", description="Products from workspace"),
) -> Response | HTTPException:
    return {"hello": "world"}

@router.get("/{id}", response_model=None, status_code=200)
async def product(
    id: str = Path(..., title="ID", description="Unique product identifier")
) -> Response | HTTPException:
    pass

@router.post("/", response_model=SuccessResponseModel, status_code=201, dependencies=[
    Depends(security.verify),
    Depends(user.has_groups("seller"))
])
async def create_product(
    product_data: ProductCreate
):
    if isinstance(product_data.workspace, str):
        workspace = PydanticObjectId(product_data.workspace)
    else:
        workspace = product_data.workspace
    try:
        new_product: Product = Product(**product_data.dict())
        await Product.insert_one(new_product)
        product_workspace: Workspace = await Workspace.get(
            document_id=workspace,
            ignore_cache=True,
            fetch_links=True
        )
        product_workspace.products.append(new_product)
        await product_workspace.save(link_rule=WriteRules.WRITE, ignore_revision=True)
    except Exception:
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
                "status": "sucess",
                "response": {
                    "message": "Product created"
                }
            }
        ).response()

@router.put("/{id}", response_model=None, status_code=201)
async def update_product(
    id: str = Path(..., title="ID", description="Unique product identifier")
) -> Response | HTTPException:
    pass

@router.patch("/{id}", response_model=None, status_code=201)
async def edit_product(
    id: str = Path(..., title="ID", description="Unique product identifier")
) -> Response | HTTPException:
    pass

@router.delete("/{id}", response_model=None, status_code=201)
async def delete_product(
    id: str = Path(..., title="ID", description="Unique product identifier")
) -> Response | HTTPException:
    pass