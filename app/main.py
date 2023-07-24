from fastapi import FastAPI

from .internal import admin
from .routers import files, users

app = FastAPI()


app.include_router(users.router,
                   prefix="/users",
                   tags=["users"])
app.include_router(files.router,
                   prefix="/files",
                   tags=["files"])
app.include_router(admin.router,
                   prefix="/admin",
                   tags=["admin"])


@app.get("/")
async def root():
    return {"message": "API corriendo correctamente."}
