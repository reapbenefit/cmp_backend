import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from models import ChatResponse
from settings import settings
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from ai import router

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
