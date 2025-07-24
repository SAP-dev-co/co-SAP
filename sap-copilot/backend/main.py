# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.analyze_error import router as analyze_error_router

app = FastAPI(title="SAP Copilot Backend")

# Allow frontend (VS Code extension) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(analyze_error_router, prefix="/api")
