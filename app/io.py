from socketio import AsyncServer

def create_sio() -> AsyncServer:
    sio = AsyncServer(
        logger=True,
        always_connect=True,
        async_mode="asgi",
        ping_interval=100000,
        ping_timeout=50000,
        cookie="",
        cors_allowed_origins=["*"],
        cors_credentials=True
    )
    
    return sio