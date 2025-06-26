import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from models import (
    Portfolio,
    LoginRequest,
    SignupUserRequest,
    CreateCommunityRequest,
    UserCommunity,
    UpdateUserProfileRequest,
)
from settings import settings
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from ai import router
from db import (
    verify_user_credentials,
    create_user,
    get_user_portfolio,
    create_community_for_user,
    update_user_profile_for_user,
)
from llm import stream_llm_with_instructor

app = FastAPI()

app.include_router(router)


# Add CORS middleware to allow cross-origin requests (for frontend to access backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login")
async def login(request: LoginRequest):
    verified_user = await verify_user_credentials(request.email, request.password)
    if verified_user:
        return verified_user

    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/signup")
async def signup(request: SignupUserRequest):
    try:
        new_user = await create_user(request)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/portfolio/{user_id}")
async def get_portfolio(user_id: int) -> Portfolio:
    try:
        return await get_user_portfolio(user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/communities")
async def create_community(request: CreateCommunityRequest) -> UserCommunity:
    try:
        return await create_community_for_user(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/users/{user_id}")
async def update_user_profile(
    user_id: int, request: UpdateUserProfileRequest
) -> Portfolio:
    try:
        return await update_user_profile_for_user(user_id, request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
