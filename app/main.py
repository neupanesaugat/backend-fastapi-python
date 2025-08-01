
from fastapi import FastAPI
from app.routers import user_router

# Create the FastAPI app instance
app = FastAPI()

# Include the user router
app.include_router(user_router.router)
