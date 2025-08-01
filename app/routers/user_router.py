# app/routers/user_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import  schemas, services, token
from app.database import Base, SessionLocal, engine
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas
from app.token import verify_token
from fastapi.security import OAuth2PasswordBearer
from app.dependencies import get_current_user  # if you created that


Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/users", tags=["Users"])

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return services.create_user(db, user)

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


@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: schemas.UserOut = Depends(get_current_user)):
    return current_user