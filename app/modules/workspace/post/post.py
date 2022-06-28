from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Response, HTTPException

from app.core import HttpResponse
from app.common import Post, Workspace, User
from app.common.dependencies import security, user
from app.common.models.post_model import PostCreate
from app.common.models.response_model import SuccessResponseModel

router = APIRouter(
    prefix="/post"
)

@router.post("/", response_model=SuccessResponseModel, status_code=201, dependencies=[
    Depends(security.verify),
    Depends(user.has_groups("seller"))
])
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(user.get_user(
        current=True,
        fetch_links=True,
        ignore_cache=True
    ))
) -> Response | HTTPException:
    try:
        workspace_id = PydanticObjectId(post_data.workspace)
        if user.is_owner(user=current_user, workspace=workspace_id):
            new_post = Post(**post_data.dict())
            await Post.insert_one(new_post)
            workspace = await Workspace.get(
                document_id=workspace_id,
                fetch_links=True,
                ignore_cache=True
            )
            workspace.posts.append(new_post)
            await workspace.save_changes(
                ignore_revision=True
            )
        else:
            raise HTTPException(
                status_code=403,
                detail={
                    "status": "fail",
                    "response": {
                        "message": "User is not workspace owner"
                    }
                }
            )
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
                    "message": "Post created"
                }
            }
        ).response()