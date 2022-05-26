from socketio import AsyncNamespace


class NotificationNamespace(AsyncNamespace):
    
    def __init__(self, namespace: str = None):
        super().__init__(namespace)
    
    async def on_connect(
        self,
        sid: str,
        environ: dict[str, object]
    ):
        print("new connection #{0}".format(sid))
        print(environ)
        pass
    
    async def on_disconnect(
        self, 
        sid: str
    ):
        print("disconnected #{0}".format(sid))