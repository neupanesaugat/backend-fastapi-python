
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from app import  schemas, services, token
from app.database import Base, SessionLocal, engine
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas
from app.token import verify_token
from fastapi.security import OAuth2PasswordBearer
from app.dependencies import get_current_user  

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/users", tags=["Users"])

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST endpoint for user registration
@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return services.create_user(db, user)

# POST endpoint for user login
@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    authenticated_user = services.authenticate_user(db, user.email, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = token.create_access_token(data={"email": authenticated_user.email})
    return {
        "user": authenticated_user,
        "access_token": access_token,
        "token_type": "bearer"
    }

# GET endpoint to get the current user
@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: schemas.UserOut = Depends(get_current_user)):
    return current_user


# GET endpoint to list all users
@router.get("/list", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    users = services.get_all_users(db)
    return users


# GET endpoint to get a user by ID
@router.get("/list/{user_id}", response_model=schemas.UserOut)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = services.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# DELETE endpoint to delete a user by ID
@router.delete("/delete/{user_id}", status_code=200)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = services.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    services.delete_user_by_id(db, user_id)
    return {"message": f"User with id {user_id} deleted successfully."}




