from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import UserCreate, UserUpdate, UserResponse, UserList, DeleteResponse
from app.service import create_new_user, fetch_users, fetch_user_by_id, update_user_info, remove_user
import logging

logger = logging.getLogger(__name__)

user_router = APIRouter()

@user_router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user with the provided information"""
    try:
        return create_new_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"[create_user] Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the user")

@user_router.get("/", response_model=UserList)
def get_all_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of users to return"),
    db: Session = Depends(get_db)
):
    """Retrieve a list of users with pagination"""
    try:
        users, count = fetch_users(db, skip, limit)
        return {"users": users, "count": count}
    except Exception as e:
        logger.error(f"[get_all_users] Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching users")

@user_router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int = Path(..., gt=0, description="The ID of the user to get"),
    db: Session = Depends(get_db)
):
    """Retrieve a specific user by ID"""
    try:
        user = fetch_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[get_user] Error fetching user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the user")

def _update_user(user_update: UserUpdate, user_id: int, db: Session):
    """Helper function to update user information"""
    updates = user_update.dict(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="At least one field must be provided for update")

    updated_user = update_user_info(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    return updated_user

@user_router.put("/{user_id}", response_model=UserResponse)
@user_router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_update: UserUpdate,
    user_id: int = Path(..., gt=0, description="The ID of the user to update"),
    db: Session = Depends(get_db)
):
    """Update or partially update a user's information"""
    try:
        return _update_user(user_update, user_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[update_user] Error updating user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the user")

@user_router.delete("/{user_id}", response_model=DeleteResponse)
def delete_user(
    user_id: int = Path(..., gt=0, description="The ID of the user to delete"),
    db: Session = Depends(get_db)
):
    """Delete a user"""
    try:
        success = remove_user(db, user_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        return {"message": f"User with ID {user_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[delete_user] Error deleting user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the user")
