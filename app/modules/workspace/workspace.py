from beanie import WriteRules
from fastapi import APIRouter, Response, Depends, Query, Path, HTTPException
from fastapi.responses import JSONResponse

from app.common import Workspace, WorkspaceProfile, Category
from app.common.dependencies import jwt, user, security
from app.common.models.workspace_model import WorkspaceCreate, WorkspaceModel

router = APIRouter(
    prefix="/workspace",
)

@router.get("/", response_model=list[WorkspaceModel], status_code=200)
async def workspaces(
    sort: str | None = Query("created_at", title="Order", description="Workspaces order method"),
    limit: int | None = Query(None, title="Limit", description="Workspaces limit"),
    skip: int | None = Query(None, title="Skip", description="Workspace skip"),
) -> Response:
    try:
        workspaces: list[Workspace] = await Workspace.find_all(
            skip=skip,
            limit=limit,
            sort=sort
        ).project(WorkspaceModel).to_list()
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
        return JSONResponse(
            content={
                "status": "success",
                "response": {
                    "workspaces": workspaces
                }
            }
        )

@router.get("/{id}", response_model=WorkspaceModel, status_code=200)
async def workspace(
    id: str
) -> Response:
    try:
        workspace: Workspace = await Workspace.find_one(
            Workspace.id == id
        ).project(WorkspaceModel)
    except:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "fail",
                "response": {
                    "message": "Workspace not found"
                }
            }
        )
    else:
        return JSONResponse(
            content={
                "status": "success",
                "response": {
                    "workspace": workspace
                }
            }
        )

@router.post("/", response_model=None, status_code=201, dependencies=[
    Depends(security.verify),
    Depends(user.has_groups("seller"))
])
async def create_workspace(
    workspace: WorkspaceCreate
) -> Response:
    existented_workspace = await Workspace.find(
        Workspace.profile.name == workspace.profile.name
    ).first_or_none()
    if not existented_workspace:
        category = await Category.find_one(Category.id == workspace.category)
        try:
            new_workspace = Workspace(
                category=category,
                profile=WorkspaceProfile(
                    name=workspace.profile.name,
                    description=workspace.profile.description,
                    slogan=workspace.profile.slogan,
                    logo=workspace.profile.logo,
                ),
                services=workspace.services,
                tags=workspace.tags
            )
            await Workspace.insert_one(new_workspace, link_rule=WriteRules.WRITE)
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
            return JSONResponse(
                content={
                    "status": "success",
                    "response": {
                        "message": "workspace was created"
                    }
                },
                status_code=201
            )
    raise HTTPException(
        status_code=400,
        detail={
            "status": "fail",
            "response": {
                "message": "Workspace already exists"
            }
        }
    )


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