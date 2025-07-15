from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
from .analyzer import analyze_code_string  # Your existing analyzer.py function

app = FastAPI()

# Define the expected input JSON schema
class CodeInput(BaseModel):
    code: str

@app.post("/analyze")
async def analyze_code(input: CodeInput) -> Any:
    result = analyze_code_string(input.code)
    return {"pylint_output": result}
