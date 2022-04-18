from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

def create_application() -> FastAPI:
    app = FastAPI(
        debug=True,
        title="Our Mall - OAuth2",
        description="""
            Servidor de autorizacion del proyecto Our Mall
        """,
        version="v0.1.0",
        contact=dict(
            email="yitocode@gmail.com",
            phone_number="+573003606702"
        )
    )
    
    app.mount("/static", StaticFiles(directory="static", check_dir=True), name="static")
    
    app.add_middleware(
        CORSMiddleware,
           
    )
    
    return app