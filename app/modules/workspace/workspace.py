from beanie.operators import In
from fastapi import APIRouter, Response, Depends, Query, Path, HTTPException
from fastapi.responses import JSONResponse

from app.common import User, Workspace, WorkspaceProfile, Category, Service
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
    id: str = Path(...)
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
    workspace: WorkspaceCreate,
    owner: User = Depends(user.get_user(current=True, fetch_links=True, ignore_cache=True))
) -> Response:
    existented_workspace = await Workspace.find(
        Workspace.profile.name == workspace.profile.name
    ).first_or_none()
    if not existented_workspace:
        if len(owner.workspaces) > 1:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "fail",
                    "response": {
                        "message": "Already you have a workspace"
                    }
                }
            )
        try:
            category: Category = await Category.find_one(Category.code_name == workspace.category.code_name)
            services: list[Service] = await Service.find(
                In(Service.code_name, workspace.services)
            ).to_list()
            new_workspace = Workspace(
                category=category,
                profile=WorkspaceProfile(
                    name=workspace.profile.name,
                    description=workspace.profile.description,
                    slogan=workspace.profile.slogan,
                    logo=workspace.profile.logo,
                ),
                services=services,
                tags=workspace.tags
            )
            await Workspace.insert_one(new_workspace)
            owner.workspaces.append(new_workspace)
            await owner.save()
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "fail",
                    "response": {
                        "message": "Something went wrong",
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