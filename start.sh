#!/usr/bin/env bash
set -euo pipefail

MODEL_NAME="${MODEL_NAME:-qwen2.5:0.5b}"
export OLLAMA_HOST="${OLLAMA_HOST:-0.0.0.0:11434}"

cleanup() {
  if [[ -n "${OLLAMA_PID:-}" ]] && kill -0 "${OLLAMA_PID}" 2>/dev/null; then
    kill "${OLLAMA_PID}"
  fi
}

trap cleanup EXIT

echo "Starting Ollama server..."
ollama serve >/tmp/ollama.log 2>&1 &
OLLAMA_PID=$!

echo "Waiting for Ollama to be ready..."
for _ in {1..60}; do
  if curl -fsS "http://127.0.0.1:11434/api/tags" >/dev/null; then
    break
  fi
  sleep 1
done

# Fail fast if Ollama is still unavailable after waiting.
if ! curl -fsS "http://127.0.0.1:11434/api/tags" >/dev/null; then
  echo "ERROR: Ollama is not ready after 60 seconds. Check /tmp/ollama.log for details." >&2
  exit 1
fi

echo "Pulling model ${MODEL_NAME}..."
ollama pull "${MODEL_NAME}"

echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
