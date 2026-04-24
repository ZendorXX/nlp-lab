"""Вспомогательные функции клиента для работы с локальным Ollama."""

from __future__ import annotations

import os
from typing import Any

import requests


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:0.5b")


def check_ollama_ready(timeout: float = 3.0) -> bool:
    """Возвращает True, если сервер Ollama отвечает на endpoint tags."""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=timeout)
        return response.ok
    except requests.RequestException:
        return False


def generate_with_ollama(prompt: str, timeout: float = 90.0) -> dict[str, Any]:
    """Отправляет промпт в Ollama и возвращает JSON с ответом модели."""
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json()
