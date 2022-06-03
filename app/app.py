from fastapi import FastAPI

def create_application() -> FastAPI:
    
    app = FastAPI(
        debug=True,
        title="Our Mall - Authorization Server",
        description="""
            Server for clients or third part applications authorization, this server issued
            scopes to the register clients.
        """,
        version="v0.8.0",
        contact={
            "name": "Brian Castro",
            "url": "https://brian-space.herokuapp.com/",
            "email": "bcastro421@misena.edu.co"
        }
    )
    
    return app