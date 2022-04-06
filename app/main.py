from .app import create_application

app = create_application()

@app.on_event('startup')
async def on_startup():
    print("Server is starting...")

@app.on_event('shuwtdown')
async def on_shutdown():
    print("Shutdown application")