from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user_router
from app.db import Base, engine  # Import Base and engine to create tables
import logging
import uvicorn

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Ensure tables are created before the app starts
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Management API",
    description="A RESTful API for managing user data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred. Please check server logs."}
    )

# Include Routes
app.include_router(user_router, prefix="/api/users", tags=["Users"])

# Root Endpoint
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to User Management API",
            }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
