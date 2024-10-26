from fastapi import APIRouter, HTTPException
from typing import List
from app.models.users import User, UserCreate, UserUpdate
from app.db.connectors import get_user_collection
from app.utils.logger import logger
from bson.objectid import ObjectId
from pydantic import ValidationError

router = APIRouter()


@router.post("/users", response_model=User)
async def create_user(user_create: UserCreate):
    collection = get_user_collection()
    user_dict = user_create.model_dump()
    result = await collection.insert_one(user_dict)
    user = await collection.find_one({"_id": result.inserted_id})
    logger.info(f"User created with id {result.inserted_id}")
    if user:
        try:
            user_model = User.model_validate(user)
            return user_model
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=500, detail="User creation failed")


@router.get("/users", response_model=List[User])
async def list_users():
    collection = get_user_collection()
    users = await collection.find().to_list(100)
    return [User.model_validate(user) for user in users]


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    collection = get_user_collection()
    try:
        user = await collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    if user:
        return User.model_validate(user)
    raise HTTPException(status_code=404, detail="User not found")


@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user_update: UserUpdate):
    collection = get_user_collection()
    try:
        update_result = await collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": user_update.model_dump(exclude_unset=True)}
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return User.model_validate(user)
    raise HTTPException(status_code=404, detail="User not found after update")


@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    collection = get_user_collection()
    try:
        delete_result = await collection.delete_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    if delete_result.deleted_count:
        logger.info(f"User deleted with id {user_id}")
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="User not found")
