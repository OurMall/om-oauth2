from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

def create_application() -> FastAPI:
    
    app = FastAPI(
        debug=True,
        title="Our Mall - Authorization Server",
        description="""
            Server for clients or third part applications authorization, this server issued
            scopes to the register clients.
        """,
        version="v0.6.0",
        contact={
            "name": "Brian Castro",
            "url": "https://brian-space.herokuapp.com/",
            "email": "bcastro421@misena.edu.co"
        }
    )
    
    app.mount(
        path="/static", 
        app=StaticFiles(directory="app/static", check_dir=True), 
        name="static"
    )
    
    return app