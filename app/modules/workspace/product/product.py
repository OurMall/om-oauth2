from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Response, HTTPException, Path

from app.core import HttpResponse
from app.common import Product, Workspace
from app.common.models.product_model import ProductCreate, ProductModel

router = APIRouter(
    prefix="/product"
)

@router.get("/", response_model=None, status_code=200)
async def products(

) -> Response | HTTPException:
    pass

@router.get("/{id}", response_model=None, status_code=200)
async def product(
    id: str = Path(..., title="ID", description="Unique product identifier")
) -> Response | HTTPException:
    pass

@router.post("/", response_model=None, status_code=201)
async def create_product(
    product_data: ProductCreate = Body(...)
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
        await product_workspace.save()
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
                "status": "sucess",
                "response": {
                    "message": "Product created"
                }
            }
        )

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