import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)

# Get database URL from environment variables or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:root@localhost:5432/test_db"
)

try:
    # Create SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    
    # Create sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create base class for models
    Base = declarative_base()
    
    logger.info("Database connection established successfully")
except Exception as e:
    logger.error(f"Failed to connect to database: {str(e)}")
    raise

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()