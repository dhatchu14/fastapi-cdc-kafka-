from sqlalchemy.orm import Session
from app.repository import (
    create_user, get_users, get_user_by_id, 
    get_user_by_email, update_user, delete_user
)
from app.schemas import UserCreate, UserUpdate
import logging

logger = logging.getLogger(__name__)

def create_new_user(db: Session, user_data: UserCreate):
    """Service function to create a new user"""
    logger.info(f"Creating new user with email: {user_data.email}")
    
    # Check if user with email already exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        logger.warning(f"User with email {user_data.email} already exists")
        raise ValueError(f"User with email '{user_data.email}' already exists")
        
    return create_user(db, user_data)

def fetch_users(db: Session, skip: int = 0, limit: int = 100):
    """Service function to fetch users with pagination"""
    logger.info(f"Fetching users with skip={skip}, limit={limit}")
    return get_users(db, skip, limit)

def fetch_user_by_id(db: Session, user_id: int):
    """Service function to fetch a user by ID"""
    logger.info(f"Fetching user with ID: {user_id}")
    user = get_user_by_id(db, user_id)
    if not user:
        logger.warning(f"User with ID {user_id} not found")
    return user

def update_user_info(db: Session, user_id: int, user_update: UserUpdate):
    """Service function to update user information"""
    logger.info(f"Updating user with ID: {user_id}")
    
    # Check if user exists
    user = get_user_by_id(db, user_id)
    if not user:
        logger.warning(f"User with ID {user_id} not found")
        return None
        
    # If email is being updated, check if it's already in use
    if user_update.email and user_update.email != user.email:
        existing_user = get_user_by_email(db, user_update.email)
        if existing_user and existing_user.id != user_id:
            logger.warning(f"Email {user_update.email} is already in use by another user")
            raise ValueError(f"Email '{user_update.email}' is already in use")
    
    return update_user(db, user_id, user_update)

def remove_user(db: Session, user_id: int):
    """Service function to remove a user"""
    logger.info(f"Removing user with ID: {user_id}")
    
    # Check if user exists
    user = get_user_by_id(db, user_id)
    if not user:
        logger.warning(f"User with ID {user_id} not found")
        return False
        
    return delete_user(db, user_id)