"""FastAPI-обертка для пересылки запросов в Ollama."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import requests

from app.ollama_client import generate_with_ollama, check_ollama_ready


app = FastAPI(title="LLM Spam POC Service")


class GenerateRequest(BaseModel):
    """Схема запроса для генерации ответа модели."""

    prompt: str = Field(..., min_length=1, description="Входной промпт для LLM.")


class GenerateResponse(BaseModel):
    """Схема ответа, возвращаемая FastAPI-эндпоинтом."""

    model: str
    response: str


@app.get("/health")
def healthcheck() -> dict[str, str]:
    """Возвращает статус доступности FastAPI и подключения к Ollama."""
    if not check_ollama_ready():
        raise HTTPException(status_code=503, detail="Ollama is not ready")
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest) -> GenerateResponse:
    """Пересылает промпт в Ollama и возвращает сгенерированный ответ."""
    try:
        data = generate_with_ollama(request.prompt)
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"Ollama request failed: {exc}") from exc

    return GenerateResponse(model=data.get("model", "unknown"), response=data.get("response", ""))
