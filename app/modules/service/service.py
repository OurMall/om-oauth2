from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi.responses import Response, JSONResponse

from app.common import Service
from app.common.dependencies import user, security
from app.common.models.service_model import ServiceCreate, ServiceModel

router = APIRouter(
    prefix="/service"
)

@router.get("/", response_model=list[ServiceModel], status_code=200)
async def services(
    sort: str | None = Query("name", title="Order", description="Service order method"),
    limit: int | None = Query(None, title="Limit", description="Services limit"),
    skip: int | None = Query(None, title="Skip", description="Services skip")
) -> Response | HTTPException:
    try:
        services: list[Service] = await Service.find_all(
            skip=skip,
            limit=limit,
            sort=sort
        ).project(ServiceModel).to_list()
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
        return services

@router.get("/{id}", response_model=ServiceModel, status_code=200)
async def service(
    id: str = Path(..., title="ID", description="Service ID for finding")
) -> Response | HTTPException:
    try:
        service: Service = await Service.find_one(
            Service.id == id
        ).project(ServiceModel)
    except:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "fail",
                "response": {
                    "message": "Service not found"
                }
            }
        )
    else:
        return JSONResponse(
            content={
                "status": "success",
                "response": {
                    "service": service
                }
            },
            status_code=200
        )

@router.post("/", response_model=None, status_code=201, dependencies=[
    Depends(security.verify),
    Depends(user.has_groups("admin")),
    Depends(user.has_permissions("services"))
])
async def create_service(
    service: ServiceCreate
) -> Response | HTTPException:
    existented_service = await Service.find(
        Service.code_name == service.code_name
    ).first_or_none()
    if not existented_service:
        try:
            new_service = Service(
                code_name=service.code_name,
                name=service.name,
                description=service.description,
                activate=service.activate
            )
            await Service.insert_one(new_service)
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
                        "message": "Service was created"
                    }
                },
                status_code=201
            )
    raise HTTPException(
        status_code=400,
        detail={
            "status": "fail",
            "response": {
                "message": "Service exists"
            }
        }
    )