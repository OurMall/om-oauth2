from beanie import PydanticObjectId
from socketio import AsyncNamespace

from app.common import Workspace, User
from app.common.models.workspace_model import WorkspaceModel

class WorkspaceNamespace(AsyncNamespace):
    
    def __init__(self, namespace: str=None):
        super().__init__(namespace)
        self.connected_clients: list[str] = []
        self.workspaces: dict[str] = dict()
    
    async def on_connect(
        self, 
        sid: str, 
        environ: dict,
    ):
        if not sid in self.connected_clients:
            return await self.on_connect_workspace(sid=sid, environ=environ)
        return await self.emit(
            event="already_connected",
            data={
                "status": "fail",
                "response": {
                    "message": "User already connected"
                }
            },
            to=sid
        )
    
    async def on_connect_workspace(
        self,
        sid: str,
        environ: dict
    ):
        async with self.session(sid=sid) as session:
            session['USER_PLATFORM'] = environ['HTTP_SEC_CH_UA_PLATFORM']
        self.connected_clients.append(sid)
        return await self.emit(
            event="connected",
            data={
                "status": "success",
                "response": {
                    "message": "User connected"
                }
            },
            to=sid
        )
    
    async def on_join_workspace(self, sid: str, data: dict):
        try:
            workspace = await Workspace.get(
                document_id=data['workspace'],
                ignore_cache=True
            )
            if not workspace:
                return await self.emit(
                    event="nonexistent_workspace",
                    data={
                        "status": "fail",
                        "response": {
                            "message": "Workspace doesn't exists"
                        }
                    },
                    to=sid
                )
            workspace_response = WorkspaceModel(**workspace.dict())
            self.enter_room(
                sid=sid,
                room=workspace_response.id
            )
        except:
            return await self.emit(
                event="workspace_error",
                data={
                    "status": "fail",
                    "response": {
                        "message": "Something went wrong"
                    }
                },
                to=sid
            )
        else:
            return await self.emit(
                event="joined",
                data={
                    "status": "success",
                    "response": {
                        "message": "User joined into workspace {0}".format(workspace_response.id),
                        "workspace": workspace_response.dict(
                            exclude={"id", "created_at", "updated_at"}
                        ),
                    }
                },
                room=workspace_response.id
            )
    
    async def on_subscribe_workspace(self, sid: str, data: dict):
        try:
            if not data.get('user'):
                return await self.emit(
                    event="not_token",
                    data={
                        "status": "fail",
                        "response": {
                            "message": "User not logged in"
                        }
                    }
                )
            if isinstance(data['user'], str):
                data['user'] = PydanticObjectId(data['user'])
            user: User = await User.get(
                document_id=data['user'],
                fetch_links=True,
                ignore_cache=True
            )
            if not user:
                return await self.emit(
                    event="workspace_error",
                    data={
                        "status": "fail",
                        "response": {
                            "message": "User not found"
                        }
                    }
                )
            workspace: Workspace = await Workspace.get(
                document_id=data['workspace'],
                fetch_links=True,
                ignore_cache=True
            )
            if user.email in workspace.suscribers:
                return await self.emit(
                    event="already_subscribed",
                    data={
                        "status": "fail",
                        "data": {
                            "message": "User already suscribed"
                        }
                    }
                )
            workspace.suscribers.append(user.email)
            await workspace.save(
                ignore_revision=True
            )
        except:
            return await self.emit(
                event="workspace_error",
                data={
                    "status": "fail",
                    "response": {
                        "message": "Something went wrong"
                    }
                }
            )
        else:
            return await self.emit(
                event="subscribed",
                data={
                    "status": "success",
                    "response": {
                        "message": "User suscribed"
                    }
                }
            )
    
    async def on_workspace_subscribers(self, sid: str, data: dict):
        pass
    
    async def on_is_subscribed_workspace(self, sid: str, data: dict):
        try:
            user = await User.get(
                document_id=data['user'],
            )
            workspace = await Workspace.get(
                document_id=data['workspace']
            )
            if user.email in workspace.suscribers:
                return await self.emit(
                    event="subscription_status",
                    data={
                        "status": "success",
                        "response": {
                            "subscribed": True
                        }
                    }
                )
            else:
                return await self.emit(
                    event="subscription_status",
                    data={
                        "status": "fail",
                        "response": {
                            "subscribed": False
                        }
                    }
                )
        except:
            return await self.emit(
                event="workspace_error",
                data={
                    "status": "fail",
                    "response": {
                        "message": "something went wrong"
                    }
                }
            )

    async def on_unsubscribe_workspace(self, sid: str):
        pass
    
    async def on_leave_workspace(self, sid: str, data: dict):
        try:
            workspace = await Workspace.get(
                document_id=data['workspace'],
                ignore_cache=True
            )
            if not workspace:
                return await self.emit(
                    event="nonexistent_workspace",
                    data={
                        "status": "fail",
                        "response": {
                            "message": "Workspace doesn't exists"
                        }
                    },
                    to=sid
                )
            workspace_response = WorkspaceModel(**workspace.dict())
            self.leave_room(
                sid=sid,
                room=workspace_response.id
            )
        except:
            return await self.emit(
                event="workspace_error",
                data={
                    "status": "fail",
                    "response": {
                        "message": "Something went wrong"
                    }
                },
                to=sid
            )
        else:
            await self.emit(
                event="left",
                data={
                    "status": "success",
                    "response": {
                        "message": "User was left"
                    }
                },
                to=sid
            )
            return await self.on_disconnect(sid=sid)

    async def on_disconnect(self, sid: str):
        try:
            self.connected_clients.remove(sid)
        except:
            pass