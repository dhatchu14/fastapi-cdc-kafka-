from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.models import User
from app.schemas import UserCreate, UserUpdate
import logging

logger = logging.getLogger(__name__)

def create_user(db: Session, user: UserCreate):
    """Create a new user in the database"""
    try:
        new_user = User(
            name=user.name,
            email=user.email,
            address=user.address,
            phone=user.phone
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating user: {str(e)}")
        if "duplicate key" in str(e).lower() and "email" in str(e).lower():
            raise ValueError(f"User with email '{user.email}' already exists")
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating user: {str(e)}")
        raise

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of users with pagination"""
    try:
        users = db.query(User).offset(skip).limit(limit).all()
        count = db.query(User).count()
        return users, count
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching users: {str(e)}")
        raise

def get_user_by_id(db: Session, user_id: int):
    """Get a user by their ID"""
    try:
        return db.query(User).filter(User.id == user_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching user {user_id}: {str(e)}")
        raise

def get_user_by_email(db: Session, email: str):
    """Get a user by their email"""
    try:
        return db.query(User).filter(User.email == email).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching user by email {email}: {str(e)}")
        raise

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    """Update a user's information"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
            
        # Update only the fields that are provided
        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
            
        try:
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError as e:
            db.rollback()
            if "duplicate key" in str(e).lower() and "email" in str(e).lower():
                raise ValueError(f"User with email '{user_update.email}' already exists")
            raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error updating user {user_id}: {str(e)}")
        raise

def delete_user(db: Session, user_id: int):
    """Delete a user by their ID"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
            
        db.delete(user)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error deleting user {user_id}: {str(e)}")
        raise