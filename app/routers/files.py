from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
router = APIRouter()

fake_files_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


class File(BaseModel):
    name: str
    format: str
    email: str


@router.get("/")
async def read_files():
    return fake_files_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_files_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_files_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
