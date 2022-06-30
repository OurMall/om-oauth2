from fastapi import APIRouter, HTTPException, Query
from beanie import operators as op

from app.core import HttpResponse
from app.common import Product, Workspace
from app.common.models.product_model import ProductModel
from app.common.models.workspace_model import WorkspaceModel
from app.common.models.response_model import SuccessResponseModel

router = APIRouter(
    prefix="/search"
)

@router.get("/", response_model=SuccessResponseModel, status_code=200)
async def search_engine(
    query: str = Query(..., title="Query", description="Keywords for search in the database"),
    limit: int = Query(5, title="Limit", description="Limit for results in the query")
):
    try:
        query = query.lower().strip()
        products: list[Product] = await Product.find(
            op.RegEx(
                field=Product.name,
                pattern=f"{query}",
                options="si",
            ),
            fetch_links=True,
            ignore_cache=True
        ).to_list(
            length=limit
        )
        products_response: list[ProductModel] = [ProductModel(**product.dict()) for product in products]
        workspaces: list[Workspace] = await Workspace.find(
            op.RegEx(
                field=Workspace.profile.name,
                pattern=f"{query}",
                options="si"
            ),
            fetch_links=True,
            ignore_cache=True
        ).to_list(
            length=limit
        )
        workspaces_response: list[WorkspaceModel] = [WorkspaceModel(**workspace.dict()) for workspace in workspaces]
    except Exception as e:
        print(e)
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
            status_code=200,
            body={
                "status": "success",
                "response": {
                    "products": products_response,
                    "workspaces": workspaces_response
                }
            }
        ).response()