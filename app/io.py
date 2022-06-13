from socketio import AsyncServer

from .namespaces import NotificationNamespace, WorkspaceNamespace

def create_sio() -> AsyncServer:
    
    sio = AsyncServer(
        logger=True,
        always_connect=True,
        async_mode="asgi",
        ping_interval=100000,
        ping_timeout=50000,
        #cookie="",
        cors_allowed_origins="*",
        cors_credentials=True
    )
    
    sio.register_namespace(
        namespace_handler=NotificationNamespace(
            namespace="/notification"
        )
    )

    sio.register_namespace(
        namespace_handler=WorkspaceNamespace(
            namespace="/workspace"
        )
    )
    
    return sio