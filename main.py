# main.py
from fastapi import FastAPI
from routers import hls_routes,media_info,thumbnails

app = FastAPI()
app.include_router(media_info.router)
app.include_router(hls_routes.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World"}

