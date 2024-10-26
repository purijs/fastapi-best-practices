from fastapi import APIRouter, HTTPException
from typing import List
from app.models.user import User, UserCreate, UserUpdate
from app.db.connectors import get_user_collection
from app.utils.logger import logger
from bson.objectid import ObjectId

router = APIRouter()

@router.post("/users", response_model=User)
async def create_user(user_create: UserCreate):
    collection = get_user_collection()
    user_dict = user_create.dict()
    result = await collection.insert_one(user_dict)
    user = await collection.find_one({"_id": result.inserted_id})
    logger.info(f"User created with id {result.inserted_id}")
    return User(**user)

@router.get("/users", response_model=List[User])
async def list_users():
    collection = get_user_collection()
    users = await collection.find().to_list(100)
    return [User(**user) for user in users]

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    collection = get_user_collection()
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(**user)
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user_update: UserUpdate):
    collection = get_user_collection()
    await collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user_update.dict(exclude_unset=True)}
    )
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(**user)
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    collection = get_user_collection()
    result = await collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count:
        logger.info(f"User deleted with id {user_id}")
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="User not found")
