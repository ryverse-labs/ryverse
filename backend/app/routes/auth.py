"""
Authentication routes: signup, login, and current user.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from app.db.mongo import db
from app.models.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token
from app.deps.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


# @router.post("/signup")
# async def signup(user: UserCreate):
#     """Register a new user."""
#     existing = await db.users.find_one({"email": user.email})
#     if existing:
#         raise HTTPException(status_code=400, detail="User already exists")

#     hashed = hash_password(user.password)

#     result = await db.users.insert_one({
#         "name": user.name,
#         "email": user.email,
#         "password": hashed,
#     })

#     token = create_access_token({"user_id": str(result.inserted_id)})
#     return {"access_token": token, "token_type": "bearer"}




@router.post("/signup")
async def signup(user: UserCreate):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    try:
        hashed = hash_password(user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = await db.users.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hashed
    })

    token = create_access_token({"user_id": str(result.inserted_id)})

    return {"access_token": token}




@router.post("/login")
async def login(user: UserLogin):
    """Authenticate user and return JWT."""
    db_user = await db.users.find_one({"email": user.email})

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"user_id": str(db_user["_id"])})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def me(current=Depends(get_current_user)):
    """Return current authenticated user (minimal)."""
    return current